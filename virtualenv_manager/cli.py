import argparse
from config.settings import TOOL_SETTINGS, API_URL, DATABASE
from env_manager import EnvironmentManager
from file_manager import FileManager
from package_installer import PackageInstaller
from django_setup import DjangoSetup
from dir_structure import write_directory_structure_to_file as write_local_structure

def main():
    parser = argparse.ArgumentParser(description="Virtual Environment Management Tool")
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    # Sub-command: create_env
    parser_create_env = subparsers.add_parser('create_env', help='Create a virtual environment')
    parser_create_env.add_argument('env_name', type=str, help='Name of the virtual environment')

    # Sub-command: create_folder
    parser_create_folder = subparsers.add_parser('create_folder', help='Create a folder')
    parser_create_folder.add_argument('folder_path', type=str, help='Path of the folder to create')

    # Sub-command: delete_folder
    parser_delete_folder = subparsers.add_parser('delete_folder', help='Delete a folder')
    parser_delete_folder.add_argument('folder_path', type=str, help='Path of the folder to delete')

    # Sub-command: create_file
    parser_create_file = subparsers.add_parser('create_file', help='Create a file')
    parser_create_file.add_argument('file_path', type=str, help='Path of the file to create')
    parser_create_file.add_argument('--content', type=str, default='', help='Content to write to the file')

    # Sub-command: delete_file
    parser_delete_file = subparsers.add_parser('delete_file', help='Delete a file')
    parser_delete_file.add_argument('file_path', type=str, help='Path of the file to delete')

    # Sub-command: install_packages
    parser_install_packages = subparsers.add_parser('install_packages', help='Install packages')
    parser_install_packages.add_argument('packages', nargs='*', default=PackageInstaller.DEFAULT_PACKAGES, help='List of packages to install')

    # Sub-command: create_django_project
    parser_django_project = subparsers.add_parser('create_django_project', help='Create a Django project')
    parser_django_project.add_argument('project_name', type=str, help='Name of the Django project')

    # Sub-command: local_structure
    parser_local_structure = subparsers.add_parser('local_structure', help='Write local directory structure to file')
    parser_local_structure.add_argument('root_dir', type=str, help='Root directory to scan')
    parser_local_structure.add_argument('output_file', type=str, help='Output file to write the structure to')

    # Sub-command: github_structure
    parser_github_structure = subparsers.add_parser('github_structure', help='Write GitHub repository directory structure to file')
    parser_github_structure.add_argument('repo_url', type=str, help='GitHub repository URL')
    parser_github_structure.add_argument('output_file', type=str, help='Output file to write the structure to')
    parser_github_structure.add_argument('--access_token', type=str, help='GitHub access token', default=None)

    args = parser.parse_args()

    try:
        if args.command == 'create_env':
            EnvironmentManager.create_virtual_environment(args.env_name)
        elif args.command == 'create_folder':
            FileManager.create_folder(args.folder_path)
        elif args.command == 'delete_folder':
            FileManager.delete_folder(args.folder_path)
        elif args.command == 'create_file':
            FileManager.create_file(args.file_path, args.content)
        elif args.command == 'delete_file':
            FileManager.delete_file(args.file_path)
        elif args.command == 'install_packages':
            PackageInstaller.install_packages(args.packages)
        elif args.command == 'create_django_project':
            DjangoSetup.create_django_project(args.project_name)
            DjangoSetup.setup_django_settings(args.project_name)
        elif args.command == 'local_structure':
            write_local_structure(args.root_dir, args.output_file)
        elif args.command == 'github_structure':
            owner, repo, path = extract_github_details(args.repo_url)
            structure = fetch_directory_structure_from_github(owner, repo, path, args.access_token)
            write_github_structure(structure, args.output_file)
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
