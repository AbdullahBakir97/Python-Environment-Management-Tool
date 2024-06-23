import tkinter as tk
from tkinter import constants as tkc
from tkinter import ttk, filedialog, messagebox, simpledialog
from TKinterModernThemes import ThemedTKinterFrame
import TKinterModernThemes as TKMT
from TKinterModernThemes.WidgetFrame import Widget as WTWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from env_manager import EnvironmentManager
from file_manager import FileManager
from package_installer import PackageInstaller
from django_setup import DjangoSetup
from github_manager import RepoManager
from dir_structure import DirStructure
from db_manager import ToolDatabase
from PIL import Image, ImageTk
from tkcalendar import Calendar, DateEntry
import matplotlib.pyplot as plt
from ttkthemes import ThemedStyle
import sv_ttk
import sqlite3
import os
import random
import io
import glob
import cairosvg
import cairocffi as cairo

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Professional Tool")
        self.tool_db = ToolDatabase(db_path="./libraries.db")
        self.create_themed_frame()

    def create_themed_frame(self):
        self.style = ThemedStyle(self)
        sv_ttk.set_theme("dark")  # Set your preferred theme, e.g., "arc", "plastik", "clearlooks"
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)

        self.create_environment_tab(notebook)
        self.manage_files_tab(notebook)
        self.django_app_tab(notebook)
        self.add_library_tab(notebook)
        self.repository_tab(notebook)

        notebook.pack(expand=True, fill="both")

    def create_environment_tab(self, notebook):
        env_frame = ttk.Frame(notebook)
        notebook.add(env_frame, text="Environment")

        env_label_frame = ttk.LabelFrame(env_frame, text="Create Virtual Environment")
        env_label_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(env_label_frame, text="Enter Environment Name:").pack(pady=(10, 5))
        self.env_name_entry = ttk.Entry(env_label_frame, width=30)
        self.env_name_entry.pack(pady=5)

        create_button = ttk.Button(env_label_frame, text="Create", command=self.create_virtual_environment)
        create_button.pack(pady=10)

    def manage_files_tab(self, notebook):
        file_frame = ttk.Frame(notebook)
        notebook.add(file_frame, text="Manage Files")

        ttk.Label(file_frame, text="Manage Files and Projects", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Button(file_frame, text="Create File", command=self.create_file_dialog).pack(pady=5)
        ttk.Button(file_frame, text="Create Folder", command=self.create_folder_dialog).pack(pady=5)
        ttk.Button(file_frame, text="Delete File", command=self.delete_file_dialog).pack(pady=5)
        ttk.Button(file_frame, text="Delete Folder", command=self.delete_folder_dialog).pack(pady=5)

    def django_app_tab(self, notebook):
        django_frame = ttk.Frame(notebook)
        notebook.add(django_frame, text="Django App")

        django_label_frame = ttk.LabelFrame(django_frame, text="Django Management")
        django_label_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(django_label_frame, text="Create Django Project", command=self.create_django_project_dialog).pack(pady=5)
        ttk.Button(django_label_frame, text="Add Django App", command=self.add_django_app_dialog).pack(pady=5)

    def add_library_tab(self, notebook):
        library_frame = ttk.Frame(notebook)
        notebook.add(library_frame, text="Add Library")

        library_label_frame = ttk.LabelFrame(library_frame, text="Library Management")
        library_label_frame.pack(fill="both", expand=True, padx=10, pady=10)

        button_frame = ttk.Frame(library_label_frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Install Package", command=self.install_package_dialog).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Add Library", command=self.open_add_library_form).pack(side="left", padx=5)

        columns = ('Library Name', 'Version', 'Description', 'Actions')
        self.library_tree = ttk.Treeview(library_label_frame, columns=columns, show='headings')
        self.library_tree.heading('Library Name', text='Library Name')
        self.library_tree.heading('Version', text='Version')
        self.library_tree.heading('Description', text='Description')
        self.library_tree.heading('Actions', text='Actions')
        self.library_tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Add a vertical scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(library_label_frame, orient="vertical", command=self.library_tree.yview)
        self.library_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Fetch libraries from the database and populate Treeview
        self.populate_library_tree()

        self.library_tree.bind("<<TreeviewSelect>>", self.on_item_select)

    def populate_library_tree(self):
        libraries = self.fetch_libraries_from_db()
        for library in libraries:
            library_name, version, description = library
            item_id = self.library_tree.insert('', 'end', values=(library_name, version, description))
            self.create_action_buttons(item_id)

    def create_action_buttons(self, item_id):
        edit_button = ttk.Button(self.library_tree, text="Edit", command=lambda: self.edit_library(item_id))
        remove_button = ttk.Button(self.library_tree, text="Remove", command=lambda: self.remove_library(item_id))
        self.library_tree.set(item_id, 'Actions', ' ')
        self.library_tree.tag_bind(item_id, '<Button-1>', lambda event, edit=edit_button, remove=remove_button: self.on_button_click(event, edit, remove))

    def on_item_select(self, event):
        selected_item = self.library_tree.selection()[0]
        self.create_action_buttons(selected_item)

    def on_button_click(self, event, edit_button, remove_button):
        item_id = self.library_tree.selection()[0]
        x, y, width, height = self.library_tree.bbox(item_id, 'Actions')
        edit_button.place(x=x, y=y, width=width//2, height=height)
        remove_button.place(x=x + width//2, y=y, width=width//2, height=height)

    def edit_library(self, item_id):
        item_values = self.library_tree.item(item_id, 'values')
        library_name = item_values[0]
        # Implement the function to edit the library details
        messagebox.showinfo("Edit Library", f"Editing {library_name}")

    def remove_library(self, item_id):
        item_values = self.library_tree.item(item_id, 'values')
        library_name = item_values[0]
        # Implement the function to remove the library
        if messagebox.askyesno("Remove Library", f"Are you sure you want to remove {library_name}?"):
            self.library_tree.delete(item_id)
            self.delete_library_from_db(library_name)

    def fetch_libraries_from_db(self):
        conn = sqlite3.connect('libraries.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, version, description FROM libraries")
        libraries = cursor.fetchall()
        conn.close()
        return libraries

    def delete_library_from_db(self, library_name):
        conn = sqlite3.connect('libraries.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM libraries WHERE name=?", (library_name,))
        conn.commit()
        conn.close()

    def show_pip_command(self, library_name):
        pip_command = f"pip install {library_name}"
        messagebox.showinfo(f"Pip Command for {library_name}", pip_command)

    def open_add_library_form(self):
        AddLibraryForm(self)

    def install_package_dialog(self):
        # Placeholder function to install a package
        messagebox.showinfo("Install Package", "This will open a dialog to install a package.")


    def repository_tab(self, notebook):
        repo_frame = ttk.Frame(notebook)
        notebook.add(repo_frame, text="Repository")

        repo_label_frame = ttk.LabelFrame(repo_frame, text="Repository Management")
        repo_label_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Button(repo_label_frame, text="Create Repository", command=self.create_repository_dialog).pack(pady=5)
        ttk.Button(repo_label_frame, text="Push Repository", command=self.push_repository_dialog).pack(pady=5)
        ttk.Button(repo_label_frame, text="Read Repository Changes", command=self.read_repository_changes_dialog).pack(pady=5)
        ttk.Button(repo_label_frame, text="Commit Changes", command=self.commit_changes_dialog).pack(pady=5)
        ttk.Button(repo_label_frame, text="Generate Tool Report", command=self.generate_tool_report_dialog).pack(pady=5)
    def create_virtual_environment(self):
        env_name = self.env_name_entry.get().strip()
        if not env_name:
            messagebox.showwarning("Input Error", "Please enter a valid environment name.")
            return

        location = filedialog.askdirectory(title="Select Location for Virtual Environment")
        if not location:
            return

        full_path = os.path.join(location, env_name)
        try:
            EnvironmentManager.create_virtual_environment(full_path)
            messagebox.showinfo("Success", f"Virtual environment '{env_name}' created successfully at '{location}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create virtual environment: {e}")

    def create_file_dialog(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            FileManager.create_file(file_path)
            messagebox.showinfo("Success", f"File '{file_path}' created successfully.")

    def create_folder_dialog(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            FileManager.create_folder(folder_path)
            messagebox.showinfo("Success", f"Folder '{folder_path}' created successfully.")

    def delete_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            FileManager.delete_file(file_path)
            messagebox.showinfo("Success", f"File '{file_path}' deleted successfully.")

    def delete_folder_dialog(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            FileManager.delete_folder(folder_path)
            messagebox.showinfo("Success", f"Folder '{folder_path}' deleted successfully.")

    def create_django_project_dialog(self):
        project_name = simpledialog.askstring("Input", "Enter Django project name:")
        if project_name:
            env_path = filedialog.askdirectory(title="Select Virtual Environment Directory")
            if env_path:
                try:
                    DjangoSetup.create_django_project(project_name, env_path)
                    messagebox.showinfo("Success", f"Django project '{project_name}' created successfully at '{env_path}'.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create Django project: {e}")

    def add_django_app_dialog(self):
        project_name = simpledialog.askstring("Input", "Enter Django project name:")
        app_name = simpledialog.askstring("Input", "Enter Django app name:")
        env_path = filedialog.askdirectory(title="Select Virtual Environment Directory")
        if project_name and app_name and env_path:
            try:
                if EnvironmentManager.activate_virtual_environment(env_path):
                    DjangoSetup.add_django_app(project_name, app_name)
                    DjangoSetup.add_app_to_settings(project_name, app_name)
                    messagebox.showinfo("Success", f"Django app '{app_name}' added to project '{project_name}'.")
                else:
                    messagebox.showerror("Error", f"Failed to activate virtual environment for '{env_path}'.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add Django app: {e}")
        else:
            messagebox.showwarning("Input Error", "Please enter project name, app name, and environment path.")

    def install_package_dialog(self):
        try:
            name = simpledialog.askstring("Input", "Enter library name:")
            if not name:
                return

            installation_command = self.tool_db.fetch_library_installation_command(name)
            if not installation_command:
                messagebox.showerror("Error", f"Library '{name}' not found in the database.")
                return

            selected_folder = filedialog.askdirectory(title="Select Virtual Environment Directory")
            if not selected_folder:
                return

            env_path = os.path.abspath(selected_folder)
            if not os.path.exists(os.path.join(env_path, 'Scripts', 'activate')):
                messagebox.showerror("Error", "Selected directory is not a valid virtual environment.")
                return

            PackageInstaller.install_package(installation_command, env_path)
            messagebox.showinfo("Success", f"Library '{name}' installed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install library: {str(e)}")

    def open_add_library_form(self):
        AddLibraryForm(self)

    def create_repository_dialog(self):
        repo_name = simpledialog.askstring("Create Repository", "Enter repository name:")
        if repo_name:
            location = filedialog.askdirectory(title="Select Location for Repository")
            if location:
                try:
                    RepoManager.create_repository(repo_name, location)
                    messagebox.showinfo("Success", f"Repository '{repo_name}' created successfully at '{location}'.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create repository: {e}")

    def push_repository_dialog(self):
        repo_path = filedialog.askdirectory(title="Select Repository Directory")
        if repo_path:
            try:
                RepoManager.push_changes(repo_path)
                messagebox.showinfo("Success", f"Changes pushed successfully to repository at '{repo_path}'.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to push changes: {e}")

    def read_repository_changes_dialog(self):
        repo_path = filedialog.askdirectory(title="Select Repository Directory")
        if repo_path:
            try:
                changes = RepoManager.read_changes(repo_path)
                messagebox.showinfo("Repository Changes", changes)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read repository changes: {e}")

    def commit_changes_dialog(self):
        repo_path = filedialog.askdirectory(title="Select Repository Directory")
        if repo_path:
            commit_message = simpledialog.askstring("Commit Changes", "Enter commit message:")
            if commit_message:
                try:
                    RepoManager.commit_changes(repo_path, commit_message)
                    messagebox.showinfo("Success", f"Changes committed successfully to repository at '{repo_path}'.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to commit changes: {e}")

    def generate_tool_report_dialog(self):
        try:
            data = self.tool_db.fetch_tool_usage_data()
            if not data:
                messagebox.showwarning("No Data", "No tool usage data found.")
                return

            tools = list(data.keys())
            counts = list(data.values())

            # Clear any existing content in the current notebook tab
            current_tab_index = self.notebook.index(self.notebook.select())
            current_tab = self.notebook.nametowidget(self.notebook.tabs()[current_tab_index])

            # Check if there's already a frame for the report, and destroy it if present
            for widget in current_tab.winfo_children():
                if isinstance(widget, ttk.Frame) and widget.winfo_children():
                    widget.destroy()

            # Create a new frame for the report
            report_frame = ttk.Frame(current_tab)
            report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Plotting multiple charts
            fig, axs = plt.subplots(2, 2, figsize=(12, 8))

            # Chart 1: Bar chart
            axs[0, 0].bar(tools, counts, color='skyblue')
            axs[0, 0].set_xlabel('Tool')
            axs[0, 0].set_ylabel('Usage Count')
            axs[0, 0].set_title('Tool Usage Report')

            # Chart 2: Pie chart
            axs[0, 1].pie(counts, labels=tools, autopct='%1.1f%%', shadow=True, startangle=90)
            axs[0, 1].set_title('Tool Usage Distribution')

            # Chart 3: Line chart
            axs[1, 0].plot(tools, counts, marker='o', color='orange')
            axs[1, 0].set_xlabel('Tool')
            axs[1, 0].set_ylabel('Usage Count')
            axs[1, 0].set_title('Tool Usage Trend')

            # Chart 4: Horizontal bar chart
            axs[1, 1].barh(tools, counts, color='green')
            axs[1, 1].set_xlabel('Usage Count')
            axs[1, 1].set_ylabel('Tool')
            axs[1, 1].set_title('Tool Usage Overview')

            # Adjust layout
            plt.tight_layout()

            # Creating a canvas within the report frame
            canvas = FigureCanvasTkAgg(fig, master=report_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate tool report: {e}")


class AddLibraryForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Library")
        self.geometry("400x300")

        ttk.Label(self, text="Library Name:").pack()
        self.entry_name = ttk.Entry(self)
        self.entry_name.pack()

        ttk.Label(self, text="Description:").pack()
        self.entry_description = ttk.Entry(self)
        self.entry_description.pack()

        ttk.Label(self, text="Installation Command:").pack()
        self.entry_installation = ttk.Entry(self)
        self.entry_installation.pack()

        ttk.Label(self, text="Settings Needed:").pack()
        self.entry_settings = ttk.Entry(self)
        self.entry_settings.pack()

        ttk.Label(self, text="Documentation URL:").pack()
        self.entry_documentation = ttk.Entry(self)
        self.entry_documentation.pack()

        ttk.Button(self, text="Save", command=self.save_library).pack()

    def save_library(self):
        name = self.entry_name.get().strip()
        description = self.entry_description.get().strip()
        installation_command = self.entry_installation.get().strip()
        settings = self.entry_settings.get().strip()
        documentation_url = self.entry_documentation.get().strip()

        if name and installation_command:
            # Save library details to SQLite database
            conn = sqlite3.connect('libraries.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO libraries (name, description, installation_command, settings, documentation_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, description, installation_command, settings, documentation_url))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Library '{name}' added successfully.")
            self.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter library name and installation command.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
