import re


KNOWN_MEDICINES = [
    "banaba blend",
    "omega 3",
    "amoxicillin",
    "azithromycin",
    "cephalexin",
    "ciprofloxacin",
    "doxycycline",
    "paracetamol",
    "acetaminophen",
    "ibuprofen",
    "naproxen",
    "cetirizine",
    "loratadine",
    "fexofenadine",
    "levocetirizine",
    "omeprazole",
    "pantoprazole",
    "esomeprazole",
    "famotidine",
    "biotin",
    "fish oil",
]


IGNORED_NAMES = {
    "pharmacy",
    "medicine",
    "medicine label",
    "product name",
    "product",
    "name",
    "supplement facts",
    "supplement",
    "sugar",
    "solutions",
    "temp rate",
    "vector templates",
    "label design",
    "dreamstime",
}


def normalize_text(text: str) -> str:
    """
    Normalize OCR text for easier matching.
    Keeps the original meaning while removing
    unnecessary whitespace and formatting differences.
    """

    text = text.lower()

    text = text.replace("-", " ")
    text = text.replace("_", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_lines(text: str) -> list[str]:
    """
    Normalize OCR output while preserving line structure.
    """

    lines = []

    for line in text.splitlines():
        cleaned = re.sub(
            r"\s+",
            " ",
            line.strip(),
        )

        if cleaned:
            lines.append(cleaned)

    return lines


def find_known_medicine(
    text: str,
    lines: list[str],
) -> str | None:
    """
    Try to identify a known medicine or product name.

    Multi-word names are checked first so that
    'Banaba Blend' is selected instead of only
    'Banaba'.
    """

    normalized_text = normalize_text(text)

    normalized_lines = [
        normalize_text(line)
        for line in lines
    ]

    # -------------------------------------------------
    # 1. Check exact multi-word names across lines
    # -------------------------------------------------
    for medicine in KNOWN_MEDICINES:
        if " " not in medicine:
            continue

        medicine_words = medicine.split()

        # Normal same-line match
        pattern = (
            r"\b"
            + r"\s+".join(
                re.escape(word)
                for word in medicine_words
            )
            + r"\b"
        )

        if re.search(
            pattern,
            normalized_text,
        ):
            return format_medicine_name(medicine)

        # Match when OCR puts words on separate lines
        for index in range(
            len(normalized_lines)
        ):
            combined_parts = []

            for offset in range(
                len(medicine_words)
            ):
                current_index = index + offset

                if current_index >= len(
                    normalized_lines
                ):
                    break

                combined_parts.append(
                    normalized_lines[
                        current_index
                    ]
                )

            combined = " ".join(
                combined_parts
            )

            if re.search(
                pattern,
                combined,
            ):
                return format_medicine_name(
                    medicine
                )

    # -------------------------------------------------
    # 2. Check single-word known medicines
    # -------------------------------------------------
    for medicine in KNOWN_MEDICINES:
        if " " in medicine:
            continue

        pattern = (
            r"\b"
            + re.escape(medicine)
            + r"\b"
        )

        if re.search(
            pattern,
            normalized_text,
        ):
            return format_medicine_name(
                medicine
            )

    return None


def format_medicine_name(
    medicine_name: str,
) -> str:
    """
    Convert normalized medicine names into
    user-friendly display names.
    """

    display_names = {
        "banaba blend": "Banaba Blend",
        "omega 3": "Omega 3",
        "fish oil": "Fish Oil",
        "amoxicillin": "Amoxicillin",
        "azithromycin": "Azithromycin",
        "cephalexin": "Cephalexin",
        "ciprofloxacin": "Ciprofloxacin",
        "doxycycline": "Doxycycline",
        "paracetamol": "Paracetamol",
        "acetaminophen": "Acetaminophen",
        "ibuprofen": "Ibuprofen",
        "naproxen": "Naproxen",
        "cetirizine": "Cetirizine",
        "loratadine": "Loratadine",
        "fexofenadine": "Fexofenadine",
        "levocetirizine": "Levocetirizine",
        "omeprazole": "Omeprazole",
        "pantoprazole": "Pantoprazole",
        "esomeprazole": "Esomeprazole",
        "famotidine": "Famotidine",
        "biotin": "Biotin",
    }

    normalized_name = normalize_text(
        medicine_name
    )

    return display_names.get(
        normalized_name,
        medicine_name.title(),
    )


def extract_strength(
    text: str,
) -> str | None:
    """
    Extract medicine strength such as:
    500 mg, 250 mg, 1000 mcg, 6 g.
    """

    pattern = (
        r"\b\d+(?:\.\d+)?\s*"
        r"(?:mg|mcg|g|kg|ml|l)\b"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE,
    )

    if not match:
        return None

    return re.sub(
        r"\s+",
        " ",
        match.group(0).strip(),
    )


def extract_form(
    text: str,
) -> str | None:
    """
    Extract dosage form from OCR text.
    """

    forms = [
        "capsule",
        "capsules",
        "tablet",
        "tablets",
        "syrup",
        "solution",
        "injection",
        "cream",
        "ointment",
        "gel",
        "drops",
        "powder",
        "supplement",
        "softgel",
        "softgels",
    ]

    normalized_text = normalize_text(text)

    for form in forms:
        if re.search(
            rf"\b{re.escape(form)}\b",
            normalized_text,
        ):
            return form.title()

    return None


def extract_instructions(
    text: str,
) -> str | None:
    """
    Extract common medicine usage instructions.
    """

    lines = normalize_lines(text)

    instruction_keywords = [
        "take",
        "use",
        "apply",
        "drink",
        "consume",
        "once daily",
        "twice daily",
        "three times daily",
        "four times daily",
        "by mouth",
        "before food",
        "after food",
    ]

    for line in lines:
        normalized_line = normalize_text(
            line
        )

        for keyword in instruction_keywords:
            if keyword in normalized_line:
                return line

    return None


def extract_expiration_date(
    text: str,
) -> str | None:
    """
    Extract common expiration-date formats.
    """

    patterns = [
        r"\b(?:exp|expiration|expiry)"
        r"\s*(?:date)?\s*[:\-]?\s*"
        r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",

        r"\b(?:exp|expiration|expiry)"
        r"\s*(?:date)?\s*[:\-]?\s*"
        r"(\d{1,2}[/-]\d{4})",

        r"\b(?:exp|expiration|expiry)"
        r"\s*(?:date)?\s*[:\-]?\s*"
        r"(\d{4}[/-]\d{1,2})",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

    return None


def extract_name_from_strength(
    text: str,
) -> str | None:
    """
    Try to detect a medicine name when it appears
    directly before or near a strength value.
    """

    lines = normalize_lines(text)

    strength_pattern = re.compile(
        r"\b\d+(?:\.\d+)?\s*"
        r"(?:mg|mcg|g|kg|ml|l)\b",
        re.IGNORECASE,
    )

    for line in lines:
        if not strength_pattern.search(
            line
        ):
            continue

        cleaned = re.sub(
            strength_pattern,
            "",
            line,
        )

        cleaned = re.sub(
            r"[^A-Za-z0-9\s\-]",
            " ",
            cleaned,
        )

        cleaned = re.sub(
            r"\s+",
            " ",
            cleaned,
        ).strip()

        if not cleaned:
            continue

        normalized = normalize_text(
            cleaned
        )

        if normalized in IGNORED_NAMES:
            continue

        if len(cleaned.split()) <= 5:
            return cleaned.title()

    return None


def extract_uppercase_candidate(
    text: str,
) -> str | None:
    """
    Fallback for labels where OCR captures
    a medicine name in uppercase.
    """

    lines = normalize_lines(text)

    for line in lines:
        cleaned = line.strip()

        if not cleaned:
            continue

        # Ignore obvious template / stock-image text.
        normalized = normalize_text(
            cleaned
        )

        if normalized in IGNORED_NAMES:
            continue

        if any(
            ignored in normalized
            for ignored in [
                "vector",
                "dreamstime",
                "label design",
                "product name",
                "temp rate",
            ]
        ):
            continue

        letters = re.sub(
            r"[^A-Za-z]",
            "",
            cleaned,
        )

        if (
            letters
            and cleaned.upper() == cleaned
            and 3 <= len(letters) <= 30
        ):
            return cleaned.title()

    return None


def extract_medicine_info(
    text: str,
) -> dict:
    """
    Extract structured medicine information
    from OCR text.
    """

    if not text or not text.strip():
        return {
            "medicine_name": None,
            "strength": None,
            "form": None,
            "instructions": None,
            "expiration_date": None,
        }

    lines = normalize_lines(text)

    # -------------------------------------------------
    # Medicine name
    # -------------------------------------------------

    medicine_name = find_known_medicine(
        text,
        lines,
    )

    # Try name + strength if known medicine
    # matching did not find anything.
    if not medicine_name:
        medicine_name = (
            extract_name_from_strength(
                text
            )
        )

    # Final uppercase fallback.
    if not medicine_name:
        medicine_name = (
            extract_uppercase_candidate(
                text
            )
        )

    # Never accept obvious non-medicine labels.
    if medicine_name:
        normalized_name = normalize_text(
            medicine_name
        )

        if normalized_name in IGNORED_NAMES:
            medicine_name = None

    return {
        "medicine_name": medicine_name,
        "strength": extract_strength(text),
        "form": extract_form(text),
        "instructions": extract_instructions(
            text
        ),
        "expiration_date": (
            extract_expiration_date(text)
        ),
    }