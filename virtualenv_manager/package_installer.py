import os
import subprocess
import sys
from typing import List
from env_manager import EnvironmentManager
from db_manager import ToolDatabase
from tkinter import filedialog, simpledialog, messagebox

class PackageInstaller:
    DEFAULT_PACKAGES = [
        'requests', 'django', 'djangorestframework', 
        'channels', 'django-celery-beat', 'django-celery-results', 
        'redis', 'whitenoise'
    ]

    @staticmethod
    def install_package(installation_command, env_path=None):
        """
        Install a package/library using pip or another package manager
        """
        try:
            # Execute installation command using subprocess
            subprocess.run([installation_command], cwd=env_path, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Installation failed with error: {e}")


# Example usage
if __name__ == "__main__":
    env_name = "my_env"
    env_path = os.path.join(os.getcwd(), env_name)  # Assuming virtual environment is created in current working directory

    # Create and activate virtual environment
    EnvironmentManager.create_virtual_environment(env_name)
    EnvironmentManager.activate_virtual_environment(env_path)

    # Example usage of PackageInstaller methods
    packages_to_install = ['numpy', 'pandas']  # Example additional packages to install

    for package in packages_to_install:
        PackageInstaller.install_package(env_path, package)

    PackageInstaller.install_default_packages(env_path)

