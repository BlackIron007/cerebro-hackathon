import os
import git
from pathlib import Path

CODE_EXTENSIONS = [
    '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.scss',
    '.java', '.go', '.php', '.rb', '.rs', '.swift', '.kt', '.c', '.cpp', '.h', '.hpp',
    '.md', '.json', '.yml', '.yaml', '.toml'
]

def load_repo(repo_url: str) -> list[tuple[str, str]]:
    """
    Clones a public GitHub repository to a local directory and reads the content
    of all relevant code and text files.

    Args:
        repo_url: The URL of the public GitHub repository to clone.

    Returns:
        A list of tuples, where each tuple contains the file path and its content.
        Example: [('src/main.py', 'print("hello")'), ...]
    """
    try:
        temp_dir = "temp_repo"
        
        if os.path.exists(temp_dir):
            print(f"Clearing existing temporary directory: {temp_dir}")
            os.system(f'rmdir /s /q {temp_dir}' if os.name == 'nt' else f'rm -rf {temp_dir}')

        print(f"Cloning repository '{repo_url}' into '{temp_dir}'...")

        git.Repo.clone_from(repo_url, temp_dir)
        print("Repository cloned successfully.")

        all_files_content = []
        
        repo_path = Path(temp_dir)
        
        print("Reading files from the repository...")
        
        for file_path in repo_path.glob('**/*'):
            if file_path.is_file():
                if file_path.suffix in CODE_EXTENSIONS:
                    try:
                        content = file_path.read_text(encoding='utf-8')
                    
                        relative_path = str(file_path.relative_to(repo_path))
                        
                        all_files_content.append((relative_path, content))
                    except Exception as e:
                        print(f"Could not read file {file_path}: {e}")
        
        print(f"Successfully read {len(all_files_content)} relevant files.")
        return all_files_content

    except Exception as e:
        print(f"An error occurred while loading the repository: {e}")
        return []
