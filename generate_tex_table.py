import unicodedata
from datetime import date

FILENAME = "coptic_letters.tex"

# Unicode ranges and extra codepoints
RANGES = [
    (0x2C80, 0x2CB1),  # Main Coptic letters
    (0x03E2, 0x03EF),  # Extended Coptic letters
    (0x2CB2, 0x2CFF),  # Remaining Coptic letters & symbols
    # (0x2CF4, 0x2CF8),  # skipped UNKNOWN
    # (0x2CF9, 0x2CFF),
    (0x0305, 0x0307),  # Diacritics: Macron, Dot above
]

# Today's date in French-style format
TODAY = date.today().strftime("%d %B %Y")  # e.g., 15 August 2025

HEADER = (
    r"""
\documentclass[10pt,a4paper]{article}
\usepackage{geometry}
\geometry{margin=0.25in}
\usepackage{fontspec}
\usepackage{longtable}
\usepackage[table]{xcolor}
\usepackage{booktabs}
\usepackage{array}

%% Fonts
\setmonofont{JetBrainsMono Nerd Font}[Scale=MatchLowercase]
\newfontfamily\copticfont{Noto Sans Coptic}[Scale=MatchLowercase]
\newfontfamily\diacriticfont{Noto Sans}[Scale=MatchLowercase]

\newcommand{\coptic}[1]{{\copticfont #1}}
\newcommand{\diacritic}[1]{{\diacriticfont #1}}

%% Table formatting
\newcolumntype{C}{>{\centering\arraybackslash}p{2.5cm}}
\newcolumntype{L}{>{\raggedright\arraybackslash}p{10cm}}

\title{Coptic Letters}
\author{Youssef Adly}
\date{%s}

\begin{document}
\maketitle

%% Alternating row colors
\rowcolors{2}{gray!15}{white}

\begin{longtable}{C C L}
\toprule
Codepoint & Glyph & Unicode Name \\
\midrule
\endfirsthead

\toprule
Codepoint & Glyph & Unicode Name \\
\midrule
\endhead
"""
    % TODAY
)

FOOTER = r"""
\bottomrule
\end{longtable}
\end{document}
"""


def generate_coptic_tex(filename: str = FILENAME):
    lines = [HEADER]

    for start, end in RANGES:
        for cp in range(start, end + 1):
            try:
                glyph = chr(cp)
                name = unicodedata.name(glyph)
                if "COPTIC" not in name:
                    lines.append(
                        f"\\texttt{{U+{cp:04X}}} & \\diacritic{{{glyph}}} & {name} \\\\"
                    )
                else:
                    lines.append(
                        f"\\texttt{{U+{cp:04X}}} & \\coptic{{{glyph}}} & {name} \\\\"
                    )
            except ValueError:
                continue

    lines.append(FOOTER)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"LaTeX file '{filename}' generated successfully.")


if __name__ == "__main__":
    generate_coptic_tex()
