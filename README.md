# AI Code Quality & Documentation Analyzer

An AI-powered Python code analysis tool that helps developers understand code quality, identify potential issues, generate documentation drafts, and create test templates.

## 🚀 Live Demo

**[Try the Live App](https://ai-code-quality-documentation-analyzer-caps.streamlit.app/)**

## ✨ Features

* **Static Code Analysis:** Analyze Python source code using Python's AST module.
* **Code Quality Insights:** Identify missing docstrings, missing type hints, and other configured code quality issues.
* **AI Code Review:** Use Google Gemini to explain code purpose, potential bugs, improvements, and best practices.
* **AI Documentation Generation:** Generate documentation drafts for functions and classes.
* **Documentation Drafts:** Prepare documentation suggestions for detected functions and classes.
* **Test Template Generation:** Generate starter test templates for Python code.
* **Downloadable Reports:** Download analysis reports and generated documentation.
* **Interactive Web Interface:** Upload Python files and explore results through Streamlit.

## 🛠️ Tech Stack

* **Language:** Python
* **Web Framework:** Streamlit
* **Static Analysis:** Python AST
* **AI Integration:** Google Gemini API
* **Environment Configuration:** python-dotenv
* **Testing:** pytest

## 📂 Project Structure

```text
AI-Code-Quality-Documentation-Analyzer/
├── app.py
├── ai_service.py
├── analyzer.py
├── documentation_generator.py
├── test_generator.py
├── logger.py
├── main.py
├── generated_tests/
├── sample_files/
├── reports/
├── requirements.txt
└── .gitignore
```

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/sanjaykumar-dev-26/AI-Code-Quality-Documentation-Analyzer.git
cd AI-Code-Quality-Documentation-Analyzer
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure the Gemini API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key. Never commit `.env` or expose your API key publicly.

### 4. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## 🧪 Run Tests

```bash
python -m pytest generated_tests/test_generated.py -v
```

## 🔐 Security

* API keys are supplied through environment variables or deployment secrets.
* The `.env` file is excluded from Git using `.gitignore`.
* AI-generated reviews and documentation are suggestions and should be verified before use.

## 👨‍💻 Author

**Sanjay Kumar**

* GitHub: [sanjaykumar-dev-26](https://github.com/sanjaykumar-dev-26)

---

If you find this project useful, feel free to explore the code and try the live demo.
