
from log_parser import parse_log
from bug_analyzer import analyze_failure
from validator import validate_bug_report
from excel_exporter import export_bug_report


def main():

    print("\n===================================")
    print("      AI BUG REPORT GENERATOR")
    print("===================================\n")

    print("Paste your PyTest/Selenium failure log.")
    print("Enter END on a new line when finished.\n")

    log_lines = []

    while True:

        line = input()

        if line.strip().upper() == "END":
            break

        log_lines.append(line)

    log_text = "\n".join(log_lines)

    try:

        # Step 1: Parse failure log
        print("\n[1/4] Parsing failure log...")

        parsed_data = parse_log(log_text)

        print("Log parsing completed.")

        # Step 2: AI bug analysis
        print("\n[2/4] Analyzing failure using Llama 3.2...")



        max_attempts = 3
        validation_feedback = None
        bug_report = None

        for attempt in range(1, max_attempts + 1):

            print(f"\nAI generation attempt: {attempt}")

            bug_report = analyze_failure(
                parsed_data,
                validation_feedback=validation_feedback
            )

            try:
                validate_bug_report(bug_report)

                print("AI report passed validation.")
                break

            except ValueError as error:

                validation_feedback = str(error)

                print(
                    f"Validation failed: {validation_feedback}"
                )

                if attempt == max_attempts:
                    raise ValueError(
                        "AI could not generate a valid "
                        "bug report after 3 attempts. "
                        f"Last error: {validation_feedback}"
                    )

                print("Retrying with validation feedback...")

        print("AI analysis completed.")



        # Step 3: Validate bug report
        print("\n[3/4] Validating generated bug report...")

        validate_bug_report(bug_report)

        print("Bug report validation passed.")

        # Step 4: Export to Excel
        print("\n[4/4] Exporting bug report to Excel...")

        export_bug_report(bug_report)

        print("\n===================================")
        print("       BUG REPORT GENERATED")
        print("===================================")

        print("\nBug Title:", bug_report["bug_title"])
        print("Severity:", bug_report["severity"])
        print("Priority:", bug_report["priority"])

    except Exception as error:

        print("\nERROR:", error)


if __name__ == "__main__":
    main()
