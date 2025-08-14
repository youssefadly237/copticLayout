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
    "<TLDE>": ("`", None, None, None, None),
    # Number row
    "<AE01>": ("1", None, None, None, None),
    "<AE02>": ("2", None, None, None, None),
    "<AE03>": ("3", None, None, None, None),
    "<AE04>": ("4", None, None, None, None),
    "<AE05>": ("5", None, None, None, None),
    "<AE06>": ("6", None, None, None, None),
    "<AE07>": ("7", None, None, None, None),
    "<AE08>": ("8", None, None, None, None),
    "<AE09>": ("9", None, None, None, None),
    "<AE10>": ("0", None, None, None, None),
    "<AE11>": ("-", None, None, None, None),
    "<AE12>": ("=", None, None, None, None),
    # Top row
    "<AD01>": ("Q", None, None, None, None),
    "<AD02>": ("W", None, None, None, None),
    "<AD03>": ("E", None, None, None, None),
    "<AD04>": ("R", None, None, None, None),
    "<AD05>": ("T", None, None, None, None),
    "<AD06>": ("Y", None, None, None, None),
    "<AD07>": ("U", None, None, None, None),
    "<AD08>": ("I", None, None, None, None),
    "<AD09>": ("O", None, None, None, None),
    "<AD10>": ("P", None, None, None, None),
    "<AD11>": ("[", None, None, None, None),
    "<AD12>": ("]", None, None, None, None),
    # Home row
    "<AC01>": ("A", None, None, None, None),
    "<AC02>": ("S", None, None, None, None),
    "<AC03>": ("D", None, None, None, None),
    "<AC04>": ("F", None, None, None, None),
    "<AC05>": ("G", None, None, None, None),
    "<AC06>": ("H", None, None, None, None),
    "<AC07>": ("J", None, None, None, None),
    "<AC08>": ("K", None, None, None, None),
    "<AC09>": ("L", None, None, None, None),
    "<AC10>": (";", None, None, None, None),
    "<AC11>": ("'", None, None, None, None),
    # Bottom row
    "<AB01>": ("Z", None, None, None, None),
    "<AB02>": ("X", None, None, None, None),
    "<AB03>": ("C", None, None, None, None),
    "<AB04>": ("V", None, None, None, None),
    "<AB05>": ("B", None, None, None, None),
    "<AB06>": ("N", None, None, None, None),
    "<AB07>": ("M", None, None, None, None),
    "<AB08>": (",", None, None, None, None),
    "<AB09>": (".", None, None, None, None),
    "<AB10>": ("/", None, None, None, None),
}


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

        label, *levels = values
        levels_array = [lvl if lvl is not None else "" for lvl in levels]
        levels_str = ", ".join(levels_array).rstrip(", ")
        padding = " " * (array_len - len(levels_str)) if levels_str else ""
        glyphs = " / ".join(chr(int(l[1:], 16)) for l in levels if l is not None)
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
