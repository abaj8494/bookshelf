# Bookshelf

A LaTeX package for generating visual bookshelf displays from BibTeX entries.

Based on the bookshelf package by Peter Flynn, with changes by Boris Veytsman.

## Quick Start

```bash
# Edit your books
vim doc/sample.bib

# Generate PDF and SVG
make svg
```

## Make Targets

Run all commands from the repository root:

| Command | Description |
|---------|-------------|
| `make` | Build everything (cls, docs, PDF, etc.) |
| `make pdf` | Build `doc/spines.pdf` from `doc/sample.bib` |
| `make svg` | Build `doc/bookshelf.svg` from PDF (requires inkscape) |
| `make fonts` | Regenerate font files (run after TeX Live updates) |
| `make clean` | Remove intermediate files (aux, log, etc.) |
| `make distclean` | Deep clean including all outputs |

## Troubleshooting

### Font Errors

If you see errors like:
```
! Font \SILmfont=[...] not loadable: metric data not found or bad.
```

Run `make fonts` to regenerate the font selection for your current TeX Live installation:
```bash
make fonts
make pdf
```

### Interactive Prompts

During PDF generation, LaTeX may pause with `?` prompts for missing fonts. Press Enter to continue - it will select alternative fonts automatically.

## Files

```
bookshelf/
├── Makefile              # Main build file (run make from here)
├── doc/
│   ├── sample.bib        # Your book entries (edit this)
│   ├── spines.tex        # LaTeX source for bookshelf
│   ├── spines.pdf        # Generated PDF output
│   ├── bookshelf.svg     # Generated SVG output
│   ├── pickfont.tex      # Font selection (auto-generated)
│   └── allfonts          # Available fonts list (auto-generated)
└── scripts/
    ├── bookshelf-listallfonts
    └── bookshelf-mkfontsel
```

## SVG Generation

The SVG is generated from PDF using inkscape:

```bash
inkscape --pdf-poppler --export-text-to-path --export-plain-svg \
    --export-area-drawing --export-filename=bookshelf.svg spines.pdf
```

## Current Shelf

![shelf](doc/bookshelf.svg)
