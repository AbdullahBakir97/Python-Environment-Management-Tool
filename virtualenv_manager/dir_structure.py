import os

def generate_directory_structure(root_dir, indent=''):
    structure = []
    items = os.listdir(root_dir)
    items.sort()

    for index, item in enumerate(items):
        full_path = os.path.join(root_dir, item)
        is_last = index == len(items) - 1
        marker = '└── ' if is_last else '├── '
        structure.append(f"{indent}{marker}{item}")

        if os.path.isdir(full_path):
            if is_last:
                structure.extend(generate_directory_structure(full_path, indent + '    '))
            else:
                structure.extend(generate_directory_structure(full_path, indent + '│   '))

    return structure

def write_directory_structure_to_file(root_dir, output_file):
    structure = generate_directory_structure(root_dir)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(structure))

# Example usage
if __name__ == "__main__":
    root_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(root_directory, 'directory_structure.txt')
    write_directory_structure_to_file(root_directory, output_file)
    print(f"Directory structure written to {output_file}")


class DirStructure:
    @staticmethod
    def create_structure(base_path, structure_name, structure=None):
        """
        Create a directory structure at the specified base path.

        Args:
        - base_path (str): The base directory where the structure will be created.
        - structure_name (str): The name of the directory structure.
        - structure (dict, optional): Optional predefined structure dictionary. If None, creates a basic structure.

        Raises:
        - ValueError: If structure_name is empty or base_path is invalid.
        """
        if not structure_name:
            raise ValueError("Structure name cannot be empty.")

        if not os.path.isdir(base_path):
            raise ValueError(f"Invalid base path: '{base_path}' is not a directory.")

        structure = structure or {
            'project': {
                'app': [],
                'config': ['settings.py', 'urls.py'],
                'templates': [],
                'static': []
            },
            'docs': ['README.md'],
            'tests': [],
            'data': []
        }

        base_dir = os.path.join(base_path, structure_name)
        os.makedirs(base_dir, exist_ok=True)

        for folder, files in structure.items():
            folder_path = os.path.join(base_dir, folder)
            os.makedirs(folder_path, exist_ok=True)
            for file in files:
                if isinstance(file, str):
                    file_path = os.path.join(folder_path, file)
                    with open(file_path, 'w') as f:
                        f.write('')
                else:
                    os.makedirs(os.path.join(folder_path, file), exist_ok=True)

    # Add more methods as needed (e.g., validating structure, handling variations, etc.)