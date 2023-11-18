#!/usr/bin/env python3

import os
import sys

from fontTools import ttLib

from utils import get_version, file_exists


def main():
    argv = sys.argv

    # command argument tests
    if len(argv) == 2 and argv[1] == "-v":
        sys.stderr.write(f"{get_version()}{os.linesep}")
        sys.exit(1)

    if len(argv) < 3:
        sys.stderr.write(f"Error: you did not provide enough arguments.{os.linesep}")
        sys.stderr.write(
            f"Usage:{os.linesep}  - fontnamer family_name font_file...{os.linesep}  - fontnamer -v{os.linesep}"
        )
        sys.exit(1)

    # begin parsing command line arguments
    try:
        font_name = str(argv[1])  # the first argument is the new typeface name
    except Exception as e:
        sys.stderr.write(
            f"Error: unable to convert argument to string. {e}{os.linesep}"
        )
        sys.exit(1)

    # all remaining arguments on command line are file paths to fonts
    font_path_list = argv[2:]

    # iterate through all paths provided on command line and rename to `font_name` defined by user
    for font_path in font_path_list:
        # test for existence of font file on requested file path
        if not file_exists(font_path):
            sys.stderr.write(
                f"Error: the path '{font_path}' does not appear to be a valid file path.{os.linesep}"
            )
            sys.exit(1)

        tt = ttLib.TTFont(font_path)
        namerecord_list = tt["name"].names

        style = ""

        # determine font style for this file path from name record nameID 2
        for record in namerecord_list:
            if record.nameID == 2:
                style = str(record)
                break

        # test that a style name was found in the OpenType tables of the font
        if len(style) == 0:
            sys.stderr.write(
                f"Error: unable to detect the font style from the OpenType name table in '{font_path}'. {os.linesep}"
            )
            sys.stderr.write("Could not to complete execution of the script.")
            sys.exit(1)
        else:
            # font family name
            nameID1_string = font_name
            # full font name
            nameID4_string = f"{font_name} {style}"
            # postscript name - no spaces allowed, should be dash delimited
            nameID6_string = f"{font_name.replace(" ", "")}-{style.replace(' ', '')}"
            # typographic family name
            nameID16_string = font_name

            # modify the opentype table data in memory with updated values
            for record in namerecord_list:
                if record.nameID == 1:
                    record.string = nameID1_string
                elif record.nameID == 4:
                    record.string = nameID4_string
                elif record.nameID == 6:
                    record.string = nameID6_string
                elif record.nameID == 16:
                    record.string = nameID16_string

            # CFF table naming for CFF fonts (only)
            if "CFF " in tt:
                try:
                    cff = tt["CFF "]
                    cff.cff[0].FamilyName = nameID1_string
                    cff.cff[0].FullName = nameID4_string
                    cff.cff.fontNames = [nameID6_string]
                except Exception as e:
                    sys.stderr.write(
                        f"Error: unable to write new names to CFF table: {e}"
                    )

        # write changes to the font file
        try:
            tt.save(font_path)
            print(
                f"Successfully updated '{font_path}' with the name '{nameID4_string}'"
            )
        except Exception as e:
            sys.stderr.write(
                f"Error: unable to write new name to OpenType name table for '{font_path}'. {os.linesep}"
            )
            sys.stderr.write(f"{e}{os.linesep}")
            sys.exit(1)
