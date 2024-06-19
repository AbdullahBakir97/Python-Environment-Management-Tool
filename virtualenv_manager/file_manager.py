import os
import shutil
from typing import List, Union

class FileManager:
    @staticmethod
    def create_folder(folder_path: str):
        """
        Create a folder at the specified path.

        Args:
        - folder_path (str): Path of the folder to create.
        """
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder '{folder_path}' created successfully.")
        except OSError as e:
            print(f"Error: Failed to create folder '{folder_path}'. {e}")

    @staticmethod
    def delete_folder(folder_path: str):
        """
        Delete a folder and its contents recursively.

        Args:
        - folder_path (str): Path of the folder to delete.
        """
        try:
            shutil.rmtree(folder_path, ignore_errors=True)
            print(f"Folder '{folder_path}' deleted successfully.")
        except OSError as e:
            print(f"Error: Failed to delete folder '{folder_path}'. {e}")

    @staticmethod
    def create_file(file_path: str, content: str = ""):
        """
        Create a file at the specified path with optional content.

        Args:
        - file_path (str): Path of the file to create.
        - content (str, optional): Content to write to the file (default is an empty string).
        """
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            print(f"File '{file_path}' created successfully.")
        except OSError as e:
            print(f"Error: Failed to create file '{file_path}'. {e}")

    @staticmethod
    def delete_file(file_path: str):
        """
        Delete a file at the specified path.

        Args:
        - file_path (str): Path of the file to delete.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File '{file_path}' deleted successfully.")
            else:
                print(f"File '{file_path}' does not exist.")
        except OSError as e:
            print(f"Error: Failed to delete file '{file_path}'. {e}")

    @staticmethod
    def copy_file(source_file: str, destination_file: str):
        """
        Copy a file from source to destination.

        Args:
        - source_file (str): Path of the source file.
        - destination_file (str): Path of the destination file.
        """
        try:
            shutil.copy2(source_file, destination_file)
            print(f"File '{source_file}' copied to '{destination_file}' successfully.")
        except FileNotFoundError as e:
            print(f"Error: File '{source_file}' not found. {e}")
        except shutil.SameFileError:
            print(f"Error: Source and destination file are the same.")
        except OSError as e:
            print(f"Error: Failed to copy file '{source_file}' to '{destination_file}'. {e}")

    @staticmethod
    def move_file(source_file: str, destination_file: str):
        """
        Move (rename) a file from source to destination.

        Args:
        - source_file (str): Path of the source file.
        - destination_file (str): Path of the destination file.
        """
        try:
            shutil.move(source_file, destination_file)
            print(f"File '{source_file}' moved to '{destination_file}' successfully.")
        except FileNotFoundError as e:
            print(f"Error: File '{source_file}' not found. {e}")
        except shutil.Error as e:
            print(f"Error: Failed to move file '{source_file}' to '{destination_file}'. {e}")

    @staticmethod
    def list_files(folder_path: str, file_extensions: Union[str, List[str]] = None) -> List[str]:
        """
        List files in a folder with optional filtering by file extensions.

        Args:
        - folder_path (str): Path of the folder to list files from.
        - file_extensions (str or List[str], optional): File extension(s) to filter by (e.g., '.txt', ['.py', '.html']).

        Returns:
        - List[str]: List of file names in the folder.
        """
        try:
            if file_extensions:
                if isinstance(file_extensions, str):
                    file_extensions = [file_extensions]
                files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(tuple(file_extensions))]
            else:
                files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            
            files.sort()  # Sort files alphabetically
            return files
        except OSError as e:
            print(f"Error: Failed to list files in folder '{folder_path}'. {e}")
            return []

    @staticmethod
    def list_folders(folder_path: str) -> List[str]:
        """
        List subfolders in a folder.

        Args:
        - folder_path (str): Path of the folder to list subfolders from.

        Returns:
        - List[str]: List of subfolder names in the folder.
        """
        try:
            folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            folders.sort()  # Sort folders alphabetically
            return folders
        except OSError as e:
            print(f"Error: Failed to list subfolders in folder '{folder_path}'. {e}")
            return []

# Example usage
if __name__ == "__main__":
    # Example usage of FileManager methods
    folder_path = "test_folder"
    file_path = "test_folder/test_file.txt"
    content = "Hello, this is a test file content."

    FileManager.create_folder(folder_path)
    FileManager.create_file(file_path, content)
    print(FileManager.list_files(folder_path))
    print(FileManager.list_folders("."))

    new_file_path = "test_folder/test_file_new.txt"
    FileManager.copy_file(file_path, new_file_path)
    FileManager.delete_file(file_path)

    new_folder_path = "test_folder_new"
    FileManager.move_file(folder_path, new_folder_path)
    FileManager.delete_folder(new_folder_path)
