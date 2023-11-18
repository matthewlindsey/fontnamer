# fontnamer

## About
A Python utility that renames OpenType (`.otf`) and TrueType (`.ttf`) fonts using the [fonttools](https://github.com/fonttools/fonttools) library. This forked version of Chris Simpkins' [fontname.py](https://github.com/chrissimpkins/fontname.py) script has been packaged to allow simple installation as a global command line tool using `pipx`.

Font renaming script for OpenType tables in CFF (.otf) and OT TrueType (.ttf) fonts

## Requirements
* Python 3.6 or later

## Dependencies
* [fonttools](https://github.com/fonttools/fonttools) Python library (4.0.0 or later)


## Usage

Once installed globally, `fontnamer` can be used as follows:

```
$ fontnamer family_name font_file...
```

The `fontnamer` command updates the name table records of `.ttf` and `.otf` files with appropriately formatted font names given the user-provided `family_name` and the style definition found within each `font_file`.

A few things to keep in mind:
- You can provide multiple `font_file` arguments
- Use quotes around `family_name` arguments that include spaces
- This tool edits the font files in place, so make copies beforehand if you you would like to preserve the fonts with their former names. (You can always rewrite them with the previous name if you forget or change your mind.)

### Details
To apply a new family name to a font file, `fontnamer` updates the following entries in its `name` table: Family Name (name ID 1).
Full Name (name ID 4), PostScript name (id 6), Typographic Family (id 16). For OpenType fonts with Compact Font Format data, `fonttools` also updates the `FontName`, `FullName`, and `FamilyName` records in the `CFF` table.


### Examples

```
$ fontnamer "Hack DEV" Hack-Regular.ttf
```

![fscw-hack](https://user-images.githubusercontent.com/4249591/32151555-2a456982-bcf4-11e7-8ec8-57f8dbbd40a4.png)


```
$ fontnamer "Source Code Pro DEV" SourceCodePro-Regular.otf
```

![fscw-scp](https://user-images.githubusercontent.com/4249591/32151559-2e58a688-bcf4-11e7-9d39-7c8accdc41a6.png)


```
$ fontnamer "DejaVu Sans Mono DEV" DejaVuSansMono-Bold.ttf
```

![fscw-djv](https://user-images.githubusercontent.com/4249591/32151564-3414a644-bcf4-11e7-93c3-93bc2bbaebdb.png)

These should all be detected as "different" fonts so that you can install them side-by-side with the pre-modified versions.

## Warnings
Many fonts have licences prohibiting modifications of any kind, including changes to font family names and other metadata. Please take the time to understand the licenses of any fonts you wish to rename and act accordingly.

## License

[MIT License](LICENSE)