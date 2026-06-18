with open("append_chunk5.py", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if '"""' in line or "'''" in line:
            print(f"Line {i}: {line.strip()}")
