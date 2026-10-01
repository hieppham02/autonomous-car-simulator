from pathlib import Path

repo = Path(".")
extensions = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml"}

with open("repo_context.md", "w", encoding="utf-8") as out:
    for path in sorted(repo.rglob("*")):
        if (
            path.is_file()
            and path.suffix.lower() in extensions
            and ".git" not in path.parts
            and "__pycache__" not in path.parts
            and "venv" not in path.parts
            and ".venv" not in path.parts
            and "node_modules" not in path.parts
        ):
            out.write(f"\n\n# FILE: {path.as_posix()}\n\n")
            try:
                out.write(path.read_text(encoding="utf-8"))
            except UnicodeDecodeError:
                pass