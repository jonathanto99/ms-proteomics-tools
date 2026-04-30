#!/usr/bin/env python3
"""
MSPP logic.py - Data Processing
Contains the core analytical algorithms.
"""

import logging
import re
from pathlib import Path

import numpy as np
import pandas as pd


class DataProcessor:
    """
    Handles data ingestion, organism classification, and quantitative calculations.
    Uses vectorized pandas operations for performance on large proteomics datasets.
    """

    # Standard organisms used in the MSPP (Mixed Species Proteomics Performance) benchmark
    ORGANISMS = ["HeLa", "E.coli", "Yeast"]

    # Mapping of organism types to expected Uniprot naming conventions or taxonomic strings
    # in the protein identifiers (e.g., _HUMAN for HeLa).
    ORGANISM_PATTERNS = {
        "HeLa": ["_HUMAN", "HOMO_SAPIENS"],
        "E.coli": [
            "_ECOLI",
            "_ECOL",
            "_ECO2",
            "_ECO5",
            "_ECO7",
            "_SHIF",
            "_SHIB",
            "_SHIS",
            "ESCHERICHIA",
        ],
        "Yeast": ["_YEAST", "SACCHAROMYCES", "CEREVISIAE"],
    }

    def __init__(self):
        self.file_to_raw_column = {}  # Map source file to its specific .raw intensity column
        self.cached_data = None
        self.cached_file_list = []

    def identify_organism_vectorized(self, series):
        """
        Classifies protein IDs into their respective organisms using fast vectorized string matching.
        This is preferred over row-by-row iteration for files with >100k rows.
        """
        upper = series.fillna("").astype(str).str.upper()
        result = pd.Series("Unknown", index=series.index)
        for organism, patterns in self.ORGANISM_PATTERNS.items():
            # Join patterns with OR operator for regex-based matching
            mask = upper.str.contains("|".join(patterns), regex=True)
            result = result.where(~mask, organism)
        return pd.Categorical(result, categories=self.ORGANISMS)

    def load_data(self, file_paths):
        """
        Load data from selected files with memory optimization.

        Strategy:
        1. Fast scan: Peek at headers to identify target columns (.raw intensities and Protein IDs).
        2. Selective load: Use 'usecols' to only pull required columns into RAM, significantly
           reducing the memory footprint for large FragPipe/MaxQuant outputs.
        3. Fallback: If selective load fails (e.g. malformed CSV), attempt a full load.
        """
        if not file_paths:
            raise ValueError("No files provided")

        if self.cached_data is not None and self.cached_file_list == file_paths:
            return self.cached_data

        all_data = []
        self.file_to_raw_column = {}

        for filepath in file_paths:
            try:
                # OPTIMIZATION: Scan headers first to load ONLY required columns
                header_df = pd.read_csv(filepath, sep="\t", nrows=0)
                cols = header_df.columns.tolist()

                raw_cols = [c for c in cols if ".raw" in c.lower()]
                prot_col = next(
                    (c for c in ["Protein.Names", "Protein.Group", "Protein.Ids"] if c in cols),
                    None,
                ) or next((c for c in cols if "protein" in c.lower()), None)

                usecols = [c for c in [prot_col] + raw_cols if c]

                # Load only necessary columns to save RAM
                df = pd.read_csv(
                    filepath, sep="\t", usecols=usecols if usecols else None, low_memory=False
                )  # ty:ignore[no-matching-overload]
            except Exception as e:
                logging.warning(f"Fast load failed for {filepath}, falling back to full load: {e}")
                df = pd.read_csv(filepath, sep="\t", low_memory=False)
                raw_cols = [c for c in df.columns if ".raw" in c.lower()]
                prot_col = next(
                    (c for c in ["Protein.Names", "Protein.Group"] if c in df.columns), None
                )

            source_name = Path(filepath).stem
            df["Source_File"] = source_name

            if raw_cols:
                self.file_to_raw_column[source_name] = raw_cols[0]

            df["Organism"] = (
                self.identify_organism_vectorized(df[prot_col]) if prot_col else "Unknown"
            )

            # Filter out unwanted organisms immediately to keep the dataframe small
            df = df[df["Organism"].isin(self.ORGANISMS)]
            all_data.append(df)

        self.cached_data = pd.concat(all_data, ignore_index=True)
        self.cached_file_list = file_paths.copy()
        return self.cached_data

    def calculate_intensity_ratios(self, data, e25_file, e100_file, organism):
        """
        Calculate log2 intensity ratios (E25/E100) for consensus proteins.

        Consensus proteins are those identified in BOTH files for the given organism.
        Filtering for consensus ensures the ratio is meaningful and not biased by
        missing values in one of the runs.
        """
        if e25_file not in self.file_to_raw_column or e100_file not in self.file_to_raw_column:
            return None

        e25_col = self.file_to_raw_column[e25_file]
        e100_col = self.file_to_raw_column[e100_file]

        e25_data = data[data["Source_File"] == e25_file].copy()
        e100_data = data[data["Source_File"] == e100_file].copy()

        e25_org = e25_data[e25_data["Organism"] == organism]
        e100_org = e100_data[e100_data["Organism"] == organism]

        if len(e25_org) == 0 or len(e100_org) == 0:
            return None

        prot_col = next(
            (c for c in ["Protein.Group", "Protein.Ids", "Protein.Names"] if c in e25_org.columns),
            None,
        )
        if not prot_col:
            return None

        # Filter for valid, non-zero intensities before ratio calculation
        e25_v = e25_org[(e25_org[e25_col].notna()) & (e25_org[e25_col] > 0)]
        e100_v = e100_org[(e100_org[e100_col].notna()) & (e100_org[e100_col] > 0)]

        # Find consensus proteins (intersection)
        common = set(e25_v[prot_col]) & set(e100_v[prot_col])
        if not common:
            return None

        e25_c = e25_v[e25_v[prot_col].isin(common)].set_index(prot_col)
        e100_c = e100_v[e100_v[prot_col].isin(common)].set_index(prot_col)

        idx = e25_c.index.intersection(e100_c.index)

        # Calculate ratios (log2) - Log transformation normalizes the distribution
        ratios = np.log2(e25_c.loc[idx, e25_col].values / e100_c.loc[idx, e100_col].values)
        return ratios[np.isfinite(ratios)]

    def calculate_protein_id_counts(self, data):
        """Calculate protein ID counts grouped by organism and source file."""
        counts = data.groupby(["Source_File", "Organism"]).size().unstack(fill_value=0)
        return counts.reindex(columns=self.ORGANISMS, fill_value=0)

    def calculate_sample_comparison_data(self, data):
        """
        Pairs samples based on experimental conditions encoded in filenames.

        Experimental Design:
        - Samples are typically named with "E25" (or "Y150") and "E100" (or "Y75").
        - "E25" vs "E100" refers to specific dilution/mixing ratios of the organisms.
        - Strict pairing looks for matching suffixes after the condition tag.
        """
        sample_files = sorted(data["Source_File"].unique())
        if len(sample_files) < 2:
            raise ValueError("Need at least 2 samples to create comparisons")

        # Separate files into the two experimental condition groups
        e25_exp, e100_exp = [], []
        for f in sample_files:
            if re.search(r"E[-_]?25|Y[-_]?150|HYE[-_]?[1A]", f.upper()):
                e25_exp.append(f)
            elif re.search(r"E[-_]?100|Y[-_]?75|HYE[-_]?[2B]", f.upper()):
                e100_exp.append(f)

        strict_pairs_dict, singlets = {}, []

        def get_suffix(name):
            """Extracts the unique identifier/suffix after the condition (e.g., E25_Rep1 -> Rep1)."""
            m = re.search(
                r"(?:E[-_]?(?:25|100)|Y[-_]?(?:150|75)|HYE[-_]?[12AB])[-_](.*)", name, re.IGNORECASE
            )
            return m.group(1) if m else None

        # Attempt to pair E25 and E100 files that share the same suffix (e.g. same replicate)
        for s in e25_exp:
            suff = get_suffix(s)
            if suff:
                if suff not in strict_pairs_dict:
                    strict_pairs_dict[suff] = {}
                if "E25" in strict_pairs_dict[suff]:
                    singlets.append(s)
                else:
                    strict_pairs_dict[suff]["E25"] = s
            else:
                singlets.append(s)

        for s in e100_exp:
            suff = get_suffix(s)
            if suff:
                if suff not in strict_pairs_dict:
                    strict_pairs_dict[suff] = {}
                if "E100" in strict_pairs_dict[suff]:
                    singlets.append(s)
                else:
                    strict_pairs_dict[suff]["E100"] = s
            else:
                singlets.append(s)

        strict_pairs = []
        for suff, p in strict_pairs_dict.items():  # noqa: B007
            if "E25" in p and "E100" in p:
                strict_pairs.append((p["E25"], p["E100"]))
            else:
                singlets.extend(p.values())

        if strict_pairs:
            logging.info(
                f"Strict pairing: {len(strict_pairs)} pairs. Excluded {len(singlets)} singlets."
            )
            sample_pairs = sorted(strict_pairs)
        else:
            # Fallback: if suffixes don't match, pair files by their sorted index
            logging.warning("No suffix matches. Falling back to index pairing.")
            e25_s, e100_s = sorted(e25_exp), sorted(e100_exp)
            sample_pairs = list(zip(e25_s, e100_s, strict=False))

        results = {"HeLa": [], "E.coli": [], "Yeast": []}
        for e25, e100 in sample_pairs:

            def get_pk(name):
                """Extracts a short numeric key from the filename for plotting labels."""
                raw = self.file_to_raw_column.get(name, "")
                m = re.search(r"(\d+)", Path(raw).stem if raw else name)
                return m.group(1) if m else name

            label = f"{get_pk(e25)} vs {get_pk(e100)}"
            for org in self.ORGANISMS:
                ratios = self.calculate_intensity_ratios(data, e25, e100, org)
                if ratios is not None:
                    results[org].append((ratios, label))

        if not any(results.values()):
            raise ValueError("No valid sample pairs found")
        return results
