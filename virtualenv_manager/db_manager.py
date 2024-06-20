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
    
    
    # def fetch_tool_usage_data(self):
    #     """
    #     Fetch tool usage data from the SQLite database
    #     """
    #     usage_query = """
    #         SELECT name, COUNT(*) AS usage_count
    #         FROM libraries
    #         GROUP BY name
    #     """
    #     self.cursor.execute(usage_query)
    #     rows = self.cursor.fetchall()
    #     if not rows:
    #         return {}
    #     tool_usage_data = {name: count for name, count in rows}
    #     return tool_usage_data

    # def _execute_query(self, query, params=None, fetchone=False):
    #     if params is None:
    #         params = ()
    #     self.cursor.execute(query, params)
    #     if fetchone:
    #         return self.cursor.fetchone()
    #     else:
    #         return self.cursor.fetchall()

    # def create_tables(self):
    #     create_query = """
    #         CREATE TABLE IF NOT EXISTS libraries (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             name TEXT UNIQUE NOT NULL,
    #             description TEXT,
    #             installation_command TEXT NOT NULL,
    #             settings TEXT,
    #             documentation_url TEXT
    #         )
    #     """
    #     self._execute_query(create_query)

    def add_library(self, name, description, installation_command, settings=None, documentation_url=None):
        data = {
            "name": name,
            "description": description,
            "installation_command": installation_command,
            "settings": settings,
            "documentation_url": documentation_url
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
        data = {"name": name, "settings": settings}
        return self._run_ps_script("update", data)

    def update_library_documentation_url(self, name, documentation_url):
        data = {"name": name, "documentation_url": documentation_url}
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
        
        


# Example usage
if __name__ == "__main__":
    # Create an instance of ToolDatabase
    tool_db = ToolDatabase('libraries.db')

    # Example add library to database
    tool_db.add_library("Django", "The core framework for web application development in Python.", "pip install django", "{'version': '3.2.5'}", "https://docs.djangoproject.com")

    # Example get library
    library = tool_db.get_library("Django")
    print(f"Library details: {library}")

    # Example update library fields
    tool_db.update_library_description("Django", "A high-level Python web framework")
    tool_db.update_library_installation_command("Django", "pip install django==4.0.0")
    tool_db.update_library_settings("Django", "{'version': '4.0.0'}")
    tool_db.update_library_documentation_url("Django", "https://docs.djangoproject.com/4.0/")