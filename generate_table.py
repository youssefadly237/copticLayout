"""
Generate a complete Markdown table of all Coptic letters in correct script order.
Outputs a file `coptic_letters.md`.
"""

import unicodedata

FILENAME = "coptic_letters.md"

TITLE = "# Complete Coptic Letters\n\n| Codepoint | Glyph | Unicode Name |"
SEPARATOR = "|---|---|---|"

# Unicode ranges
RANGES = [
    (0x2C80, 0x2CB1),  # Main Coptic letters
    (0x03E2, 0x03EF),  # Extended Greek & Coptic
    (0x2CB2, 0x2CFF),  # Remaining Coptic letters & symbols
    (0x0305, 0x0307),  # Diacritics: Macron, Dot above
]


def generate_coptic_table_md(filename: str = FILENAME):
    """
    Table gen logic
    """
    lines = [TITLE, SEPARATOR]

    for start, end in RANGES:
        for cp in range(start, end + 1):
            try:
                glyph = chr(cp)
                name = unicodedata.name(glyph)  # will raise ValueError if invalid
                # Include all valid glyphs (letters or diacritics)
                lines.append(f"| U+{cp:04X} | {glyph} | {name} |")
            except ValueError:
                continue  # skip invalid codepoints like UNKNOWN

    content = "\n".join(lines)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Markdown table saved to '{filename}'.")


if __name__ == "__main__":
    generate_coptic_table_md()
