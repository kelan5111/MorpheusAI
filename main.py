import json
import re


def fix_jsonl(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed = []
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            # Fix common issues
            line = re.sub(r'\\(?!["\\/bfnrt])', r'\\\\', line)  # Escape lone backslashes
            data = json.loads(line)
            fixed.append(json.dumps(data, ensure_ascii=False))
        except json.JSONDecodeError as e:
            print(f"❌ Error on line {i}: {e}")
            # Try to salvage it
            try:
                # Force escape newlines and backslashes
                line = line.replace('\n', '\\n').replace('\r', '\\n')
                data = json.loads(line)
                fixed.append(json.dumps(data, ensure_ascii=False))
            except:
                print(f"   Could not fix line {i}")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed))

    print(f"✅ Fixed file saved to {output_path} ({len(fixed)} entries)")


# Run it
fix_jsonl("data/train.jsonl", "/home/workdir/attachments/train_fixed.jsonl")
