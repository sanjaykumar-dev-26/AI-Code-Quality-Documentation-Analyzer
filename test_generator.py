
import ast
from pathlib import Path


def generate_test_drafts(file_path, output_dir="generated_tests"):
    """Generate basic pytest test templates for Python functions."""

    source_path = Path(file_path)
    source_code = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source_code)

    test_lines = [
        "import pytest",
        "",
        "# TODO: Import the functions you want to test.",
        "# Example: from sample import calculate_area",
        "",
    ]

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                continue

            parameters = [
                arg.arg
                for arg in node.args.args
                if arg.arg not in ("self", "cls")
            ]

            test_name = f"test_{node.name}"

            test_lines.extend([
                "",
                f"def {test_name}():",
                f'    """TODO: Write tests for {node.name}."""',
            ])

            if parameters:
                test_lines.append(
                    f"    # TODO: Provide test values for: {', '.join(parameters)}"
                )
            else:
                test_lines.append("    # TODO: Call the function")

            test_lines.append("    # TODO: Add assertions")

    output_folder = Path(output_dir)
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "test_generated.py"
    output_file.write_text("\n".join(test_lines) + "\n", encoding="utf-8")

    return output_file