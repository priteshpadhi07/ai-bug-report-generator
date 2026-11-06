# AI Bug Report Generator

An AI-assisted automation failure analysis tool built using **Python, Ollama, and Llama 3.2**. It analyzes Selenium/PyTest failure logs and generates structured bug reports in Excel format.

The project uses a hybrid approach that combines deterministic Python-based extraction with local LLM-assisted investigation suggestions.

## Features

- Parse Selenium/PyTest failure logs.
- Extract test names, exception types, error messages, and traceback locations.
- Generate evidence-based bug titles, descriptions, and actual results.
- Use Llama 3.2 to suggest possible root causes and investigation steps.
- Validate generated bug reports.
- Retry AI generation when report validation fails.
- Apply provisional severity and priority classifications when impact is unknown.
- Export formatted bug reports to Excel.
- Run locally using Ollama without paid cloud AI APIs.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Ollama | Local LLM runtime |
| Llama 3.2 | AI-assisted failure investigation |
| Requests | Ollama API communication |
| OpenPyXL | Excel report generation |
| Selenium/PyTest | Supported failure-log sources |

## Project Structure

```text
ai-bug-report-generator/
├── main.py
├── llm_client.py
├── log_parser.py
├── bug_analyzer.py
├── validator.py
├── excel_exporter.py
├── requirements.txt
└── README.md
```

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/ai-bug-report-generator.git
cd ai-bug-report-generator
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Install Ollama**

Download Ollama from https://ollama.com.

Pull the model:

```bash
ollama pull llama3.2
```

Ensure Ollama is running locally.

## Usage

Run the application:

```bash
python main.py
```

Paste a Selenium/PyTest failure log:

```text
FAILED test_login.py::test_valid_login

selenium.common.exceptions.NoSuchElementException:
Message: Unable to locate element: //*[@id='login']

File "test_login.py", line 25
```

Enter `END` on a new line.

The application parses the log, generates an evidence-based report, validates its structure, and exports the results to:

`AI_Generated_Bug_Report.xlsx`

## Sample Output

| Field | Example |
|---|---|
| Bug Title | Selenium failed to locate element with ID `login` |
| Severity | Medium (provisional) |
| Priority | Medium (provisional) |
| Possible Root Causes | Incorrect locator, element timing, frame context, or DOM changes |
| Suggested Investigation | Verify locator, inspect DOM, review waits and browser context |

## Design Approach

The application separates observed facts from AI-generated hypotheses.

**Python handles:**
- Log parsing and extraction.
- Evidence-based report fields.
- Report validation.
- Provisional severity and priority.
- Excel export.

**Llama 3.2 handles:**
- Possible technical root causes.
- Suggested debugging and investigation steps.

This reduces the risk of AI inventing application behavior that is not supported by the failure log.

## Limitations

- Log parsing currently supports a limited set of failure formats.
- XPath extraction supports selected locator patterns.
- Business impact and urgency are not inferred from exceptions alone.
- Root-cause suggestions are hypotheses and require human verification.
- The generated report should be reviewed before filing a defect.

## Future Enhancements

- Support additional Selenium and PyTest exception formats.
- Batch processing of multiple test failures.
- Automated test-log file ingestion.
- Jira integration for defect creation.
- Enhanced semantic validation of AI-generated suggestions.
- Configurable severity and priority based on supplied impact evidence.

## Author

Developed as a Python and AI-assisted software test automation portfolio project.
