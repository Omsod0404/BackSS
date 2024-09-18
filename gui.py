import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import main

def run_script():
    file1 = file1_entry.get()
    file2 = file2_entry.get()
    output_folder = output_entry.get()

    # Validate the selected paths
    if not (os.path.isfile(file1) and os.path.isfile(file2)):
        messagebox.showerror("Error", "Please select valid input files.")
        return
    if not os.path.isdir(output_folder):
        messagebox.showerror("Error", "Please select a valid output folder.")
        return

    # Start the progress bar and disable the Run button
    progress_bar.grid(row=3, column=1, padx=10, pady=20)
    progress_bar.start()
    run_button.config(state=tk.DISABLED)

    # Run the script in a separate thread to avoid freezing the UI
    threading.Thread(target=execute_script, args=(file1, file2, output_folder)).start()

def execute_script(file1, file2, output_folder):
    try:
        # Run your script and capture the output
        result = main.run_script(file1, file2, output_folder)
        if result['success']:
            messagebox.showinfo("Success", "Script executed successfully!")
        else:            messagebox.showerror("Error", f"Script failed: {result['success']}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        # Stop the progress bar, hide it, and re-enable the Run button
        progress_bar.stop()
        progress_bar.grid_remove()
        run_button.config(state=tk.NORMAL)

def select_file1():
    file_path = filedialog.askopenfilename()
    file1_entry.delete(0, tk.END)
    file1_entry.insert(0, file_path)

def select_file2():
    file_path = filedialog.askopenfilename()
    file2_entry.delete(0, tk.END)
    file2_entry.insert(0, file_path)

def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_path)

# Create the main window
root = tk.Tk()
root.title("Comparación SIIA-CH")
root.configure(bg='white', padx=10, pady=10)

# Apply modern style using ttk
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12), padding=5)

# Create labels and entry fields for file selection
ttk.Label(root, text="Archivo SIIA:").grid(row=0, column=0, padx=15, pady=10, sticky=tk.E)
file1_entry = ttk.Entry(root, width=50)
file1_entry.grid(row=0, column=1, padx=10, pady=10)
ttk.Button(root, text="Buscar...", command=select_file1).grid(row=0, column=2, padx=10, pady=10)

ttk.Label(root, text="Archivo CH:").grid(row=1, column=0, padx=15, pady=10, sticky=tk.E)
file2_entry = ttk.Entry(root, width=50)
file2_entry.grid(row=1, column=1, padx=10, pady=10)
ttk.Button(root, text="Buscar...", command=select_file2).grid(row=1, column=2, padx=10, pady=10)

ttk.Label(root, text="Folder de\nGuardado:").grid(row=2, column=0, padx=15, pady=10, sticky=tk.E)
output_entry = ttk.Entry(root, width=50)
output_entry.grid(row=2, column=1, padx=10, pady=10)
ttk.Button(root, text="Buscar...", command=select_output_folder).grid(row=2, column=2, padx=10, pady=10)

# Create the progress bar (hidden by default)
progress_bar = ttk.Progressbar(root, mode='indeterminate', length=400)
progress_bar.grid(row=3, column=1, padx=10, pady=20)
progress_bar.grid_remove()  # Hide the progress bar initially

# Run script button
run_button = ttk.Button(root, text="Comparar", command=run_script)
run_button.grid(row=4, column=1, padx=10, pady=20)

# Start the GUI event loop
root.mainloop()