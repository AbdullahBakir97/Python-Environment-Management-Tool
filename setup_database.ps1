# Path to SQLite command-line utility (update if necessary)
$sqlitePath = "C:\Users\B\anaconda3\Library\bin\sqlite3.exe"

# SQLite database file path
$databasePath = "C:\Users\B\Project\P-V.Env-Tool\src\libraries.db"

# SQLite commands to be executed
$sqliteCommands = @"
-- Create database and connect
.open '$databasePath'

-- Create libraries table
CREATE TABLE IF NOT EXISTS libraries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    installation_command TEXT,
    settings TEXT,
    documentation_url TEXT
);

-- Insert sample data
INSERT INTO libraries (name, description, installation_command, settings, documentation_url)
VALUES
    ('Django', 'The core framework for web application development in Python.', 'pip install django', '', 'https://docs.djangoproject.com'),
    ('Django REST Framework', 'Toolkit for building Web APIs in Django.', 'pip install djangorestframework', '', 'https://www.django-rest-framework.org'),
    ('Channels', 'Handles WebSockets and other asynchronous protocols in Django.', 'pip install channels', '', 'https://channels.readthedocs.io/en/stable'),
    ('Celery', 'Distributed task queue for handling asynchronous tasks.', 'pip install celery', '', 'https://docs.celeryproject.org'),
    ('Whitenoise', 'Simplifies serving static files in production.', 'pip install whitenoise', '', 'http://whitenoise.evans.io/en/stable')
;

-- Display tables to verify
.tables

-- Exit SQLite
.quit
"@

# Save SQLite commands to a temporary script file
$sqliteScriptFile = "sqlite_commands.sql"
$sqliteCommands | Set-Content -Path $sqliteScriptFile

# Execute SQLite commands using SQLite command-line utility
& $sqlitePath ".read $sqliteScriptFile"

# Remove the temporary script file
Remove-Item $sqliteScriptFile

# Output a message indicating successful execution
Write-Output "SQLite database setup completed successfully."

