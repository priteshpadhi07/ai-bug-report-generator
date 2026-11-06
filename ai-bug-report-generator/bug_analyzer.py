
import json
import re

from llm_client import generate_response


def extract_locator(error_message):

    # Extract XPath from a Selenium error message
    match = re.search(
        r"(//\*\[@id=['\"][^'\"]+['\"]\])",
        error_message
    )

    if match:
        return match.group(1)

    return None


def analyze_failure(parsed_data, validation_feedback=None):

    test_name = parsed_data.get("test_name", "Unknown")
    exception_type = parsed_data.get(
        "exception_type", "Unknown"
    )
    error_message = parsed_data.get(
        "error_message", "Unknown"
    )
    failure_log = parsed_data.get(
        "failure_log", ""
    )

    locator = extract_locator(error_message)

    # -------------------------------------------------
    # Step 1: Construct evidence-based report fields
    # -------------------------------------------------

    if exception_type == "NoSuchElementException":

        if locator:
            bug_title = (
                f"Selenium failed to locate element: {locator}"
            )

            description = (
                f"Test '{test_name}' failed with "
                f"{exception_type}. Selenium reported "
                f"that no element matched locator "
                f"'{locator}'. Business impact is unknown."
            )

            actual_result = (
                f"Selenium could not locate an element "
                f"matching '{locator}'."
            )

        else:
            bug_title = (
                "Selenium failed to locate an element"
            )

            description = (
                f"Test '{test_name}' failed with "
                f"{exception_type}. "
                f"Error: {error_message}. "
                f"Business impact is unknown."
            )

            actual_result = (
                f"Selenium raised {exception_type}: "
                f"{error_message}"
            )

    else:

        bug_title = (
            f"Automation test failure: {exception_type}"
        )

        description = (
            f"Test '{test_name}' failed with "
            f"{exception_type}. "
            f"Error: {error_message}. "
            f"Business impact is unknown."
        )

        actual_result = (
            f"Automation test raised {exception_type}: "
            f"{error_message}"
        )

    steps_to_reproduce = [
        (
            f"Execute the automated test '{test_name}' "
            "in the environment where the failure occurred."
        )
    ]

    expected_result = (
        "Expected application behavior is not "
        "established by the supplied failure log."
    )

    # -------------------------------------------------
    # Step 2: Ask AI for investigation suggestions only
    # -------------------------------------------------

    prompt = f"""
You are a Senior QA Automation Engineer.

Analyze the following automation test failure.

Test Name: {test_name}
Exception Type: {exception_type}
Error Message: {error_message}

Complete Failure Log:
{failure_log}

TASK:

Suggest possible technical causes and investigation
steps for this automation failure.

Return valid JSON only:

{{
    "root_cause": "Possible causes requiring verification",
    "suggested_fix": "Specific investigation steps"
}}

RULES:

1. Do not claim that an application defect is confirmed.
2. Do not invent application functionality.
3. Do not assume an element is a button, link, or input.
4. Do not invent business impact.
5. Clearly state that root causes are hypotheses.
6. Consider test-script, locator, synchronization,
   browser context, environment, and application causes
   when relevant.
7. Suggest practical debugging steps.
8. Return valid JSON only.
"""

    if validation_feedback:

        prompt += f"""

Previous validation error:
{validation_feedback}

Correct the problem in your response.
"""

    response = generate_response(prompt)

    try:
        ai_result = json.loads(response)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"AI returned invalid JSON: {error}"
        )

    if not isinstance(ai_result, dict):
        raise ValueError(
            "AI investigation result must be a JSON object."
        )

    root_cause = ai_result.get("root_cause")
    suggested_fix = ai_result.get("suggested_fix")


    # Use evidence-based investigation guidance
    # if the AI response is missing required fields.


    invalid_root_causes = {
        "possible causes requiring verification",
        "possible root cause",
        "unknown",
        "not available",
        "n/a",
        "requires investigation",
        "further investigation required"
    }

    if (
        not isinstance(root_cause, str)
        or not root_cause.strip()
        or root_cause.strip().lower().rstrip(".:")
        in invalid_root_causes
    ):


        if exception_type == "NoSuchElementException":

            root_cause = (
                "Possible causes include an incorrect locator, "
                "element loading delay, incorrect frame context, "
                "or an application DOM change. "
                "The actual cause requires investigation."
            )

        else:

            root_cause = (
                f"The cause of {exception_type} is not "
                "confirmed by the available failure log. "
                "Further investigation is required."
            )

    if not isinstance(suggested_fix, str) or not suggested_fix.strip():

        if exception_type == "NoSuchElementException":

            suggested_fix = (
                "Inspect the page DOM, verify the element locator, "
                "check explicit waits, confirm the correct frame "
                "or window context, and review application changes."
            )

        else:

            suggested_fix = (
                "Review the complete traceback, inspect the "
                "failing test code, verify the test environment, "
                "and reproduce the failure before identifying a fix."
            )


    # -------------------------------------------------
    # Step 3: Assemble final report
    # -------------------------------------------------

    bug_report = {
        "bug_title": bug_title,
        "description": description,
        "steps_to_reproduce": steps_to_reproduce,
        "expected_result": expected_result,
        "actual_result": actual_result,
        "severity": "Medium",
        "priority": "Medium",
        "root_cause": (
            "Possible causes requiring verification: "
            + root_cause.strip()
        ),
        "suggested_fix": suggested_fix.strip()
    }

    return bug_report
