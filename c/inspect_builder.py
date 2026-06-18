with open('build_cs_ds_encyclopedia_c.py', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if "'''" in line:
            print(f"Line {i}: {line.strip()}")
