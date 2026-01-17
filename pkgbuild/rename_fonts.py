#!/usr/bin/env python3
import sys
import os
from fontTools.ttLib import TTFont


def rename_font(font_path):
    try:
        tt = TTFont(font_path)
    except Exception as e:
        print(f"Failed to open {font_path}: {e}")
        return

    name_table = tt["name"]
    modified = False

    print(f"Processing: {font_path}")

    for record in name_table.names:
        # 1: Family, 4: Full Name, 16: Typographic Family
        if record.nameID in [1, 4, 16]:
            try:
                old_str = record.toUnicode()
            except UnicodeDecodeError:
                continue

            new_str = old_str

            # Rename NotoSansM -> Noto Mono
            if "NerdFont" in new_str and "Nerd Font" not in new_str:
                new_str = new_str.replace("NerdFont", " Nerd Font")

            # Rename NotoSansM -> Noto Mono
            if "NotoSansM" in new_str:
                new_str = new_str.replace("NotoSansM", "Noto Mono ")
            # Rename NotoMono -> Noto Mono
            elif "NotoMono" in new_str:
                new_str = new_str.replace("NotoMono", "Noto Mono ")
            # Rename NotoSans -> Noto Sans (only if not preceded by 'Noto ')
            elif "NotoSans" in new_str and "Noto Sans" not in new_str:
                new_str = new_str.replace("NotoSans", "Noto Sans ")

            # Clean up potential double spaces
            while "  " in new_str:
                new_str = new_str.replace("  ", " ")

            # Trim
            new_str = new_str.strip()

            if new_str != old_str:
                try:
                    encoding = record.getEncoding() or "utf_16_be"
                    record.string = new_str.encode(encoding)
                    modified = True
                    print(f"  [{record.nameID}] '{old_str}' -> '{new_str}'")
                except Exception as e:
                    print(f"  Error encoding '{new_str}': {e}")

    if modified:
        print(f"  Saving {font_path}...")
        try:
            tt.save(font_path)
        except Exception as e:
            print(f"  Failed to save: {e}")
    else:
        print("  No changes.")


def main():
    if len(sys.argv) < 2:
        print("Usage: rename_fonts.py <font_files...>")
        sys.exit(1)

    for f in sys.argv[1:]:
        rename_font(f)


if __name__ == "__main__":
    main()
