# Python Environment Management Tool

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-yellow.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

## Overview

The **Python Environment Management Tool** provides a graphical user interface (GUI) for managing Python libraries, virtual environments, and project files. This tool integrates SQLite for library management and supports tasks such as creating virtual environments, managing files, installing libraries, and interacting with Django projects. It aims to streamline the development setup and management process, making it easier for developers to handle their projects efficiently.

## Features

- 📚 **Library Management:**
  - Add, update, fetch, and delete libraries in an SQLite database.
  - Specify installation commands, settings, and documentation URLs for each library.

- 🛠️ **Virtual Environment Management:**
  - Create virtual environments with custom names and locations.
  - Activate virtual environments and install Python packages using pip.

- 🗂️ **File and Project Management:**
  - Create, delete, and manage files and folders directly from the GUI.
  - Support for creating Django projects, adding apps, and managing directory structures.

- ⚙️ **Automated Django Setup:**
  - Create new Django projects within specified virtual environments.
  - Configure Django settings for integration with Whitenoise, Celery, and Channels.
  - Add new Django apps to the project and configure middleware and static file storage settings.

- 🔄 **GitHub Integration:**
  - Clone repositories directly from GitHub into specified directories.

- 🖥️ **GUI Interface:**
  - User-friendly interface built using Tkinter for seamless interaction and ease of use.

## Getting Started

### Prerequisites

- 🐍 Python 3.x installed
- 🖼️ Tkinter library (usually included with Python installations)
- 🗄️ SQLite3
- 🌐 Git (optional for GitHub integration)

### Installation

1. **Clone the repository:**
   
```
   git clone https://github.com/yourusername/python-env-tool.git
   cd python-env-tool
```
2. **Install dependencies:**
   
```
   pip install -r requirements.txt
```

3. **Setup the SQLite database:**
   
```
   python setup_db.py
```

### Usage

1. **Run the application:**

```
    python gui.py
```


### Explore functionalities:

- 🆕 **Create Virtual Environment:** Specify a name and location to create a new virtual environment.
- 📁 **Manage Files and Projects:** Create, delete files/folders, and manage Django projects.
- ➕ **Add Libraries:** Input library details and save them to the database for future reference.
- 📦 **Install Packages:** Select a library and a virtual environment to install it using pip.

### Additional Features:

- 🌀 **GitHub Repository Cloning:** Clone repositories from GitHub and specify the target directory.
- 📝 **Open Directory in VS Code:** Open selected directories directly in VS Code for further development.


## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests for any improvements or additional features you'd like to see.

## License

This project is licensed under the - [MIT License](LICENSE).
