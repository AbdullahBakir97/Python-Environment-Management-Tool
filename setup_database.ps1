# Path to SQLite command-line utility (update if necessary)
# $sqlitePath = "C:\Users\B\anaconda3\Library\bin\sqlite3.exe"

# SQLite database file path
$databasePath = "C:\Users\B\Project\P-V.Env-Tool\src\libraries.db"

class ConnectDatabase {
    ConnectDatabase([string]$dbPath) {
        $this.dbPath = $dbPath
        $this.connection = New-Object -TypeName System.Data.SQLite.SQLiteConnection("Data Source=$dbPath;Version=3;")
        $this.connection.Open()
        $this.command = $this.connection.CreateCommand()
    }

    [void] ExecuteCommand([string]$commandText) {
        $this.command.CommandText = $commandText
        $this.command.ExecuteNonQuery()
    }

    [object[]] ExecuteQuery([string]$queryText) {
        $this.command.CommandText = $queryText
        $result = $this.command.ExecuteReader()
        $output = @()
        while ($result.Read()) {
            $row = @{}
            for ($i = 0; $i -lt $result.FieldCount; $i++) {
                $row[$result.GetName($i)] = $result.GetValue($i)
            }
            $output += $row
        }
        $result.Close()
        return $output
    }

    [void] SetupDatabase() {
        $commands = @"
CREATE TABLE IF NOT EXISTS libraries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    installation_command TEXT NOT NULL,
    settings TEXT,
    documentation_url TEXT
);

INSERT INTO libraries (name, description, installation_command, settings, documentation_url)
VALUES
    ('Django', 'The core framework for web application development in Python.', 'pip install django', '', 'https://docs.djangoproject.com'),
    ('Django REST Framework', 'Toolkit for building Web APIs in Django.', 'pip install djangorestframework', '', 'https://www.django-rest-framework.org'),
    ('Channels', 'Handles WebSockets and other asynchronous protocols in Django.', 'pip install channels', '', 'https://channels.readthedocs.io/en/stable'),
    ('Celery', 'Distributed task queue for handling asynchronous tasks.', 'pip install celery', '', 'https://docs.celeryproject.org'),
    ('Whitenoise', 'Simplifies serving static files in production.', 'pip install whitenoise', '', 'http://whitenoise.evans.io/en/stable')
;
"@

        $commands -split '\r?\n' | ForEach-Object {
            if ($_ -match '\S') {
                $this.ExecuteCommand($_)
            }
        }
    }

    [void] Dispose() {
        $this.connection.Dispose()
    }
}

# Function to handle database operations
function Invoke-DatabaseOperation {
    param(
        [string]$operation,
        [hashtable]$data
    )

    try {
        $toolDatabase = [ConnectDatabase]::new($databasePath)

        switch ($operation) {
            "add" {
                $query = "INSERT INTO libraries (name, description, installation_command, settings, documentation_url) VALUES ('$($data.name)', '$($data.description)', '$($data.installation_command)', '$($data.settings)', '$($data.documentation_url)')"
                $toolDatabase.ExecuteCommand($query)
            }
            "update" {
                if ($data.new_name) {
                    $query = "UPDATE libraries SET name='$($data.new_name)' WHERE name='$($data.current_name)'"
                    $toolDatabase.ExecuteCommand($query)
                }
                if ($data.description) {
                    $query = "UPDATE libraries SET description='$($data.description)' WHERE name='$($data.name)'"
                    $toolDatabase.ExecuteCommand($query)
                }
                if ($data.installation_command) {
                    $query = "UPDATE libraries SET installation_command='$($data.installation_command)' WHERE name='$($data.name)'"
                    $toolDatabase.ExecuteCommand($query)
                }
                if ($data.settings) {
                    $query = "UPDATE libraries SET settings='$($data.settings)' WHERE name='$($data.name)'"
                    $toolDatabase.ExecuteCommand($query)
                }
                if ($data.documentation_url) {
                    $query = "UPDATE libraries SET documentation_url='$($data.documentation_url)' WHERE name='$($data.name)'"
                    $toolDatabase.ExecuteCommand($query)
                }
            }
            "delete" {
                $query = "DELETE FROM libraries WHERE name='$($data.name)'"
                $toolDatabase.ExecuteCommand($query)
            }
            "fetch" {
                $query = "SELECT * FROM libraries WHERE name='$($data.name)'"
                $result = $toolDatabase.ExecuteQuery($query)
                return $result
            }
            "fetch_all" {
                $query = "SELECT * FROM libraries"
                $result = $toolDatabase.ExecuteQuery($query)
                return $result
            }
            "fetch_installation_command" {
                $query = "SELECT installation_command FROM libraries WHERE name='$($data.name)'"
                $result = $toolDatabase.ExecuteQuery($query)
                return $result[0]['installation_command']
            }
            "fetch_usage_data" {
                $query = "SELECT name, COUNT(*) AS usage_count FROM libraries GROUP BY name"
                $result = $toolDatabase.ExecuteQuery($query)
                return $result
            }
            default {
                throw "Unsupported operation: $operation"
            }
        }

    } finally {
        $toolDatabase.Dispose()
    }
}

# Main logic to handle requests
while ($true) {
    $request = Read-Host "Enter operation (or 'exit' to quit)"
    if ($request -eq "exit") {
        break
    }
    
    $operation, $dataJson = $request -split " ", 2
    $data = $dataJson | ConvertFrom-Json
    
    try {
        $result = Invoke-DatabaseOperation -operation $operation -data $data
        if ($result) {
            $result | ConvertTo-Json
        }
        else {
            "Operation '$operation' completed successfully."
        }
    } catch {
        $_.Exception.Message
    }
}
