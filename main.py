
from analyzer import analyze_file
from report_generator import generate_report


def main():
    file_path = "sample_files/sample.py"

    result = analyze_file(file_path)

    print("File:", result["file"])
    print("Function count:", result["function_count"])
    print("Class count:", result["class_count"])
    print("Import count:", result["import_count"])
    print("Total issues:", result["issue_count"])

    generate_report(result)


if __name__ == "__main__":
    main()