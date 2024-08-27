import os
import json

def convert_json_to_jsonl(json_file_path, jsonl_file_path):
    """Converts a JSON file to a JSONL file."""
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:
        for item in data:
            jsonl_file.write(json.dumps(item) + '\n')

def process_directory(directory_path):
    """Processes all JSON files within a directory and converts them to JSONL files."""
    jsonl_dir = os.path.join(directory_path, 'jsonl_files')
    os.makedirs(jsonl_dir, exist_ok=True)  # Create the jsonl_files directory if it doesn't exist

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(directory_path, file_name)
            jsonl_file_path = os.path.join(jsonl_dir, file_name.replace('.json', '.jsonl'))
            convert_json_to_jsonl(json_file_path, jsonl_file_path)
            print(f"Converted {json_file_path} to {jsonl_file_path}")

if __name__ == "__main__":
    directory_path = r'NanoPi_M4/Datasheets/processed_fine_tuning/reformatted_fine_tuning'  # Replace with the path to your directory containing JSON files
    process_directory(directory_path)
