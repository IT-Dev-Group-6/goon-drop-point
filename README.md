# goon-drop-point

Shared drop point for DCS World `.miz` mission files used by IT-Dev-Group-6.

## What's here

Raw `.miz` files — no scripts, no docs, just missions. These are working files shared across the group for testing, development, and reference.

## Usage

Clone the repo and drop `.miz` files directly in the root. Only `.miz` files are tracked (everything else is gitignored).

```bash
git clone git@github.com:IT-Dev-Group-6/goon-drop-point.git
```

## Notes

- `.miz` files are ZIP archives containing Lua tables — open with any ZIP tool or the DCS Mission Editor
- Don't rename files without coordinating with the group — scripts may reference filenames directly
