
import ast
from pathlib import Path


def generate_documentation(file_path, output_dir="reports"):
    """Generate documentation drafts for functions and classes."""

    source_path = Path(file_path)
    source_code = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source_code)

    documentation = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node) is None:
                parameters = [
                    arg.arg
                    for arg in node.args.args
                    if arg.arg not in ("self", "cls")
                ]

                documentation.append({
                    "type": "function",
                    "name": node.name,
                    "line": node.lineno,
                    "parameters": parameters,
                    "draft": (
                        f"Document the purpose of {node.name}. "
                        f"Explain its parameters: {', '.join(parameters) or 'none'}. "
                        "Describe its return value and any side effects."
                    )
                })

        elif isinstance(node, ast.ClassDef):
            if ast.get_docstring(node) is None:
                documentation.append({
                    "type": "class",
                    "name": node.name,
                    "line": node.lineno,
                    "draft": (
                        f"Describe the responsibility of the {node.name} class, "
                        "its main attributes, and its public methods."
                    )
                })

    output_folder = Path(output_dir)
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "documentation_drafts.json"

    import json
    output_file.write_text(
        json.dumps(documentation, indent=4),
        encoding="utf-8"
    )

    return documentation