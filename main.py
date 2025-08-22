"""
Generate a complete XKB keyboard layout file from a Python dictionary.

Each key is mapped to up to 4 levels:
    - level1: base (plain)
    - level2: Shift
    - level3: AltGr (Right Alt)
    - level4: Shift + AltGr

Empty levels (None) are skipped, but key syntax remains valid.

Outputs a ready-to-use `.xkb` file.
"""

# Configuration variables
LAYOUT_NAME = "Egyptian"
LAYOUT_TITLE = "Coptic"
LEVEL3_INCLUDE = "level3(ralt_switch)"
ROW_HEADERS = {
    "<TLDE>": "Tilde / key left of 1",
    "<AE01>": "Number row",
    "<AD01>": "Top row (Q-P)",
    "<AC01>": "Home row (A-L)",
    "<AB01>": "Bottom row (Z-M)",
}

# Key mapping: (label, level1, level2, level3, level4)
mapping = {
    "<TLDE>": ("`", "U0307", "U0305", "U0306", None),
    # Number row
    "<AE01>": ("1", "1", "exclam", None, None),
    "<AE02>": ("2", "2", "at", None, None),
    "<AE03>": ("3", "3", "numbersign", None, None),
    "<AE04>": ("4", "4", "dollar", None, None),
    "<AE05>": ("5", "5", "percent", None, None),
    "<AE06>": ("6", "6", "asciicircum", None, None),
    "<AE07>": ("7", "7", "ampersand", None, None),
    "<AE08>": ("8", "8", "asterisk", None, None),
    "<AE09>": ("9", "9", "parenleft", None, None),
    "<AE10>": ("0", "0", "parenright", None, None),
    "<AE11>": ("-", "minus", "underscore", None, None),
    "<AE12>": ("=", "equal", "plus", None, None),
    # Top row
    "<AD01>": ("Q", "U2C91", "U2C90", None, None),
    "<AD02>": ("W", "U2CB1", "U2CB0", None, None),
    "<AD03>": ("E", "U2C89", "U2C88", None, None),
    "<AD04>": ("R", "U2CA3", "U2CA2", None, None),
    "<AD05>": ("T", "U2CA7", "U2CA6", None, None),
    "<AD06>": ("Y", "U2CAF", "U2CAE", None, None),
    "<AD07>": ("U", "U2CA9", "U2CA8", None, None),
    "<AD08>": ("I", "U2C93", "U2C92", None, None),
    "<AD09>": ("O", "U2C9F", "U2C9E", None, None),
    "<AD10>": ("P", "U2CA1", "U2CA0", "U2CE6", None),
    "<AD11>": ("[", "U2C9D", "U2C9C", None, None),
    "<AD12>": ("]", "U03E3", "U03E2", None, None),
    # Home row
    "<AC01>": ("A", "U2C81", "U2C80", None, None),
    "<AC02>": ("S", "U03ED", "U03EC", None, None),
    "<AC03>": ("D", "U2C87", "U2C86", None, None),
    "<AC04>": ("F", "U03E5", "U03E4", None, None),
    "<AC05>": ("G", "U2C85", "U2C84", None, None),
    "<AC06>": ("H", "U2C8F", "U2C8E", None, None),
    "<AC07>": ("J", "U03EB", "U03EA", None, None),
    "<AC08>": ("K", "U2C95", "U2C94", "U2CB9", "U2CB8"),
    "<AC09>": ("L", "U2C97", "U2C96", None, None),
    "<AC10>": (";", "U03EF", "U03EE", None, None),
    "<AC11>": ("'", "U03E7", "U03E6", None, None),
    # Bottom row
    "<AB01>": ("Z", "U2C8D", "U2C8C", None, None),
    "<AB02>": ("X", "U2CAD", "U2CAC", None, None),
    "<AB03>": ("C", "U2CA5", "U2CA4", None, None),
    "<AB04>": ("V", "U2CAB", "U2CAA", None, None),
    "<AB05>": ("B", "U2C83", "U2C82", None, None),
    "<AB06>": ("N", "U2C9B", "U2C9A", None, None),
    "<AB07>": ("M", "U2C99", "U2C98", "U2CE5", None),
    "<AB08>": (",", "U03E9", "U03E8", None, None),
    "<AB09>": (".", "U2C8B", "U2C8A", None, None),
    "<AB10>": ("/", None, None, None, None),
}


def unicode_to_char(value):
    """Convert Unicode codepoint string to character, or return as-is if not Unicode format."""
    if value and value.startswith("U") and len(value) > 1:
        try:
            return chr(int(value[1:], 16))
        except ValueError:
            return value  # Return as-is if not valid hex
    return value


def generate_xkb_file(mapping_dict, layout_name, layout_title, level3_include):
    """
    Generate an XKB layout string from the mapping dictionary.

    Args:
        mapping (dict): {keycode: (label, lvl1, lvl2, lvl3, lvl4)}
        layout_name (str): XKB symbol name
        layout_title (str): Display name
        level3_include (str): Level3 file to include

    Returns:
        str: Complete XKB file content
    """
    key_len = max(len(k) for k in mapping_dict)
    array_len = max(len(", ".join(filter(None, v[1:]))) for v in mapping_dict.values())

    lines = [
        "default  partial alphanumeric_keys modifier_keys",
        f'xkb_symbols "{layout_name}" {{',
        f'    name[Group1] = "{layout_title}";\n',
    ]

    for key_code, values in mapping_dict.items():
        # Comment if row begin
        if key_code in ROW_HEADERS:
            lines.append(f"    // {ROW_HEADERS[key_code]}")
        if not any(values[1:]):
            continue
        label, *levels = values
        levels_array = [lvl if lvl is not None else "" for lvl in levels]
        levels_str = ", ".join(levels_array).rstrip(", ")
        padding = " " * (array_len - len(levels_str)) if levels_str else ""

        # Generate comment with actual characters (only for Unicode values)
        glyphs = " / ".join(
            unicode_to_char(l) for l in levels if l is not None and l.startswith("U")
        )
        comment = f"{label} -> {glyphs}" if glyphs else f"{label}"

        lines.append(
            f"    key {key_code.ljust(key_len)} {{ [ {levels_str} ] }}{padding} ;  // {comment}"
        )

    lines.append(f'\n    include "{level3_include}"')
    lines.append("};")

    return "\n".join(lines)


if __name__ == "__main__":
    xkb_content = generate_xkb_file(mapping, LAYOUT_NAME, LAYOUT_TITLE, LEVEL3_INCLUDE)
    # Save to file
    with open(f"{LAYOUT_NAME}.xkb", "w", encoding="utf-8") as f:
        f.write(xkb_content)
    print(f"XKB file '{LAYOUT_NAME}.xkb' generated successfully!")
