# Bookshelf package by Peter Flynn, with changes by Boris Veytsman

A LaTeX package for generating visual bookshelf displays from BibTeX entries.

## Usage

1. Edit `doc/sample.bib` with your book entries
2. Run `make` in the `doc/` directory
3. The build generates:
   - `spines.pdf` - PDF of book spines
   - `bookshelf.svg` - SVG version (via inkscape)

## Build Process

```bash
cd doc/
make spines.pdf      # Generate PDF only
make bookshelf.svg   # Generate SVG from PDF
make                 # Build everything
```

## SVG Generation

The SVG is generated from the PDF using inkscape:

```bash
inkscape --pdf-poppler --export-text-to-path --export-plain-svg \
    --export-area-drawing --export-filename=bookshelf.svg spines.pdf
```

Options:
- `--pdf-poppler`: Use poppler for PDF parsing
- `--export-text-to-path`: Convert text to paths for portability
- `--export-plain-svg`: Output plain SVG (no Inkscape-specific elements)
- `--export-area-drawing`: Export only the drawing area

## Current Shelf

![shelf](doc/bookshelf.svg)

## Files

- `doc/sample.bib` - Bibliography entries for books to display
- `doc/spines.tex` - LaTeX source that generates the shelf
- `doc/Makefile` - Build automation
