
import re


def parse_log(log_text):

    if not log_text or not log_text.strip():
        raise ValueError("Log content cannot be empty.")

    # Store extracted information
    parsed_data = {
        "test_name": "Unknown",
        "exception_type": "Unknown",
        "error_message": "Unknown",
        "file_name": "Unknown",
        "line_number": "Unknown",
        "failure_log": log_text.strip()
    }

    # 1. Extract test name from PyTest FAILED line
    test_match = re.search(
        r"FAILED\s+(.+?)(?:\s+-\s+.*)?$",
        log_text,
        re.MULTILINE
    )

    if test_match:
        parsed_data["test_name"] = test_match.group(1).strip()

    # 2. Extract exception type
    exception_match = re.search(
        r"([A-Za-z_][A-Za-z0-9_]*(?:Exception|Error))"
        r"(?=:\s|\s*$)",
        log_text
    )

    if exception_match:
        parsed_data["exception_type"] = (
            exception_match.group(1)
        )

    # 3. Extract error message
    message_match = re.search(
        r"(?:Message:\s*|Exception:\s*|Error:\s*)"
        r"(.+)",
        log_text
    )

    if message_match:
        parsed_data["error_message"] = (
            message_match.group(1).strip()
        )

    elif exception_match:
        error_line = re.search(
            rf"{re.escape(parsed_data['exception_type'])}:\s*(.+)",
            log_text
        )

        if error_line:
            parsed_data["error_message"] = (
                error_line.group(1).strip()
            )

    # 4. Extract file name and line number
    file_match = re.search(
        r'File "([^"]+)", line (\d+)',
        log_text
    )

    if file_match:
        parsed_data["file_name"] = file_match.group(1)
        parsed_data["line_number"] = file_match.group(2)

    # 5. Return extracted information
    return parsed_data


if __name__ == "__main__":

    sample_log = """
    FAILED test_login.py::test_valid_login

    selenium.common.exceptions.NoSuchElementException:
    Message: Unable to locate element: //*[@id='login']

    File "test_login.py", line 25
    """

    result = parse_log(sample_log)

    print("\nParsed Failure Information:")

    for key, value in result.items():
        print(f"{key}: {value}")