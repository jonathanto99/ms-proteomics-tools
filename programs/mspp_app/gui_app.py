#!/usr/bin/env python3
"""
MSPP Data Plotter - CustomTkinter API
This module serves the MSPP GUI application and provides analytical endpoints.
"""

from tkinter import filedialog, messagebox
import threading
import os
import matplotlib.pyplot as plt
import customtkinter as ctk

from logic import DataProcessor, PlotGenerator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MSPPDesktopApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MSPP Data Plotter")
        self.geometry("1400x800")

        # Initialize core logic
        self.processor = DataProcessor()
        self.plotter = PlotGenerator(self.processor)
        
        # Application State
        self.file_paths = []
        self.current_data = None
        
        # UI/Plotting state
        self.current_canvas = None
        self.current_toolbar = None
        self.current_fig = None
        
        # Thread safety lock for Matplotlib's global state machine
        self.plot_lock = threading.Lock()

        self._build_ui()

    def _build_ui(self):
        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.logo_label = ctk.CTkLabel(self.sidebar, text="MSPP Tools", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(padx=20, pady=(20, 10))

        self.load_btn = ctk.CTkButton(self.sidebar, text="1. Load TSV Files", command=self.load_files)
        self.load_btn.pack(padx=20, pady=10)

        self.file_count_label = ctk.CTkLabel(self.sidebar, text="0 files loaded")
        self.file_count_label.pack(padx=20, pady=(0, 20))

        self.plot_type = ctk.StringVar(value="bar-chart")
        ctk.CTkRadioButton(self.sidebar, text="Protein ID Bar Chart", variable=self.plot_type, value="bar-chart").pack(padx=20, pady=10, anchor="w")
        ctk.CTkRadioButton(self.sidebar, text="Sample Comparison", variable=self.plot_type, value="sample-comparison").pack(padx=20, pady=10, anchor="w")

        self.plot_btn = ctk.CTkButton(self.sidebar, text="2. Generate Plot", command=self.generate_plot)
        self.plot_btn.pack(padx=20, pady=20)

        self.export_btn = ctk.CTkButton(self.sidebar, text="3. Export All Plots", command=self.export_plots, state="disabled")
        self.export_btn.pack(padx=20, pady=10)

        self.clear_btn = ctk.CTkButton(self.sidebar, text="Clear Data", command=self.clear_data, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        self.clear_btn.pack(padx=20, pady=(40, 10))

        # --- Main Plot Area ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def load_files(self):
        """Open file dialog and store paths."""
        files = filedialog.askopenfilenames(
            title="Select Proteomics Data",
            filetypes=[("Text Files", "*.txt *.tsv"), ("All Files", "*.*")]
        )
        if files:
            self.file_paths = list(files)
            self.file_count_label.configure(text=f"{len(self.file_paths)} files loaded")
            self.current_data = None
            if hasattr(self, 'export_btn'):
                self.export_btn.configure(state="disabled")

    def clear_data(self):
        """Reset the application state and clear the plot area."""
        self.file_paths = []
        self.current_data = None
        self.file_count_label.configure(text="0 files loaded")
        
        if hasattr(self, 'export_btn'):
            self.export_btn.configure(state="disabled")
        
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None
        if self.current_toolbar:
            self.current_toolbar.destroy()
            self.current_toolbar = None
            
        # Clean up matplotlib memory
        if self.current_fig:
            plt.close(self.current_fig)
            self.current_fig = None

    def generate_plot(self):
        """Process data and render the matplotlib figure to the UI using a background thread."""
        if not self.file_paths:
            messagebox.showwarning("No Files", "Please load files first.")
            return

        # Extract Tkinter variables on the main thread before passing to the worker
        selected_plot_type = self.plot_type.get()

        self.plot_btn.configure(state="disabled", text="Processing...")
        self.export_btn.configure(state="disabled")

        thread = threading.Thread(target=self._plot_worker, args=(selected_plot_type,), daemon=True)
        thread.start()

    def _plot_worker(self, plot_type):
        try:
            if self.current_data is None:
                self.current_data = self.processor.load_data(self.file_paths)

            # Lock the pyplot global state machine while generating
            with self.plot_lock:
                if plot_type == "bar-chart":
                    fig = self.plotter.create_bar_chart_figure(self.current_data)
                else:
                    fig = self.plotter.create_comparison_figure(self.current_data)

            self.after(0, self._on_plot_ready, fig)
        except Exception as e:
            self.after(0, self._on_plot_error, str(e))

    def _on_plot_ready(self, fig):
        self._render_figure(fig)
        self.plot_btn.configure(state="normal", text="2. Generate Plot")
        self.export_btn.configure(state="normal")

    def _on_plot_error(self, error_msg):
        self.plot_btn.configure(state="normal", text="2. Generate Plot")
        messagebox.showerror("Error", f"Failed to generate plot:\n\n{error_msg}")

    def export_plots(self):
        if self.current_data is None:
            messagebox.showinfo("No Data", "Please generate a plot first to load the data.")
            return

        save_dir = filedialog.askdirectory(title="Select Directory to Save Plots")
        if not save_dir:
            return

        self.export_btn.configure(state="disabled", text="Exporting...")
        thread = threading.Thread(target=self._export_worker, args=(save_dir,), daemon=True)
        thread.start()

    def _export_worker(self, save_dir):
        try:
            # Lock the pyplot global state machine during headless generation
            with self.plot_lock:
                fig_bar = self.plotter.create_bar_chart_figure(self.current_data)
                fig_comp = self.plotter.create_comparison_figure(self.current_data)

                bar_path = os.path.join(save_dir, "protein_id_bar_chart.png")
                comp_path = os.path.join(save_dir, "sample_comparison.png")

                fig_bar.savefig(bar_path, dpi=300, bbox_inches="tight")
                fig_comp.savefig(comp_path, dpi=300, bbox_inches="tight")

                plt.close(fig_bar)
                plt.close(fig_comp)

            self.after(0, self._on_export_success, save_dir)
        except Exception as e:
            self.after(0, self._on_export_error, str(e))

    def _on_export_success(self, save_dir):
        self.export_btn.configure(state="normal", text="3. Export All Plots")
        messagebox.showinfo("Export Successful", f"Both plots saved successfully to:\n{save_dir}")

    def _on_export_error(self, error_msg):
        self.export_btn.configure(state="normal", text="3. Export All Plots")
        messagebox.showerror("Export Error", f"Failed to export plots:\n\n{error_msg}")

    def _render_figure(self, fig):
        """Embeds a Matplotlib Figure into the CustomTkinter frame."""
        # Clean up old matplotlib memory before rendering to avoid memory leaks
        if self.current_fig:
            plt.close(self.current_fig)
            
        self.current_fig = fig

        # Clear existing widgets
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
        if self.current_toolbar:
            self.current_toolbar.destroy()

        # Create drawing canvas
        self.current_canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
        self.current_canvas.draw()

        # Add matplotlib toolbar
        self.current_toolbar = NavigationToolbar2Tk(self.current_canvas, self.main_frame)
        self.current_toolbar.update()

        # Pack into view
        self.current_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

if __name__ == "__main__":
    app = MSPPDesktopApp()
    app.mainloop()
