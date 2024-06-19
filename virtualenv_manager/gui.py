import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from config.settings import TOOL_SETTINGS
from env_manager import EnvironmentManager
from file_manager import FileManager
from package_installer import PackageInstaller
from django_setup import DjangoSetup
from github_manager import RepoManager
from dir_structure import DirStructure
from db_manager import ToolDatabase
import sqlite3
import os
import subprocess


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.tool_db = ToolDatabase(db_path="./libraries.db")
        
    def create_widgets(self):
        # Create Virtual Environment Section
        self.create_env_label = tk.Label(self, text="Create Virtual Environment")
        self.create_env_label.pack()
        
        self.env_name_entry = tk.Entry(self)
        self.env_name_entry.pack()
        
        self.create_env_button = tk.Button(self, text="Create", command=self.create_virtual_environment)
        self.create_env_button.pack()
        
        # Manage Files and Projects Section
        self.file_project_label = tk.Label(self, text="Manage Files and Projects")
        self.file_project_label.pack()

        self.create_file_button = tk.Button(self, text="Create File", command=self.create_file_dialog)
        self.create_file_button.pack()

        self.create_folder_button = tk.Button(self, text="Create Folder", command=self.create_folder_dialog)
        self.create_folder_button.pack()

        self.delete_file_button = tk.Button(self, text="Delete File", command=self.delete_file_dialog)
        self.delete_file_button.pack()

        self.delete_folder_button = tk.Button(self, text="Delete Folder", command=self.delete_folder_dialog)
        self.delete_folder_button.pack()

        self.create_django_project_button = tk.Button(self, text="Create Django Project", command=self.create_django_project_dialog)
        self.create_django_project_button.pack()
        
        # Add Django App Section
        self.add_app_label = tk.Label(self, text="Add Django App")
        self.add_app_label.pack()

        self.add_app_name_entry = tk.Entry(self)
        self.add_app_name_entry.pack()

        self.env_path_label = tk.Label(self, text="Environment Path")
        self.env_path_label.pack()

        self.env_path_entry = tk.Entry(self)
        self.env_path_entry.pack()

        self.add_app_button = tk.Button(self, text="Add App", command=self.add_django_app_dialog)
        self.add_app_button.pack()
        
        # Add Library Section
        self.add_library_label = tk.Label(self, text="Add Libraries")
        self.add_library_label.pack()

        self.add_library_button = tk.Button(self, text="Add Library", command=self.open_add_library_form)
        self.add_library_button.pack()
        
        # Create Directory Structure Section
        self.create_structure_label = tk.Label(self, text="Create Directory Structure")
        self.create_structure_label.pack()

        self.structure_name_entry = tk.Entry(self)
        self.structure_name_entry.pack()

        self.create_structure_button = tk.Button(self, text="Create Structure", command=self.create_structure_dialog)
        self.create_structure_button.pack()
        
        # Clone Repository Section
        self.clone_repo_label = tk.Label(self, text="Clone GitHub Repository")
        self.clone_repo_label.pack()

        self.repo_url_entry = tk.Entry(self)
        self.repo_url_entry.pack()

        self.clone_repo_button = tk.Button(self, text="Clone Repository", command=self.clone_repo_dialog)
        self.clone_repo_button.pack()
        
        # Open Directory in VS Code Section
        self.open_with_vscode_label = tk.Label(self, text="Open Directory in VS Code")
        self.open_with_vscode_label.pack()
        
        self.open_with_vscode_button = tk.Button(self, text="Open in VS Code", command=self.open_directory_in_vscode)
        self.open_with_vscode_button.pack()
        
        # Install Package Section
        self.install_package_label = tk.Label(self, text="Install Package")
        self.install_package_label.pack()
        

        self.install_package_button = tk.Button(self, text="Install Package", command=self.install_package_dialog)
        self.install_package_button.pack()

        # Quit Button
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack()
        
    def open_add_library_form(self):
        add_library_form = AddLibraryForm(self.master)

    def _select_directory_dialog(self, title):
        """Show directory selection dialog and return selected path."""
        return filedialog.askdirectory(title=title)

    def create_virtual_environment(self):
        """Create a new virtual environment based on user input."""
        env_name = self.env_name_entry.get().strip()
        if not env_name:
            messagebox.showwarning("Input Error", "Please enter a valid environment name.")
            return
        
        location = self._select_directory_dialog("Select Location for Virtual Environment")
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
        project_name = simpledialog.askstring("Input", "Enter Django project name:", parent=self.master)
        if project_name:
            env_path = filedialog.askdirectory(title="Select Virtual Environment Directory")
            if env_path:
                try:
                    # Assuming DjangoSetup is correctly implemented
                    if EnvironmentManager.activate_virtual_environment(env_path):
                        DjangoSetup.create_django_project(project_name, env_path)
                        DjangoSetup.setup_django_settings(project_name)
                        messagebox.showinfo("Success", f"Django project '{project_name}' created and configured successfully in '{env_path}'.")
                    else:
                        messagebox.showerror("Error", f"Failed to activate virtual environment for '{env_path}'.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create Django project: {e}")

    def add_django_app_dialog(self):
        project_name = simpledialog.askstring("Input", "Enter Django project name:", parent=self.master)
        app_name = self.add_app_name_entry.get().strip()
        env_path = self.env_path_entry.get().strip()

        if project_name and app_name and env_path:
            try:
                # Check if virtual environment can be activated
                activation_command = EnvironmentManager.activate_virtual_environment(env_path)
                if activation_command:
                    # Add Django app to the project
                    DjangoSetup.add_django_app(project_name, app_name)
                    DjangoSetup.add_app_to_settings(project_name, app_name)  # Optionally add to settings.py
                    messagebox.showinfo("Success", f"Django app '{app_name}' added to project '{project_name}'.")
                else:
                    messagebox.showerror("Error", f"Failed to activate virtual environment for '{env_path}'.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add Django app: {e}")
        else:
            messagebox.showwarning("Input Error", "Please enter project name, app name, and environment path.")
            
    def clone_repo_dialog(self):
        repo_url = simpledialog.askstring("Input", "Enter repository URL:", parent=self.master)
        if repo_url:
            clone_path = filedialog.askdirectory(title="Select Location to Clone Repository")
            if clone_path:
                try:
                    RepoManager.clone_repository(repo_url, clone_path)
                    messagebox.showinfo("Success", f"Repository cloned successfully to '{clone_path}'.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def create_structure_dialog(self):
        structure_name = simpledialog.askstring("Input", "Enter directory structure name:", parent=self.master)
        if structure_name:
            base_path = filedialog.askdirectory(title="Select Base Directory for Structure")
            if base_path:
                try:
                    DirStructure.create_structure(base_path, structure_name)
                    messagebox.showinfo("Success", f"Directory structure '{structure_name}' created successfully at '{base_path}'.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def install_package_dialog(self):
        try:
            # Input dialog to get library name
            name = simpledialog.askstring("Input", "Enter library name:", parent=self.master)
            if not name:
                return

            # Fetch installation command from database using the library name
            installation_command = self.tool_db.fetch_library_installation_command(name)
            if not installation_command:
                messagebox.showerror("Error", f"Library '{name}' not found in the database.")
                return

            # Select virtual environment directory
            selected_folder = filedialog.askdirectory(title="Select Virtual Environment Directory")
            if not selected_folder:
                return

            env_path = os.path.abspath(selected_folder)
            if not os.path.exists(os.path.join(env_path, 'Scripts', 'activate')):
                messagebox.showerror("Error", "Selected directory is not a valid virtual environment.")
                return

            # Install the library in the virtual environment
            PackageInstaller.install_package(installation_command, env_path)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to install library: {str(e)}")

                
    def install_library_dialog():
        library_name = simpledialog.askstring("Input", "Enter library name:", parent=None)
        if library_name:
            selected_folder = filedialog.askdirectory(title="Select Virtual Environment Directory")
            if selected_folder:
                try:
                    env_path = os.path.abspath(selected_folder)
                    if not os.path.exists(os.path.join(env_path, 'Scripts', 'activate')):
                        messagebox.showerror("Error", "Selected directory is not a valid virtual environment.")
                        return

                    # Install the library in the selected virtual environment
                    PackageInstaller.install_library(env_path, library_name)

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to install library: {str(e)}")

    def open_directory_in_vscode(self):
        directory_path = filedialog.askdirectory(title="Select Directory to Open in VS Code")
        if directory_path:
            try:
                # Change the path based on your operating system and installation path
                if os.name == 'nt':  # Windows
                    vscode_path = r"C:\Users\B\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd"
                elif os.name == 'posix':  # macOS and Linux
                    vscode_path = "/usr/local/bin/code"  # Adjust if necessary
                else:
                    raise Exception("Unsupported OS")

                # Check if the file exists
                if not os.path.exists(vscode_path):
                    raise FileNotFoundError(f"VS Code executable not found at {vscode_path}")

                # Use code.cmd instead of code.exe to avoid permission issues on Windows
                subprocess.run([vscode_path, directory_path], check=True)
                messagebox.showinfo("Success", f"Directory '{directory_path}' opened in VS Code.")
            except FileNotFoundError as e:
                messagebox.showerror("Error", f"File not found: {e}")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Subprocess error: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open directory in VS Code: {e}")

                
class AddLibraryForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Library")
        self.geometry("400x300")
        
        self.label_name = tk.Label(self, text="Library Name:")
        self.label_name.pack()
        self.entry_name = tk.Entry(self)
        self.entry_name.pack()

        self.label_description = tk.Label(self, text="Description:")
        self.label_description.pack()
        self.entry_description = tk.Entry(self)
        self.entry_description.pack()

        self.label_installation = tk.Label(self, text="Installation Command:")
        self.label_installation.pack()
        self.entry_installation = tk.Entry(self)
        self.entry_installation.pack()
        
        self.label_settings = tk.Label(self, text="Settings Needed:")
        self.label_settings.pack()
        self.entry_settings = tk.Entry(self)
        self.entry_settings.pack()

        self.label_documentation = tk.Label(self, text="Documentation URL:")
        self.label_documentation.pack()
        self.entry_documentation = tk.Entry(self)
        self.entry_documentation.pack()

        self.save_button = tk.Button(self, text="Save", command=self.save_library)
        self.save_button.pack()

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


root = tk.Tk()
app = Application(master=root)
app.mainloop()
