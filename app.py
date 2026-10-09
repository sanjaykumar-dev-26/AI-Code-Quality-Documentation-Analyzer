
import json
import tempfile
from pathlib import Path

import streamlit as st

from ai_service import (
    review_python_code,
    generate_ai_documentation
)
from analyzer import analyze_file
from documentation_generator import generate_documentation
from test_generator import generate_test_drafts


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Code Quality Analyzer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Code Quality & Documentation Analyzer")

st.write(
    "Analyze Python code quality, generate documentation "
    "and test templates, and get AI-powered code insights."
)


# --------------------------------------------------
# Python File Upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a Python file",
    type=["py"]
)


if uploaded_file is not None:

    try:
        source_code = uploaded_file.getvalue().decode("utf-8")

    except UnicodeDecodeError:
        st.error("The uploaded file is not valid UTF-8 text.")
        st.stop()

    st.success(f"Uploaded: {uploaded_file.name}")

    with st.expander("Preview Python Code"):
        st.code(source_code, language="python")

    # --------------------------------------------------
    # 1. Traditional Code Analysis
    # --------------------------------------------------

    if st.button("Analyze Code", type="primary"):

        try:
            with tempfile.TemporaryDirectory() as temp_dir:

                temp_dir = Path(temp_dir)

                temp_file = (
                    temp_dir / Path(uploaded_file.name).name
                )

                temp_file.write_text(
                    source_code,
                    encoding="utf-8"
                )

                # Analyze code quality
                result = analyze_file(temp_file)

                # Generate traditional documentation drafts
                documentation = generate_documentation(
                    temp_file,
                    output_dir=temp_dir / "reports"
                )

                # Generate test templates
                test_file = generate_test_drafts(
                    temp_file,
                    output_dir=temp_dir / "generated_tests"
                )

                # Read test file before temporary directory is deleted
                test_code = test_file.read_text(
                    encoding="utf-8"
                )

            # ------------------------------------------
            # Analysis Metrics
            # ------------------------------------------

            st.subheader("📊 Analysis Results")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Functions",
                result["function_count"]
            )

            col2.metric(
                "Classes",
                result["class_count"]
            )

            col3.metric(
                "Imports",
                result["import_count"]
            )

            col4.metric(
                "Issues",
                result["issue_count"]
            )

            # ------------------------------------------
            # Functions, Classes and Imports
            # ------------------------------------------

            st.subheader("🛠️ Functions")

            st.write(
                result["functions"] or "No functions found."
            )

            st.subheader("📦 Classes")

            st.write(
                result["classes"] or "No classes found."
            )

            st.subheader("📚 Imports")

            st.write(
                result["imports"] or "No imports found."
            )

            # ------------------------------------------
            # Code Quality Issues
            # ------------------------------------------

            st.subheader("⚠️ Code Quality Issues")

            if result["issues"]:

                st.dataframe(
                    result["issues"],
                    use_container_width=True
                )

            else:
                st.success(
                    "No issues detected by the current checks."
                )

            st.download_button(
                label="⬇️ Download Analysis Report (JSON)",
                data=json.dumps(result, indent=4),
                file_name="quality_report.json",
                mime="application/json",
                key="download_analysis"
            )

            # ------------------------------------------
            # Traditional Documentation Drafts
            # ------------------------------------------

            st.subheader("📝 Documentation Drafts")

            if documentation:

                st.dataframe(
                    documentation,
                    use_container_width=True
                )

                st.download_button(
                    label="⬇️ Download Documentation Drafts (JSON)",
                    data=json.dumps(documentation, indent=4),
                    file_name="documentation_drafts.json",
                    mime="application/json",
                    key="download_docs"
                )

            else:
                st.success(
                    "All detected functions and classes "
                    "already have docstrings."
                )

            # ------------------------------------------
            # Test Templates
            # ------------------------------------------

            st.subheader("🧪 Generated Test Templates")

            st.info(
                "These are starter templates. Add meaningful "
                "test values and assertions before relying on them."
            )

            st.code(
                test_code,
                language="python"
            )

            st.download_button(
                label="⬇️ Download Test Template (Python)",
                data=test_code,
                file_name="test_generated.py",
                mime="text/x-python",
                key="download_tests"
            )

        except (
            ValueError,
            UnicodeDecodeError,
            SyntaxError
        ) as error:

            st.error(str(error))

        except Exception as error:

            st.error(f"Unexpected error: {error}")

    # --------------------------------------------------
    # 2. Gemini AI Code Review
    # --------------------------------------------------

    st.divider()

    st.subheader("🤖 AI Code Review")

    st.write(
        "Ask Gemini to explain the code, identify potential bugs, "
        "suggest improvements, and draft missing docstrings."
    )

    if st.button("Review Code with Gemini"):

        try:
            with st.spinner(
                "Gemini is reviewing your code..."
            ):

                ai_review = review_python_code(source_code)

            st.success("AI code review completed!")

            st.markdown(ai_review)

            st.download_button(
                label="⬇️ Download AI Review",
                data=ai_review,
                file_name="ai_code_review.md",
                mime="text/markdown",
                key="download_ai_review"
            )

        except Exception as error:

            st.error(f"AI review failed: {error}")

    # --------------------------------------------------
    # 3. Gemini AI Documentation Generator
    # --------------------------------------------------

    st.divider()

    st.subheader("📘 AI Documentation Generator")

    st.write(
        "Generate meaningful, AI-written documentation "
        "for functions, asynchronous functions, and classes."
    )

    if st.button("Generate AI Documentation"):

        try:
            with st.spinner(
                "Gemini is generating documentation..."
            ):

                ai_documentation = generate_ai_documentation(
                    source_code
                )

            st.success(
                "AI documentation generated successfully!"
            )

            st.markdown(ai_documentation)

            st.download_button(
                label="⬇️ Download AI Documentation",
                data=ai_documentation,
                file_name="ai_documentation.md",
                mime="text/markdown",
                key="download_ai_documentation"
            )

        except Exception as error:

            st.error(
                f"AI documentation generation failed: {error}"
            )

else:

    st.info(
        "Upload a Python (.py) file to get started."
    )