#!/usr/bin/env python3
"""Builds the public pages from the app's legal documents.

The source of truth is the app repository's `legal/` folder, which the app also shows on screen.
Run after changing those files, then commit the generated HTML:

    pip install markdown
    python3 build.py ../Everyday-Gym/legal
"""
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).parent

# source file, output folder, html lang, link to the other language
PAGES = [
    ("PRIVACY.md", "privacy", "en", ("Português", "../privacidade/")),
    ("PRIVACIDADE.md", "privacidade", "pt-BR", ("English", "../privacy/")),
]

TEMPLATE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<main>
<nav><a href="../">Everyday Gym</a><a href="{other_href}" hreflang="{other_lang}">{other_label}</a></nav>
{body}
</main>
</body>
</html>
"""


def web_links(text: str) -> str:
    """Adapts links written for the app (which shows them as plain text) to the web."""
    text = text.replace("](PRIVACIDADE.md)", "](../privacidade/)").replace("](PRIVACY.md)", "](../privacy/)")
    text = re.sub(r"\((policies\.google\.com/privacy)\)", r"([\1](https://\1))", text)
    text = re.sub(r"([\w.+-]+@[\w-]+(?:\.\w+)+)", r"[\1](mailto:\1)", text)
    # The app's renderer accepts a list right after a paragraph; Python-Markdown needs a blank line.
    return re.sub(r"(?m)^(?!- )(.+)\n(?=- )", "\\1\n\n", text)


def main(legal: Path) -> None:
    for source, folder, lang, (other_label, other_href) in PAGES:
        text = web_links((legal / source).read_text(encoding="utf-8"))
        title = text.splitlines()[0].lstrip("# ").strip()
        body = markdown.markdown(text, extensions=["tables"])
        out = ROOT / folder / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(
            TEMPLATE.format(
                lang=lang,
                title=title,
                body=body,
                other_href=other_href,
                other_label=other_label,
                other_lang="en" if lang != "en" else "pt-BR",
            ),
            encoding="utf-8",
        )
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "../Everyday-Gym/legal"))
