
REQUIRED_FIELDS = [
    "bug_title",
    "description",
    "steps_to_reproduce",
    "expected_result",
    "actual_result",
    "severity",
    "priority",
    "root_cause",
    "suggested_fix"
]

ALLOWED_SEVERITIES = {
    "Critical", "High", "Medium", "Low"
}

ALLOWED_PRIORITIES = {
    "High", "Medium", "Low"
}


def validate_bug_report(bug_report, impact_known=False):

    if not isinstance(bug_report, dict):
        raise ValueError("Bug report must be a JSON object.")

    # Validate required fields and text values
    for field in REQUIRED_FIELDS:

        if field not in bug_report:
            raise ValueError(
                f"Missing required field: {field}"
            )

        if field == "steps_to_reproduce":
            continue

        value = bug_report[field]

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Invalid or empty field: {field}"
            )

    # Validate reproduction steps
    steps = bug_report["steps_to_reproduce"]

    if not isinstance(steps, list) or not steps:
        raise ValueError(
            "Steps to reproduce must be a non-empty list."
        )

    for step in steps:

        if not isinstance(step, str) or not step.strip():
            raise ValueError(
                "Each reproduction step must be non-empty text."
            )

        normalized_step = step.strip().lower()

        if normalized_step.startswith(
            ("the page should", "the application should",
             "the element should", "expected result:")
        ):
            raise ValueError(
                "Reproduction steps contain an expectation: "
                + step
            )

    # Validate severity and priority
    if bug_report["severity"] not in ALLOWED_SEVERITIES:
        raise ValueError("Invalid severity value.")

    if bug_report["priority"] not in ALLOWED_PRIORITIES:
        raise ValueError("Invalid priority value.")

    # Avoid unsupported impact classification
    if not impact_known:

        if bug_report["severity"] in {"Critical", "High"}:
            raise ValueError(
                "High/Critical severity requires impact evidence."
            )

        if bug_report["priority"] == "High":
            raise ValueError(
                "High priority requires urgency evidence."
            )

    return True
