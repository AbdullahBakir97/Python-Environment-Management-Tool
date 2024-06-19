import requests
import subprocess
import shutil
import os

class RepoManager:
    # GitHub API endpoint for repository contents
    github_api_url = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    @staticmethod
    def extract_github_details(repo_url):
        """
        Extract owner, repo name, and optional path from GitHub repository URL.

        Args:
        - repo_url (str): GitHub repository URL (e.g., https://github.com/owner/repo).

        Returns:
        - tuple: (owner, repo, path)
        """
        parts = repo_url.rstrip('/').split('/')
        owner = parts[3]
        repo = parts[4]
        path = '/'.join(parts[6:]) if len(parts) > 6 else ''
        return owner, repo, path
    
    @staticmethod
    def fetch_directory_structure_from_github(owner, repo, path='', access_token=None, indent=''):
        """
        Fetch directory structure of a GitHub repository recursively.

        Args:
        - owner (str): GitHub repository owner.
        - repo (str): GitHub repository name.
        - path (str, optional): Path within the repository (default is '').
        - access_token (str, optional): GitHub access token for authentication.
        - indent (str, optional): Indentation string for visual hierarchy (default is '').

        Returns:
        - list: List of strings representing the directory structure.

        Raises:
        - ValueError: If the GitHub API request fails or returns an error.
        """
        headers = {}
        if access_token:
            headers['Authorization'] = f"token {access_token}"

        url = RepoManager.github_api_url.format(owner=owner, repo=repo, path=path)
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            contents = response.json()
            structure = []

            contents.sort(key=lambda x: (x['type'], x['name']))

            for index, item in enumerate(contents):
                is_last = index == len(contents) - 1
                prefix = '└── ' if is_last else '├── '

                if item['type'] == 'dir':
                    structure.append(f"{indent}{prefix}{item['name']}/")
                    structure.extend(RepoManager.fetch_directory_structure_from_github(owner, repo, item['path'], access_token, indent + '│   '))
                elif item['type'] == 'file':
                    structure.append(f"{indent}{prefix}{item['name']}")

            return structure
        else:
            raise ValueError(f"Failed to fetch directory structure: {response.status_code} - {response.json().get('message', 'Unknown error')}")
        
    @staticmethod    
    def write_directory_structure_to_file(structure, output_file):
        """
        Write directory structure to a text file.

        Args:
        - structure (list): List of strings representing directory structure.
        - output_file (str): File path to write the structure.

        Raises:
        - IOError: If writing to file fails.
        """
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("\n".join(structure))

    @staticmethod
    def clone_repository(repo_url, destination_path):
        """
        Clone a Git repository from the provided URL to the specified destination path.

        Args:
        - repo_url (str): The URL of the repository to clone.
        - destination_path (str): The local path where the repository should be cloned.

        Raises:
        - RuntimeError: If the cloning process fails.
        """
        try:
            subprocess.check_call(['git', 'clone', repo_url, destination_path])
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to clone repository: {e}")

    @staticmethod
    def create_repository_with_initial_commit(repo_name, base_path, environment_path=None):
        """
        Create a new Git repository with an initial commit.

        Args:
        - repo_name (str): The name of the repository to create.
        - base_path (str): The base directory where the repository will be created.
        - environment_path (str, optional): Path to the virtual environment used for initial commit.

        Raises:
        - RuntimeError: If the repository creation or initial commit fails.
        """
        repo_path = os.path.join(base_path, repo_name)
        try:
            os.makedirs(repo_path, exist_ok=True)
            subprocess.check_call(['git', 'init'], cwd=repo_path)
            
            if environment_path and os.path.exists(environment_path):
                shutil.copytree(environment_path, os.path.join(repo_path, 'env'))
                subprocess.check_call(['git', 'add', 'env'], cwd=repo_path)

            with open(os.path.join(repo_path, 'README.md'), 'w') as readme:
                readme.write(f"# {repo_name}\n\nInitial commit.")

            subprocess.check_call(['git', 'add', 'README.md'], cwd=repo_path)
            subprocess.check_call(['git', 'commit', '-m', 'Initial commit'], cwd=repo_path)

        except subprocess.CalledProcessError as e:
            shutil.rmtree(repo_path, ignore_errors=True)
            raise RuntimeError(f"Failed to create repository: {e}")

    @staticmethod
    def push_repository(repo_path, remote_name='origin', branch='master'):
        """
        Push changes from a local repository to a remote repository.

        Args:
        - repo_path (str): The local path of the repository to push.
        - remote_name (str): Name of the remote repository (default is 'origin').
        - branch (str): Name of the branch to push (default is 'master').

        Raises:
        - RuntimeError: If the push operation fails.
        """
        try:
            subprocess.check_call(['git', 'push', remote_name, branch], cwd=repo_path)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to push repository: {e}")

    @staticmethod
    def read_repository_changes(repo_path):
        """
        Read changes in a local repository compared to its remote counterpart.

        Args:
        - repo_path (str): The local path of the repository.

        Returns:
        - str: The output of the git status command.

        Raises:
        - RuntimeError: If reading changes fails.
        """
        try:
            result = subprocess.run(['git', 'status'], cwd=repo_path, capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to read repository changes: {e}")

    @staticmethod
    def commit_changes(repo_path, message):
        """
        Stage and commit changes in a local repository.

        Args:
        - repo_path (str): The local path of the repository.
        - message (str): The commit message.

        Raises:
        - RuntimeError: If staging or committing changes fails.
        """
        try:
            subprocess.check_call(['git', 'add', '.'], cwd=repo_path)
            subprocess.check_call(['git', 'commit', '-m', message], cwd=repo_path)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to commit changes: {e}")

    @staticmethod
    def generate_tool_report(base_dir):
        """
        Generate a report of all virtual environments, projects, and apps managed by the tool.

        Args:
        - base_dir (str): The base directory where the tool operates.

        Returns:
        - str: The generated report as a string.

        Raises:
        - RuntimeError: If generating the report fails.
        """
        try:
            report = []
            venv_dirs = [dir for dir in os.listdir(base_dir) if dir.startswith('venv')]
            for venv_dir in venv_dirs:
                report.append(f"Virtual Environment: {venv_dir}")
                projects = [project for project in os.listdir(os.path.join(base_dir, venv_dir)) if project.startswith('project')]
                for project in projects:
                    report.append(f"\tProject: {project}")
                    apps = [app for app in os.listdir(os.path.join(base_dir, venv_dir, project)) if os.path.isdir(os.path.join(base_dir, venv_dir, project, app))]
                    for app in apps:
                        report.append(f"\t\tApp: {app}")
                report.append("")
            
            return "\n".join(report)
        except Exception as e:
            raise RuntimeError(f"Failed to generate tool report: {e}")
