
import logging

from analyzer import analyze_file
from report_generator import generate_report
from logger import setup_logger


def main():
    logger = setup_logger()
    file_path = "sample_files/sample.py"

    try:
        logger.info("Code analysis started")
        result = analyze_file(file_path)

        print("File:", result["file"])
        print("Function count:", result["function_count"])
        print("Class count:", result["class_count"])
        print("Import count:", result["import_count"])
        print("Total issues:", result["issue_count"])

        generate_report(result)
        logger.info("Report generated successfully")

    except (FileNotFoundError, ValueError) as error:
        logger.error("Analysis failed: %s", error)
        print("Error:", error)

    except Exception:
        logger.exception("Unexpected error occurred")
        print("An unexpected error occurred. Check logs/app.log for details.")


if __name__ == "__main__":
    main()