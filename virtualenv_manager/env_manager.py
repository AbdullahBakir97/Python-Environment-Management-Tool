import os
import subprocess
import sys
from typing import Optional

class EnvironmentManager:
    
    @staticmethod
    def create_virtual_environment(env_name: str):
        """
        Create a virtual environment with the specified name.

        Args:
        - env_name (str): Name of the virtual environment.
        """
        try:
            subprocess.check_call([sys.executable, '-m', 'venv', env_name])
            print(f"Virtual environment '{env_name}' created successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to create virtual environment '{env_name}'. {e}")

    @staticmethod
    def activate_virtual_environment(env_path: str) -> None:
        """
        Activate a virtual environment.

        Args:
        - env_path (str): Path to the virtual environment.
        """
        if sys.platform == 'win32' or sys.platform == 'win64':
            activate_script = os.path.join(env_path, 'Scripts', 'activate.bat')
        else:
            activate_script = os.path.join(env_path, 'bin', 'activate')

        try:
            subprocess.run(f'"{activate_script}"', shell=True, check=True)
            print(f"Activated virtual environment at '{env_path}'.")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to activate virtual environment: {e}")
        
# Example usage
if __name__ == "__main__":
    # Example usage of EnvironmentManager methods
    env_name = "my_env"

    EnvironmentManager.create_virtual_environment(env_name)
    EnvironmentManager.activate_virtual_environment(env_name)
