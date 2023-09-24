import git

def fetch_git_changes(repo_path="."):
    try:
        # Abrir el repositorio
        repo = git.Repo(repo_path)
        
        # Comprobar si hay cambios
        diff = repo.git.diff()
        return diff
    except Exception as e:
        return f"Error al obtener cambios de git: {e}"

if __name__ == "__main__":
    # Imprimir las diferencias
    print(fetch_git_changes())
