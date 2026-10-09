
import ast
from pathlib import Path


def analyze_file(file_path):
    """Analyze a Python file and return code quality metrics."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file() or path.suffix != ".py":
        raise ValueError("Please provide a valid Python file.")

    source_code = path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source_code)
    except SyntaxError as error:
        raise ValueError(
            f"Invalid Python syntax in {path}: {error}"
        ) from error

    functions = []
    classes = []
    imports = []
    issues = []

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)

            if ast.get_docstring(node) is None:
                issues.append({
                    "line": node.lineno,
                    "type": "Missing docstring",
                    "name": node.name
                })

            arguments = (
                node.args.posonlyargs
                + node.args.args
                + node.args.kwonlyargs
            )

            if node.args.vararg:
                arguments.append(node.args.vararg)

            if node.args.kwarg:
                arguments.append(node.args.kwarg)

            for argument in arguments:
                if argument.arg not in ("self", "cls") and argument.annotation is None:
                    issues.append({
                        "line": argument.lineno,
                        "type": "Missing parameter type hint",
                        "name": f"{node.name}.{argument.arg}"
                    })

            if node.returns is None:
                issues.append({
                    "line": node.lineno,
                    "type": "Missing return type hint",
                    "name": node.name
                })

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

            if ast.get_docstring(node) is None:
                issues.append({
                    "line": node.lineno,
                    "type": "Missing docstring",
                    "name": node.name
                })

        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")

    return {
        "file": str(path),
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "function_count": len(functions),
        "class_count": len(classes),
        "import_count": len(imports),
        "issues": issues,
        "issue_count": len(issues)
    }