import os
import time
from openai import OpenAI

# Initialize the OpenAI client with your specific API key
client = OpenAI(
    api_key="api-key-goes-here" # Replace with the company-provided API key
)

def upload_file(file_path):
    """Uploads a file to OpenAI and returns the file ID."""
    try:
        with open(file_path, "rb") as f:
            response = client.files.create(
                file=f,
                purpose='fine-tune'
            )
        print(response)
        file_id = response.id
        print(f"File {file_path} uploaded successfully with ID: {file_id}")
        return file_id
    except Exception as e:
        print(f"Error uploading file {file_path}: {e}")
        return None

def create_fine_tune(file_id):
    """Creates a fine-tuning job with the uploaded file ID."""
    try:
        response = client.fine_tuning.jobs.create(
            training_file=file_id,
            model="gpt-4o-mini-2024-07-18"  # Specify the base model to fine-tune
        )
        fine_tune_id = response.id
        print(f"Fine-tuning job created with ID: {fine_tune_id}")
        return fine_tune_id
    except Exception as e:
        print(f"Error creating fine-tuning job: {e}")
        return None

def monitor_fine_tune(fine_tune_id):
    """Monitors the fine-tuning job until it is complete."""
    while True:
        try:
            fine_tune_status = client.fine_tuning.jobs.retrieve(fine_tune_id)
            status = fine_tune_status.status
            print(f"Fine-tune job status: {status}")
            if status in ["succeeded", "failed"]:  # Check for terminal statuses
                break
            time.sleep(30)  # Wait for 30 seconds before checking again
        except Exception as e:
            print(f"Error monitoring fine-tuning job: {e}")
            break

if __name__ == "__main__":
    combined_jsonl_path = r'NanoPi_M4/Datasheets/processed_fine_tuning/reformatted_fine_tuning/combined_data.jsonl'  # Replace with the path to your combined JSONL file

    #Upload the combined JSONL file
    file_id = upload_file(combined_jsonl_path)
    if file_id:
        # Create and monitor the fine-tuning job
        fine_tune_id = create_fine_tune(file_id)
        if fine_tune_id:
            monitor_fine_tune(fine_tune_id)
    # fine_tune_id = "ftjob-xe4decKZxiRRom2sROopGOJk"
    # monitor_fine_tune(fine_tune_id)
