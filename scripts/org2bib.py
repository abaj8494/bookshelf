#!/usr/bin/env python3
"""
Generate sample.bib from org files in content-org/words/library/books/

Usage:
    python scripts/org2bib.py [--dry-run] [--rebuild]

Options:
    --dry-run   Print bib entries without writing
    --rebuild   Regenerate PDF and SVG after updating bib
"""

import os
import re
import sys
import subprocess
from pathlib import Path

# Paths relative to this script
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
SITE_ROOT = REPO_ROOT.parent.parent.parent  # static/code/bookshelf -> site root
BOOKS_DIR = SITE_ROOT / "content-org" / "words" / "library" / "books"
SAMPLE_BIB = REPO_ROOT / "doc" / "sample.bib"


def parse_org_file(filepath: Path) -> dict | None:
    """Extract metadata from an org file."""
    content = filepath.read_text(encoding="utf-8")

    # Skip index files
    if filepath.name == "_index.org":
        return None

    metadata = {"filename": filepath.stem}

    # Extract title
    title_match = re.search(r"#\+title:\s*(.+)", content, re.IGNORECASE)
    if title_match:
        metadata["title"] = title_match.group(1).strip()

    # Extract from hugo_custom_front_matter
    front_matter = re.search(r"#\+hugo_custom_front_matter:\s*(.+)", content, re.IGNORECASE)
    if front_matter:
        fm = front_matter.group(1)

        # Author - handle both string and list formats
        # Format 1: :author "Name"
        author_match = re.search(r':author\s+"([^"]+)"', fm)
        if author_match:
            metadata["author"] = author_match.group(1)
        else:
            # Format 2: :author '("Name1" "Name2" "Name3")
            author_list = re.search(r":author\s+'\(([^)]+)\)", fm)
            if author_list:
                # Extract quoted names
                names = re.findall(r'"([^"]+)"', author_list.group(1))
                if names:
                    metadata["author"] = " and ".join(names)

        # Year/composed - extract 4-digit year from various formats
        year_match = re.search(r':composed\s+"?[^"]*?(\d{4})"?', fm)
        if year_match:
            metadata["year"] = year_match.group(1)

        # Edition
        edition_match = re.search(r':edition\s+"([^"]+)"', fm)
        if edition_match:
            metadata["edition"] = edition_match.group(1)

    # Must have at least title and author
    if "title" not in metadata or "author" not in metadata:
        return None

    return metadata


def generate_bib_key(metadata: dict) -> str:
    """Generate a BibTeX key from metadata."""
    # Use first author's last name + year (or filename if no year)
    author = metadata.get("author", "unknown")
    first_author = author.split(" and ")[0].split(",")[0]
    # Get last word as surname
    surname = first_author.split()[-1].lower()
    # Remove non-alphanumeric
    surname = re.sub(r"[^a-z]", "", surname)

    year = metadata.get("year", "")

    if year:
        return f"{surname}{year}"
    else:
        # Use filename-based key
        return metadata["filename"].replace("-", "")


def format_bib_entry(metadata: dict) -> str:
    """Format metadata as a BibTeX entry."""
    key = generate_bib_key(metadata)

    lines = [f"@book{{{key},"]
    lines.append(f'  title = {{{metadata["title"]}}},')
    lines.append(f'  author = {{{metadata["author"]}}},')

    if "year" in metadata:
        lines.append(f'  year = {{{metadata["year"]}}},')

    if "edition" in metadata:
        lines.append(f'  edition = {{{metadata["edition"]}}},')

    lines.append("}")

    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv
    rebuild = "--rebuild" in sys.argv

    if not BOOKS_DIR.exists():
        print(f"Error: Books directory not found: {BOOKS_DIR}", file=sys.stderr)
        sys.exit(1)

    # Collect all org files
    org_files = sorted(BOOKS_DIR.glob("*.org"))
    print(f"Found {len(org_files)} org files in {BOOKS_DIR}")

    # Parse each file
    entries = []
    skipped = []

    for org_file in org_files:
        metadata = parse_org_file(org_file)
        if metadata:
            entries.append(format_bib_entry(metadata))
        else:
            if org_file.name != "_index.org":
                skipped.append(org_file.name)

    print(f"Generated {len(entries)} bib entries")
    if skipped:
        print(f"Skipped {len(skipped)} files (missing title/author): {', '.join(skipped[:5])}...")

    # Combine entries
    bib_content = "\n\n".join(entries) + "\n"

    if dry_run:
        print("\n--- BIB OUTPUT (dry run) ---")
        print(bib_content[:2000])
        if len(bib_content) > 2000:
            print(f"... ({len(bib_content)} chars total)")
    else:
        SAMPLE_BIB.write_text(bib_content, encoding="utf-8")
        print(f"Wrote {SAMPLE_BIB}")

        if rebuild:
            print("Rebuilding PDF and SVG...")
            os.chdir(REPO_ROOT)
            subprocess.run(["make", "svg"], check=True)
            print("Done!")


if __name__ == "__main__":
    main()
