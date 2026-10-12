
import pytest

from analyzer import analyze_file


def test_analyze_file_detects_functions_classes_and_imports(tmp_path):
    # Arrange: create a valid Python file for analysis.
    file_path = tmp_path / "sample.py"
    file_path.write_text(
        'import os\n'
        'from pathlib import Path\n\n'
        'class Calculator:\n'
        '    """Perform calculations."""\n'
        '    pass\n\n'
        'def add(a: int, b: int) -> int:\n'
        '    """Return the sum of two numbers."""\n'
        '    return a + b\n',
        encoding="utf-8",
    )

    # Act: analyze the file.
    result = analyze_file(file_path)

    # Assert: verify the reported metrics.
    assert result["file"] == str(file_path)
    assert result["functions"] == ["add"]
    assert result["classes"] == ["Calculator"]
    assert set(result["imports"]) == {"os", "pathlib"}
    assert result["function_count"] == 1
    assert result["class_count"] == 1
    assert result["import_count"] == 2
    assert result["issues"] == []
    assert result["issue_count"] == 0


def test_detects_missing_docstrings_and_type_hints(tmp_path):
    file_path = tmp_path / "issues.py"
    file_path.write_text(
        "class Empty:\n"
        "    pass\n\n"
        "def greet(name):\n"
        "    return name\n",
        encoding="utf-8",
    )

    result = analyze_file(file_path)

    assert result["function_count"] == 1
    assert result["class_count"] == 1
    assert result["issue_count"] == 4

    issue_types = [issue["type"] for issue in result["issues"]]

    assert issue_types.count("Missing docstring") == 2
    assert issue_types.count("Missing parameter type hint") == 1
    assert issue_types.count("Missing return type hint") == 1

    issue_names = [issue["name"] for issue in result["issues"]]
    assert "Empty" in issue_names
    assert "greet" in issue_names
    assert "greet.name" in issue_names


def test_accepts_fully_annotated_async_function(tmp_path):
    file_path = tmp_path / "async_sample.py"
    file_path.write_text(
        "async def fetch(url: str) -> str:\n"
        '    """Fetch a resource."""\n'
        "    return url\n",
        encoding="utf-8",
    )

    result = analyze_file(file_path)

    assert result["functions"] == ["fetch"]
    assert result["function_count"] == 1
    assert result["issues"] == []
    assert result["issue_count"] == 0


def test_raises_error_when_file_does_not_exist(tmp_path):
    file_path = tmp_path / "missing.py"

    with pytest.raises(FileNotFoundError, match="File not found"):
        analyze_file(file_path)


def test_rejects_non_python_file(tmp_path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("Hello", encoding="utf-8")

    with pytest.raises(ValueError, match="valid Python file"):
        analyze_file(file_path)


def test_rejects_directory_instead_of_file(tmp_path):
    directory_path = tmp_path / "sample_folder"
    directory_path.mkdir()

    with pytest.raises(ValueError, match="valid Python file"):
        analyze_file(directory_path)


def test_raises_clear_error_for_invalid_python_syntax(tmp_path):
    file_path = tmp_path / "broken.py"
    file_path.write_text(
        "def broken(:\n    pass\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid Python syntax"):
        analyze_file(file_path)


def test_analyzes_empty_python_file(tmp_path):
    file_path = tmp_path / "empty.py"
    file_path.write_text("", encoding="utf-8")

    result = analyze_file(file_path)

    assert result["functions"] == []
    assert result["classes"] == []
    assert result["imports"] == []
    assert result["function_count"] == 0
    assert result["class_count"] == 0
    assert result["import_count"] == 0
    assert result["issues"] == []
    assert result["issue_count"] == 0


def test_detects_missing_type_hints_for_varargs_and_kwargs(tmp_path):
    file_path = tmp_path / "variable_arguments.py"
    file_path.write_text(
        "def collect(*args, **kwargs):\n"
        '    """Collect variable arguments."""\n'
        "    return args, kwargs\n",
        encoding="utf-8",
    )

    result = analyze_file(file_path)

    missing_parameters = [
        issue["name"]
        for issue in result["issues"]
        if issue["type"] == "Missing parameter type hint"
    ]

    assert missing_parameters == [
        "collect.args",
        "collect.kwargs",
    ]