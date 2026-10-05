"""Privacy masking service - masks PII before sending stories to AI."""

import re


# Patterns to mask
PII_PATTERNS = [
    # Phone numbers (Indian 10-digit, with optional +91/0 prefix)
    (r"\b(?:\+91[\s-]?|0)?[6-9]\d{9}\b", "[PHONE_MASKED]"),
    # Email addresses
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL_MASKED]"),
    # Student IDs (common patterns like 24CSE1234, 2024BCS001, etc.)
    (r"\b\d{2,4}[A-Z]{2,5}\d{2,6}\b", "[STUDENT_ID_MASKED]"),
    # Aadhaar numbers (12 digits, possibly with spaces)
    (r"\b\d{4}\s?\d{4}\s?\d{4}\b", "[AADHAAR_MASKED]"),
    # PAN card numbers
    (r"\b[A-Z]{5}\d{4}[A-Z]\b", "[PAN_MASKED]"),
    # Bank account numbers (9-18 digits)
    (r"\b\d{9,18}\b", "[ACCOUNT_MASKED]"),
    # Dates of birth in common formats (DD/MM/YYYY, DD-MM-YYYY)
    (r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", "[DATE_MASKED]"),
]


def mask_pii(text: str) -> str:
    """
    Mask personally identifiable information in the student's story.

    Args:
        text: The original student story.

    Returns:
        The story with PII masked.
    """
    masked = text
    for pattern, replacement in PII_PATTERNS:
        masked = re.sub(pattern, replacement, masked)
    return masked
