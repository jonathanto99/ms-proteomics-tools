#!/usr/bin/env python3
"""
MSPP plot.py - Plot Generation
Contains the core visualization logic.
"""

import base64
import io
import re
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")
plt.style.use("dark_background")


def fig_to_base64(fig):
    """Convert matplotlib figure to base64 encoded PNG."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_base64


class PlotGenerator:
    """Handles matplotlib visualization logic for bar charts and boxplots."""

    # Colors associated with each organism for consistent branding across plots
    COLORS = {"HeLa": "#9b59b6", "E.coli": "#e67e22", "Yeast": "#16a085"}

    def __init__(self, processor):
        self.processor = processor

    def create_bar_chart_figure(self, data, figsize=(12, 7)):
        """Generates a stacked bar chart showing protein IDs per organism for each sample."""
        counts = self.processor.calculate_protein_id_counts(data)

        def get_sort_val(name):
            """Sorts samples numerically based on their ID found in the filename."""
            raw = self.processor.file_to_raw_column.get(name, name)
            m = re.search(r"(\d+)", Path(raw).stem)
            return int(m.group(1)) if m else 0

        sorted_samples = sorted(counts.index, key=get_sort_val)
        counts = counts.reindex(sorted_samples)

        fig, ax = plt.subplots(figsize=figsize)
        bottom = np.zeros(len(counts))

        # Build stacked bars
        for org in self.processor.ORGANISMS:
            ax.bar(
                range(len(counts)),
                counts[org],
                bottom=bottom,
                label=org,
                color=self.COLORS.get(org),
                alpha=0.8,
            )
            bottom += counts[org].values

        # Add text labels in the middle of each bar segment
        for i, sample in enumerate(counts.index):
            y_off = 0
            for org in self.processor.ORGANISMS:
                val = counts.loc[sample, org]
                if val > 0:
                    ax.text(
                        i,
                        y_off + val / 2,
                        str(int(val)),
                        ha="center",
                        va="center",
                        fontsize=9,
                        fontweight="bold",
                        color="white",
                    )
                    y_off += val

        x_labels = [Path(self.processor.file_to_raw_column.get(s, s)).name for s in counts.index]
        ax.set_xticks(range(len(counts)))
        ax.set_xticklabels(x_labels, rotation=45, ha="right")
        ax.set_title("Protein/Peptide ID Counts by Organism", fontsize=14, fontweight="bold")
        ax.legend(title="Organism", loc="upper right")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        return fig

    def create_comparison_figure(self, data, figsize=(18, 16)):
        """
        Generates three subplots (HeLa, E.coli, Yeast) showing boxplots of log2 intensity ratios.
        Expected ratios (ref lines) are derived from the experimental mixing design.
        """
        results = self.processor.calculate_sample_comparison_data(data)
        fig, axes = plt.subplots(3, 1, figsize=figsize)

        # Configuration for each organism: (Organism Name, Title, Expected Ratio Line)
        configs = [
            ("HeLa", "HeLa Log2 Ratio (Expected: 0)", 0),
            ("E.coli", "E.coli Log2 Ratio (Expected: -2)", -2),
            ("Yeast", "Yeast Log2 Ratio (Expected: 1)", 1),
        ]

        for ax, (org, title, ref) in zip(axes, configs, strict=False):
            if results.get(org):
                self.plot_ratio_comparison(
                    ax, results[org], title, self.COLORS.get(org, "#95a5a6"), ref
                )
            else:
                ax.text(0.5, 0.5, f"No {org} data", transform=ax.transAxes, ha="center")

        plt.suptitle("Intensity Ratio Comparison by Run", fontsize=16, fontweight="bold", y=0.995)
        plt.tight_layout()
        return fig

    def plot_ratio_comparison(self, ax, results, title, color, ref_line):
        """Internal helper to plot individual boxplots for a specific organism's ratios."""
        data_arrays = [r[0] for r in results]
        labels = [r[1] for r in results]
        pos = np.arange(1, len(data_arrays) + 1)

        bp = ax.boxplot(
            data_arrays,
            positions=pos,
            widths=0.6,
            patch_artist=True,
            showmeans=True,
            flierprops={"marker": "o", "markerfacecolor": color, "markersize": 3, "alpha": 0.4},
            meanprops={"marker": "s", "markerfacecolor": "white", "markersize": 5},
        )

        for patch in bp["boxes"]:
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
            patch.set_edgecolor("white")

        plt.setp(bp["medians"], color="#2c3e50", linewidth=2.5)

        # Overlay median values as text on the plot for quick reference
        medians = []
        for i, arr in enumerate(data_arrays):
            m = np.median(arr)
            medians.append(m)
            ax.text(
                i + 1,
                m,
                f"{m:.2f}",
                fontsize=9,
                va="bottom",
                ha="center",
                color="white",
                fontweight="bold",
                bbox={"boxstyle": "round", "facecolor": "black", "alpha": 0.5},
            )

        # Plot the 'Ground Truth' horizontal line
        ax.axhline(
            y=ref_line, color="#f39c12", linestyle="--", linewidth=2, label=f"Expected: {ref_line}"
        )
        if medians:
            ax.plot([], [], " ", label=f"Mean Median: {np.mean(medians):.2f}")

        ax.set_title(title, fontweight="bold")
        ax.set_xticks(pos)
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)
        ax.legend(fontsize=9, loc="upper right")
        ax.grid(axis="y", alpha=0.3)
