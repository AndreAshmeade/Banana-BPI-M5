import json
import os

def reformat_json_file(input_file_path, output_file_path):
    """
    Reformats a JSON file by extracting conversations between user and assistant roles and saves the reformatted data to a new file.

    Args:
        input_file_path (str): Path to the input JSON file.
        output_file_path (str): Path to save the reformatted JSON file.
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            content = input_file.read()

        # Split the JSON objects by double newline
        json_objects = content.strip().split('\n}\n')
        reformatted_data = []

        for obj in json_objects:
            obj = obj.strip()
            if obj:
                if not obj.endswith('}'):
                    obj += '}'
                try:
                    data = json.loads(obj)
                    if 'messages' in data:
                        conversation = data['messages']
                        for i in range(1, len(conversation) - 1, 2):
                            if conversation[i]['role'] == 'user' and conversation[i + 1]['role'] == 'assistant':
                                reformatted_data.append({
                                    "messages": [
                                        {"role": "system", "content": conversation[0]['content']},
                                        {"role": "user", "content": conversation[i]['content']},
                                        {"role": "assistant", "content": conversation[i + 1]['content']}
                                    ]
                                })
                except json.JSONDecodeError as e:
                    print(f"Failed to decode JSON object: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(reformatted_data, output_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error processing file {input_file_path}: {e}")

def process_json_files_in_directory(directory_path):
    """
    Processes all JSON files in a directory, reformats them, and saves the reformatted files to a subdirectory.

    Args:
        directory_path (str): Path to the directory containing JSON files.
    """
    output_dir = os.path.join(directory_path, 'reformatted_fine_tuning')
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):
            input_file_path = os.path.join(directory_path, file_name)
            output_file_path = os.path.join(output_dir, f'reformatted_{file_name}')
            reformat_json_file(input_file_path, output_file_path)
            print(f"Processed {input_file_path} to {output_file_path}")


if __name__ == "__main__":
    directory_path = r"NanoPi_M4/Datasheets/processed_fine_tuning"  # Path to the directory containing your JSON files
    process_json_files_in_directory(directory_path)
