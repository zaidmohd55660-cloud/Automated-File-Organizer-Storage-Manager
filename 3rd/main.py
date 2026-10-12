import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

# File Categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Documents": [".pdf", ".docx", ".doc", ".pptx", ".xlsx", ".txt"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z"],
    "Programs": [".exe", ".msi", ".py"]
}

SYSTEM_FILES = [
    "DumpStack.log",
    "pagefile.sys",
    "hiberfil.sys",
    "swapfile.sys"
]

selected_folder = ""


def browse_folder():
    global selected_folder

    folder = filedialog.askdirectory()

    if folder:
        selected_folder = folder
        folder_label.config(text=folder)
        update_storage_info()


def log_message(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)


def organize_files():

    if not selected_folder:
        messagebox.showerror(
            "Error",
            "Please select a folder first."
        )
        return

    category_count = {
        "Images": 0,
        "Videos": 0,
        "Documents": 0,
        "Music": 0,
        "Archives": 0,
        "Programs": 0,
        "Others": 0
    }

    moved = 0

    log_box.delete(1.0, tk.END)
    log_message("===== ORGANIZATION STARTED =====\n")

    for file in os.listdir(selected_folder):

        file_path = os.path.join(selected_folder, file)

        if os.path.isdir(file_path):
            continue

        if file in SYSTEM_FILES:
            log_message(f"Skipped System File: {file}")
            continue

        ext = os.path.splitext(file)[1].lower()

        moved_flag = False

        for category, extensions in FILE_TYPES.items():

            if ext in extensions:

                dest_folder = os.path.join(
                    selected_folder,
                    category
                )

                os.makedirs(dest_folder, exist_ok=True)

                try:
                    shutil.move(
                        file_path,
                        os.path.join(dest_folder, file)
                    )

                    log_message(
                        f"{file}  --->  {category}"
                    )

                    category_count[category] += 1
                    moved += 1
                    moved_flag = True

                except Exception as e:
                    log_message(
                        f"Error moving {file}: {e}"
                    )

                break

        if not moved_flag:

            other_folder = os.path.join(
                selected_folder,
                "Others"
            )

            os.makedirs(other_folder, exist_ok=True)

            try:
                shutil.move(
                    file_path,
                    os.path.join(other_folder, file)
                )

                log_message(
                    f"{file}  --->  Others"
                )

                category_count["Others"] += 1
                moved += 1

            except Exception as e:
                log_message(
                    f"Error moving {file}: {e}"
                )

    log_message("\n===== SUMMARY =====")

    for cat, count in category_count.items():
        log_message(f"{cat}: {count} files")

    log_message(f"\nTotal Files Organized: {moved}")

    update_storage_info()

    messagebox.showinfo(
        "Success",
        f"{moved} files organized successfully!"
    )


def update_storage_info():

    if not selected_folder:
        return

    total, used, free = shutil.disk_usage(selected_folder)

    total_gb = total // (1024 ** 3)
    used_gb = used // (1024 ** 3)
    free_gb = free // (1024 ** 3)

    total_label.config(
        text=f"Total Space: {total_gb} GB"
    )

    used_label.config(
        text=f"Used Space: {used_gb} GB"
    )

    free_label.config(
        text=f"Free Space: {free_gb} GB"
    )


# GUI

root = tk.Tk()
root.title("Automated File Organizer & Storage Manager")
root.geometry("850x650")
root.configure(bg="#f4f6f7")

title = tk.Label(
    root,
    text="Automated File Organizer & Storage Manager",
    font=("Arial", 18, "bold"),
    bg="#f4f6f7"
)

title.pack(pady=10)

btn_browse = tk.Button(
    root,
    text="Select Folder",
    command=browse_folder,
    bg="#28a745",
    fg="white",
    font=("Arial", 12)
)

btn_browse.pack(pady=5)

folder_label = tk.Label(
    root,
    text="No Folder Selected",
    bg="#f4f6f7"
)

folder_label.pack()

btn_organize = tk.Button(
    root,
    text="Organize Files",
    command=organize_files,
    bg="#007bff",
    fg="white",
    font=("Arial", 12)
)

btn_organize.pack(pady=10)

# Storage Info

info_frame = tk.Frame(root, bg="white")
info_frame.pack(fill="x", padx=20, pady=10)

total_label = tk.Label(
    info_frame,
    text="Total Space: --",
    bg="white",
    font=("Arial", 11)
)

total_label.pack(pady=4)

used_label = tk.Label(
    info_frame,
    text="Used Space: --",
    bg="white",
    font=("Arial", 11)
)

used_label.pack(pady=4)

free_label = tk.Label(
    info_frame,
    text="Free Space: --",
    bg="white",
    font=("Arial", 11)
)

free_label.pack(pady=4)

# Log Section

log_title = tk.Label(
    root,
    text="Organization Log",
    font=("Arial", 12, "bold"),
    bg="#f4f6f7"
)

log_title.pack()

log_box = ScrolledText(
    root,
    height=18,
    width=100
)

log_box.pack(padx=15, pady=10)

root.mainloop()
