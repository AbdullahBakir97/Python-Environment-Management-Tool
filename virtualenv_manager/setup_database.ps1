# Path to SQLite command-line utility (update if necessary)
# $sqlitePath = "C:\Users\B\anaconda3\Library\bin\sqlite3.exe"

# SQLite database file path
$databasePath = "C:\Users\B\Project\P-V.Env-Tool\src\libraries.db"

# Class for connecting and managing SQLite database
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
    documentation_url TEXT,
    version TEXT
);

INSERT INTO libraries (name, description, installation_command, settings, documentation_url, version)
VALUES
    ('Django', 'The core framework for web application development in Python.', 'pip install django', '', 'https://docs.djangoproject.com', '3.2.3'),
    ('Django REST Framework', 'Toolkit for building Web APIs in Django.', 'pip install djangorestframework', '', 'https://www.django-rest-framework.org', '3.12.4'),
    ('Channels', 'Handles WebSockets and other asynchronous protocols in Django.', 'pip install channels', '', 'https://channels.readthedocs.io/en/stable', '3.0.0'),
    ('Celery', 'Distributed task queue for handling asynchronous tasks.', 'pip install celery', '', 'https://docs.celeryproject.org', '5.0.0'),
    ('Whitenoise', 'Simplifies serving static files in production.', 'pip install whitenoise', '', 'http://whitenoise.evans.io/en/stable', '5.3.0')
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

# Main logic to setup the database
$toolDatabase = [ConnectDatabase]::new($databasePath)
try {
    $toolDatabase.SetupDatabase()
    Write-Output "Database setup completed."
} catch {
    Write-Error "Error setting up database: $_"
} finally {
    $toolDatabase.Dispose()
}

# Function to handle database operations# Function to handle database operations
function Invoke-DatabaseOperation {
    param(
        [string]$operation,
        [hashtable]$data
    )

    try {
        $toolDatabase = [ConnectDatabase]::new($databasePath)

        switch ($operation) {
            "add" {
                $query = "INSERT INTO libraries (name, description, installation_command, settings, documentation_url, version) VALUES ('$($data.name)', '$($data.description)', '$($data.installation_command)', '$($data.settings)', '$($data.documentation_url)', '$($data.version)')"
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
                    $settingsJson = $data.settings | ConvertTo-Json -Compress
                    $query = "UPDATE libraries SET settings='$settingsJson' WHERE name='$($data.name)'"
                    $toolDatabase.ExecuteCommand($query)
                }
                if ($data.documentation_url) {
                    $query = "UPDATE libraries SET documentation_url='$($data.documentation_url)' WHERE name='$($data.name)'"
                    $toolDatabase.ExecuteCommand($query)
                }
                if ($data.version) {
                    $query = "UPDATE libraries SET version='$($data.version)' WHERE name='$($data.name)'"
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
            "fetch_by_id" {
                if ($data.id) {
                    $query = "SELECT * FROM libraries WHERE id=$($data.id)"
                    $result = $toolDatabase.ExecuteQuery($query)
                    return $result
                } else {
                    throw "Missing 'id' parameter for fetch_by_id operation."
                }
            }
            "exists" {
                if ($data.name) {
                    $query = "SELECT COUNT(*) FROM libraries WHERE name='$($data.name)'"
                    $result = $toolDatabase.ExecuteQuery($query)
                    return [bool]($result[0][0] -gt 0)
                } else {
                    throw "Missing 'name' parameter for exists operation."
                }
            }
            "fetch_settings" {
                if ($data.name) {
                    $query = "SELECT settings FROM libraries WHERE name='$($data.name)'"
                    $result = $toolDatabase.ExecuteQuery($query)
                    if ($result -and $result[0].ContainsKey('settings')) {
                        return $result[0]['settings'] | ConvertFrom-Json
                    } else {
                        return $null
                    }
                } else {
                    throw "Missing 'name' parameter for fetch_settings operation."
                }
            }
            "update_settings" {
                if ($data.name -and $data.settings) {
                    $settingsJson = $data.settings | ConvertTo-Json -Compress
                    $query = "UPDATE libraries SET settings='$settingsJson' WHERE name='$($data.name)'"
                    $toolDatabase.ExecuteCommand($query)
                } else {
                    throw "Missing 'name' or 'settings' parameter for update_settings operation."
                }
            }
            "update_documentation_url" {
                if ($data.name -and $data.documentation_url) {
                    $query = "UPDATE libraries SET documentation_url='$($data.documentation_url)' WHERE name='$($data.name)'"
                    $toolDatabase.ExecuteCommand($query)
                } else {
                    throw "Missing 'name' or 'documentation_url' parameter for update_documentation_url operation."
                }
            }
            default {
                throw "Unsupported operation: $operation"
            }
        }

    } finally {
        $toolDatabase.Dispose()
    }
}

# Main logic to handle requests with help list
while ($true) {
    Write-Host "Commands and Formats:"
    Write-Host "  add                  - Format: add {'name':'...', 'description':'...', 'installation_command':'...', 'settings':'...', 'documentation_url':'...', 'version':'...'}"
    Write-Host "  update               - Format: update {'name':'...', 'new_name':'...', 'description':'...', 'installation_command':'...', 'settings':'...', 'documentation_url':'...', 'version':'...'}"
    Write-Host "  delete               - Format: delete {'name':'...'}"
    Write-Host "  fetch                - Format: fetch {'name':'...'}"
    Write-Host "  fetch_all            - Format: fetch_all"
    Write-Host "  fetch_installation_command - Format: fetch_installation_command {'name':'...'}"
    Write-Host "  fetch_usage_data     - Format: fetch_usage_data"
    Write-Host "  fetch_by_id          - Format: fetch_by_id {'id':...}"
    Write-Host "  exists               - Format: exists {'name':'...'}"
    Write-Host "  fetch_settings       - Format: fetch_settings {'name':'...'}"
    Write-Host "  update_settings      - Format: update_settings {'name':'...', 'settings':{...}}"
    Write-Host "  update_documentation_url - Format: update_documentation_url {'name':'...', 'documentation_url':'...'}"
    Write-Host "  exit                 - Exit the script"
    
    $request = Read-Host "Enter operation"
    
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