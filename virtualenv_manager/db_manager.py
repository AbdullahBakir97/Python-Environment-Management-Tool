import os
import sqlite3
import subprocess
from sqlite3 import Error as SQLiteError

# SQLite database file path
DB_FILE = 'C:/Users/B/Project/P-V.Env-Tool/src/virtualenv_manager/libraries.db'

class ToolDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    
            
    @staticmethod
    def setup():
        """
        Setup the database by creating necessary tables
        """
        db_path = 'C:/Users/B/Project/P-V.Env-Tool/src/virtualenv_manager/libraries.db'
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        create_query = """
            CREATE TABLE IF NOT EXISTS libraries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                installation_command TEXT NOT NULL,
                settings TEXT,
                documentation_url TEXT
            )
        """
        cursor.execute(create_query)
        
         
    
    
    def fetch_tool_usage_data(self):
        """
        Fetch tool usage data from the SQLite database
        """
        usage_query = """
            SELECT name, COUNT(*) AS usage_count
            FROM libraries
            GROUP BY name
        """
        self.cursor.execute(usage_query)
        rows = self.cursor.fetchall()
        if not rows:
            return {}
        tool_usage_data = {name: count for name, count in rows}
        return tool_usage_data

    def _execute_query(self, query, params=None, fetchone=False):
        """
        Execute a SQL query with optional parameters and fetch results if specified
        """
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        if fetchone:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()
 
    
    
    def create_tables(self):
        """
        Create necessary tables in the database if they don't exist
        """
        create_query = """
            CREATE TABLE IF NOT EXISTS libraries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                installation_command TEXT NOT NULL,
                settings TEXT,
                documentation_url TEXT
            )
        """
        self._execute_query(create_query)
        

    def add_library(self, name, description, installation_command, settings=None, documentation_url=None):
        """
        Add a library to the SQLite database
        """
        insert_query = """
            INSERT INTO libraries (name, description, installation_command, settings, documentation_url)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (name, description, installation_command, settings, documentation_url)
        self._execute_query(insert_query, params)
        

    def update_library_name(self, current_name, new_name):
        """
        Update the name of a library in the SQLite database
        """
        update_query = """
            UPDATE libraries SET name=? WHERE name=?
        """
        params = (new_name, current_name)
        self._execute_query(update_query, params)
        

    def update_library_description(self, name, description):
        """
        Update the description of a library in the SQLite database
        """
        update_query = """
            UPDATE libraries SET description=? WHERE name=?
        """
        params = (description, name)
        self._execute_query(update_query, params)
        

    def update_library_installation_command(self, name, installation_command):
        """
        Update the installation command of a library in the SQLite database
        """
        update_query = """
            UPDATE libraries SET installation_command=? WHERE name=?
        """
        params = (installation_command, name)
        self._execute_query(update_query, params)
        

    def update_library_settings(self, name, settings):
        """
        Update the settings of a library in the SQLite database
        """
        update_query = """
            UPDATE libraries SET settings=? WHERE name=?
        """
        params = (settings, name)
        self._execute_query(update_query, params)
        

    def update_library_documentation_url(self, name, documentation_url):
        """
        Update the documentation URL of a library in the SQLite database
        """
        update_query = """
            UPDATE libraries SET documentation_url=? WHERE name=?
        """
        params = (documentation_url, name)
        self._execute_query(update_query, params)
        

    def get_library(self, name):
        """
        Retrieve a library from the SQLite database
        """
        select_query = """
            SELECT * FROM libraries WHERE name=?
        """
        row = self._execute_query(select_query, (name,), fetchone=True)
        if row:
            return row
        else:
            raise ValueError(f"Library '{name}' not found in the database.")
        

    def delete_library(self, name):
        """
        Delete a library from the SQLite database
        """
        delete_query = """
            DELETE FROM libraries WHERE name=?
        """
        self._execute_query(delete_query, (name,))
        

    def fetch_library_installation_command(self, name):
        """
        Retrieve the installation command of a library from the SQLite database
        """
        select_query = "SELECT installation_command FROM libraries WHERE name=?"
        row = self._execute_query(select_query, (name,), fetchone=True)
        if row:
            return row[0]
        else:
            raise ValueError(f"Library '{name}' not found in the database.")
        
        


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