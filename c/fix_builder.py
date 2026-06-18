# fix_builder.py
# First, let's read the current content (which has some wrong ''') at the top)
with open("build_cs_ds_encyclopedia_c.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Clean up the top part of the file to remove the wrong ''') lines
# Lines 18 and 22 in our previous view were:
# 18: ''')
# 22: ''')
# Let's rebuild the clean content by filtering them out from the top 30 lines.
# We will search for and remove any ''') in the first 30 lines that are not part of a string.
cleaned_lines = []
for idx, line in enumerate(lines):
    if idx < 30 and line.strip() == "''')":
        continue
    cleaned_lines.append(line)

content = "".join(cleaned_lines)

# Now do the split by 'add_section('
parts = content.split("add_section(")
new_parts = [parts[0]]

for part in parts[1:]:
    # Each part represents a section: e.g. "HEADER", r'''...
    # The previous part should end with ''')
    prev = new_parts[-1].rstrip()
    if not prev.endswith("''')") and len(new_parts) > 1:
        # We need to append ''') to the previous part
        new_parts[-1] = new_parts[-1].rstrip() + "\n''')\n\n"
    new_parts.append(part)

fixed_content = "add_section(".join(new_parts)

# Let's also check if the MAIN string is properly terminated
# The last section is MAIN_C or similar.
# After that, we have the Python writer main() routine.
# Let's check if there is an unmatched string before 'def main():'
if "def main():" in fixed_content:
    main_parts = fixed_content.split("def main():")
    prev = main_parts[0].rstrip()
    if not prev.endswith("''')"):
        main_parts[0] = main_parts[0].rstrip() + "\n''')\n\n"
    fixed_content = "def main():".join(main_parts)

with open("build_cs_ds_encyclopedia_c.py", "w", encoding="utf-8") as f:
    f.write(fixed_content)

print("Builder script fixed successfully with smart parser!")
