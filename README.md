# Bookshelf

A LaTeX package for generating visual bookshelf displays from BibTeX entries.

Based on the bookshelf package by Peter Flynn, with changes by Boris Veytsman.

## Quick Start

```bash
# Generate bib from org files, then build PDF and SVG
make rebuild
```

## Make Targets

Run all commands from the repository root:

| Command | Description |
|---------|-------------|
| `make` | Build everything (cls, docs, PDF, etc.) |
| `make bib` | Generate `doc/sample.bib` from org files |
| `make pdf` | Build `doc/spines.pdf` from `doc/sample.bib` |
| `make svg` | Build `doc/bookshelf.svg` from PDF (requires inkscape) |
| `make rebuild` | Full pipeline: bib → pdf → svg |
| `make fonts` | Regenerate font files (run after TeX Live updates) |
| `make clean` | Remove intermediate files (aux, log, etc.) |
| `make distclean` | Deep clean including all outputs |

## Bib Generation

The `make bib` command runs `scripts/org2bib.py` which:

1. Scans `content-org/words/library/books/*.org`
2. Extracts metadata (title, author, year, edition)
3. Generates `doc/sample.bib`

Org files should have this format:
```org
#+title: Book Title
#+hugo_custom_front_matter: :author "Author Name" :composed "2020" :edition "First"
```

Multi-author format:
```org
#+hugo_custom_front_matter: :author '("Author1" "Author2" "Author3")
```

## Hugo Integration

To rebuild the bookshelf before Hugo builds, create a pre-build script:

```bash
#!/bin/bash
# scripts/pre-build.sh
cd static/code/bookshelf && make rebuild
```

Or add to your build command:
```bash
(cd static/code/bookshelf && make rebuild) && hugo server ...
```

For CI/CD, add to your build pipeline before `hugo build`.

## Troubleshooting

### Font Errors

If you see errors like:
```
! Font \SILmfont=[...] not loadable: metric data not found or bad.
```

Run `make fonts` to regenerate the font selection:
```bash
make fonts
make pdf
```

### Interactive Prompts

During PDF generation, LaTeX may pause with `?` prompts for missing fonts. Press Enter to continue.

## Files

```
bookshelf/
├── Makefile              # Main build file
├── scripts/
│   ├── org2bib.py        # Generate bib from org files
│   ├── bookshelf-listallfonts
│   └── bookshelf-mkfontsel
└── doc/
    ├── sample.bib        # Generated from org files
    ├── spines.tex        # LaTeX source
    ├── spines.pdf        # Generated PDF
    ├── bookshelf.svg     # Generated SVG
    ├── pickfont.tex      # Font selection (auto-generated)
    └── allfonts          # Available fonts (auto-generated)
```

## Current Shelf

![shelf](doc/bookshelf.svg)
