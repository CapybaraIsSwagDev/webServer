import yaml

def parse_note_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if content.startswith('---'):
        # Split only at the first two '---'
        parts = content.split('---', 2)
        # parts[0] is empty (before first ---)
        # parts[1] is YAML metadata
        # parts[2] is Markdown body
        metadata = yaml.safe_load(parts[1])
        body = parts[2].strip()
    else:
        # No metadata, whole file is body
        metadata = {}
        body = content

    return metadata, body


print(parse_note_file("app/site/notes/example.md"))