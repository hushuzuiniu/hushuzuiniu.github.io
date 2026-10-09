# Shu Hu 胡书

Bilingual academic profile: https://hushuzuiniu.github.io/

- English: `/`; 中文: `/zh/`
- Two-page editable Word and PDF CVs: `/uploads/`
- Shared current data: `data/profile.json`
- Original Academic / Wowchemy visual theme, assets and photo gallery retained.
- Publications form one chronological list with author, title, venue, year and DOI.

To regenerate both language pages after updating profile data, run `python3 tools/build_site.py` (requires `lxml`). The retained Academic template is `tools/academic-template.txt`. Update the four CV files in `uploads/` separately; `uploads/resume.pdf` is a compatibility copy of the English PDF.

GitHub Pages serves the `master` branch root. Earlier template routes remain available and are excluded from search indexing.
