import os
import json

def combine_jsonl_files(input_dir, output_file_path):
    """Combines all JSONL files in the input directory into a single JSONL file."""
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for file_name in os.listdir(input_dir):
            if file_name.endswith('.jsonl'):
                file_path = os.path.join(input_dir, file_name)
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    for line in input_file:
                        output_file.write(line)

if __name__ == "__main__":
    directory_path = 'NanoPi_M4/Datasheets/processed_fine_tuning/reformatted_fine_tuning'  # Replace with the path to your directory containing JSON files
    jsonl_dir = os.path.join(directory_path, 'jsonl_files')
    combined_jsonl_path = os.path.join(directory_path, 'combined_data.jsonl')

    # Combine all JSONL files into one
    combine_jsonl_files(jsonl_dir, combined_jsonl_path)
    print(f"Combined JSONL files into {combined_jsonl_path}")
