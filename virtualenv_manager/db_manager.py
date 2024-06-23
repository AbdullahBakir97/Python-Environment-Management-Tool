import os
import sqlite3
import subprocess
import json
from sqlite3 import Error as SQLiteError

# SQLite database file path
DB_FILE = 'C:/Users/B/Project/P-V.Env-Tool/src/virtualenv_manager/libraries.db'

class ToolDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
    def _run_ps_script(self, operation, data):
        script = f"powershell.exe -File setup_database.ps1"
        request = f"{operation} {json.dumps(data)}"
        result = subprocess.run(script, input=request, text=True, capture_output=True, shell=True)
        return result.stdout.strip()

    def add_library(self, name, description, installation_command, settings=None, documentation_url=None, version=None):
        data = {
            "name": name,
            "description": description,
            "installation_command": installation_command,
            "settings": json.dumps(settings) if settings else None,
            "documentation_url": documentation_url,
            "version": version
        }
        return self._run_ps_script("add", data)

    def update_library_name(self, current_name, new_name):
        data = {"current_name": current_name, "new_name": new_name}
        return self._run_ps_script("update", data)

    def update_library_description(self, name, description):
        data = {"name": name, "description": description}
        return self._run_ps_script("update", data)

    def update_library_installation_command(self, name, installation_command):
        data = {"name": name, "installation_command": installation_command}
        return self._run_ps_script("update", data)

    def update_library_settings(self, name, settings):
        data = {"name": name, "settings": json.dumps(settings)}
        return self._run_ps_script("update", data)

    def update_library_documentation_url(self, name, documentation_url):
        data = {"name": name, "documentation_url": documentation_url}
        return self._run_ps_script("update", data)

    def update_library_version(self, name, version):
        data = {"name": name, "version": version}
        return self._run_ps_script("update", data)

    def get_library(self, name):
        data = {"name": name}
        result = self._run_ps_script("fetch", data)
        return json.loads(result)

    def delete_library(self, name):
        data = {"name": name}
        return self._run_ps_script("delete", data)

    def fetch_all_libraries(self):
        result = self._run_ps_script("fetch_all", {})
        return json.loads(result)

    def fetch_library_installation_command(self, name):
        data = {"name": name}
        result = self._run_ps_script("fetch_installation_command", data)
        return result

    def fetch_tool_usage_data(self):
        result = self._run_ps_script("fetch_usage_data", {})
        return json.loads(result)
    
    def fetch_by_id(self, id):
        data = {"id": id}
        result = self._run_ps_script("fetch_by_id", data)
        return json.loads(result)