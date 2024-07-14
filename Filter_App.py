import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from scipy.signal import savgol_filter, butter, filtfilt, medfilt, cheby1
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class DataProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Processor App")
        self.filepath = None
        self.df = None
        self.canvas = None

        # GUI Elements
        self.label = tk.Label(root, text="Upload CSV or Excel File")
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=10)

        self.column_listbox_label = tk.Label(root, text="Select Columns:")
        self.column_listbox_label.pack(pady=5)
        self.column_listbox = tk.Listbox(root, selectmode='multiple', width=50, height=10)
        self.column_listbox.pack(pady=10)

        self.filter_label = tk.Label(root, text="Select Filter:")
        self.filter_label.pack(pady=5)
        self.filter_var = tk.StringVar()
        self.filter_options = ["Moving Average", "Savitzky-Golay", "Low-pass Filter", "High-pass Filter",
                               "Band-pass Filter", "Band-stop Filter", "Exponential Moving Average",
                               "Median Filter", "Butterworth Filter", "Chebyshev Filter"]
        self.filter_menu = ttk.Combobox(root, textvariable=self.filter_var, values=self.filter_options)
        self.filter_menu.pack(pady=5)
        self.filter_menu.bind("<<ComboboxSelected>>", self.clear_plot)

        self.window_size_label = tk.Label(root, text="Window Size:")
        self.window_size_label.pack(pady=5)
        self.window_size_entry = tk.Entry(root)
        self.window_size_entry.pack(pady=5)

        self.process_button = tk.Button(root, text="Process Data", command=self.process_data)
        self.process_button.pack(pady=20)

        self.save_button = tk.Button(root, text="Save Processed Data", command=self.save_data)
        self.save_button.pack(pady=20)

        self.author_label = tk.Label(root, text="Author: Rohith Jayaraman Krishnamurthy  CRN Lab UBC")
        self.author_label.pack(pady=10)

        self.progress_label = tk.Label(root, text="", fg="red")
        self.progress_label.pack(pady=5)

    def upload_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx *.xls")])
        if self.filepath:
            if self.filepath.endswith('.csv'):
                self.df = pd.read_csv(self.filepath, encoding='ISO-8859-1')
            else:
                self.df = pd.read_excel(self.filepath)

            self.column_listbox.delete(0, tk.END)
            for col in self.df.columns:
                self.column_listbox.insert(tk.END, col)

    def process_data(self):
        self.show_progress_message()
        self.root.update_idletasks()

        selected_indices = self.column_listbox.curselection()
        selected_columns = [self.column_listbox.get(i) for i in selected_indices]
        window_size = int(self.window_size_entry.get())
        filter_option = self.filter_var.get()

        if not selected_columns or not window_size or not filter_option:
            messagebox.showwarning("Input Error", "Please select columns, filter option, and provide window size.")
            self.progress_label.config(text="")
            return

        output_columns = [f"{col}_Filtered" for col in selected_columns]

        if filter_option == "Moving Average":
            for col, out_col in zip(selected_columns, output_columns):
                self.df[out_col] = self.df[col].rolling(window=window_size, min_periods=1).mean()
        elif filter_option == "Savitzky-Golay":
            for col, out_col in zip(selected_columns, output_columns):
                self.df[out_col] = savgol_filter(self.df[col], window_length=window_size, polyorder=2)
        elif filter_option == "Low-pass Filter":
            for col, out_col in zip(selected_columns, output_columns):
                b, a = butter(4, 0.1, btype='low')
                self.df[out_col] = filtfilt(b, a, self.df[col])
        elif filter_option == "High-pass Filter":
            for col, out_col in zip(selected_columns, output_columns):
                b, a = butter(4, 0.1, btype='high')
                self.df[out_col] = filtfilt(b, a, self.df[col])
        elif filter_option == "Band-pass Filter":
            for col, out_col in zip(selected_columns, output_columns):
                b, a = butter(4, [0.1, 0.3], btype='band')
                self.df[out_col] = filtfilt(b, a, self.df[col])
        elif filter_option == "Band-stop Filter":
            for col, out_col in zip(selected_columns, output_columns):
                b, a = butter(4, [0.1, 0.3], btype='bandstop')
                self.df[out_col] = filtfilt(b, a, self.df[col])
        elif filter_option == "Exponential Moving Average":
            for col, out_col in zip(selected_columns, output_columns):
                self.df[out_col] = self.df[col].ewm(span=window_size, adjust=False).mean()
        elif filter_option == "Median Filter":
            for col, out_col in zip(selected_columns, output_columns):
                self.df[out_col] = medfilt(self.df[col], kernel_size=window_size)
        elif filter_option == "Butterworth Filter":
            for col, out_col in zip(selected_columns, output_columns):
                b, a = butter(4, 0.1)
                self.df[out_col] = filtfilt(b, a, self.df[col])
        elif filter_option == "Chebyshev Filter":
            for col, out_col in zip(selected_columns, output_columns):
                b, a = cheby1(4, 0.1, 0.1)
                self.df[out_col] = filtfilt(b, a, self.df[col])

        # Plot the original and filtered data
        self.plot_data(selected_columns, output_columns)
        self.progress_label.config(text="Calculation Complete", fg="green")

    def clear_plot(self, event=None):
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
            self.canvas = None

    def show_progress_message(self):
        self.progress_label.config(text="Calculation in Progress...", fg="red")
        self.root.update_idletasks()

    def plot_data(self, original_columns, filtered_columns):
        self.clear_plot()
        fig, axs = plt.subplots(len(original_columns), 1, figsize=(10, 5 * len(original_columns)))

        if len(original_columns) == 1:
            axs = [axs]

        for i, (orig_col, filt_col) in enumerate(zip(original_columns, filtered_columns)):
            axs[i].plot(self.df['Time (min)'], self.df[orig_col], label=f'Original {orig_col}')
            axs[i].plot(self.df['Time (min)'], self.df[filt_col], label=f'Filtered {filt_col}')
            axs[i].set_title(f'{orig_col} - Original vs Filtered')
            axs[i].set_xlabel('Time (min)')
            axs[i].set_ylabel('Values')
            axs[i].legend()

        plt.tight_layout()

        # Display the plot in the Tkinter window
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def save_data(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if save_path:
            self.df.to_excel(save_path, index=False)
            messagebox.showinfo("Success", "Data processed and saved successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataProcessorApp(root)
    root.mainloop()
