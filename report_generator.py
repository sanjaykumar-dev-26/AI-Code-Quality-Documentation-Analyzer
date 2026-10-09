
from pathlib import Path
from datetime import datetime
import json


def generate_report(result, output_dir="reports"):
    """Generate and save a code quality report."""

    report_folder = Path(output_dir)
    report_folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = {
        "generated_at": timestamp,
        "file": result["file"],
        "summary": {
            "function_count": result["function_count"],
            "class_count": result["class_count"],
            "import_count": result["import_count"],
            "issue_count": result["issue_count"]
        },
        "issues": result["issues"]
    }

    output_file = report_folder / "quality_report.json"

    output_file.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print(f"Report saved to: {output_file}")

    return report