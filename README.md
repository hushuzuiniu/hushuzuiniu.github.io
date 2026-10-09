# Shu Hu 胡书

Bilingual academic profile: https://hushuzuiniu.github.io/

- English: `/`
- 中文: `/zh/`
- PDF and editable Word CVs: `/uploads/`
- Shared profile and publication data: `data/profile.json`
- Layout and styling: `assets/site.css`

To regenerate both language pages after changing profile data, run `python3 tools/build_site.py`. The generator uses only the Python standard library. Update the PDF and Word CVs in `uploads/` separately when the profile changes. `uploads/resume.pdf` is a compatibility copy of the English PDF.

GitHub Pages serves the `master` branch root. No Hugo installation or external frontend dependencies are required. Earlier template pages and assets are retained for existing links; legacy HTML pages are excluded from search indexing.
