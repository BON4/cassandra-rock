#!/usr/bin/env python3

import sys
import argparse
import json
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

def parse_key_path(key_path):
    parts = key_path.split('.')
    parsed = []
    for part in parts:
        if part.isdigit():
            parsed.append(int(part))  # list index
        else:
            parsed.append(part)       # dict key
    return parsed

def coerce_value(raw):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        if raw.lower() in ['true', 'false']:
            return raw.lower() == 'true'
        elif raw.isdigit():
            return int(raw)
        else:
            return raw  # fallback: keep as string

def update_nested_key(data, key_path_list, new_value):
    current = data
    for i, part in enumerate(key_path_list[:-1]):
        next_part = key_path_list[i + 1]
        if isinstance(part, int):
            # Ensure list exists and is long enough
            if not isinstance(current, list):
                current = CommentedSeq()
            while len(current) <= part:
                current.append(CommentedMap() if isinstance(next_part, str) else None)
            if current[part] is None:
                current[part] = CommentedMap() if isinstance(next_part, str) else CommentedSeq()
            current = current[part]
        else:
            if part not in current or not isinstance(current[part], (dict, list)):
                current[part] = CommentedMap() if isinstance(next_part, str) else CommentedSeq()
            current = current[part]

    final_key = key_path_list[-1]
    if isinstance(final_key, int):
        if not isinstance(current, list):
            current = CommentedSeq()
        while len(current) <= final_key:
            current.append(None)
        current[final_key] = new_value
    else:
        current[final_key] = new_value

def main():
    parser = argparse.ArgumentParser(description="Update or create a key in a YAML file")
    parser.add_argument('--file', required=True, help='Path to YAML config file')
    parser.add_argument('--key', required=True, help='Dot-delimited key path (e.g. key1.key2.0.key3)')
    parser.add_argument('--value', required=True, help='New value to set (JSON format for lists/objects)')

    args = parser.parse_args()

    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(args.file, 'r') as f:
            config = yaml.load(f)
    except FileNotFoundError:
        print(f"File not found: {args.file}")
        sys.exit(1)

    key_path = parse_key_path(args.key)
    value = coerce_value(args.value)

    update_nested_key(config, key_path, value)

    with open(args.file, 'w') as f:
        yaml.dump(config, f)

    print(f"Set: {args.key} = {args.value}")

if __name__ == "__main__":
    main()
