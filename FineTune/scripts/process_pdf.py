import openai
import os
import PyPDF2



# Initialize the OpenAI client with your specific API key
client = openai.OpenAI(api_key="api-key-goes-here")  # Replace with your actual API key

def read_pdf(file_path):
    """Reads a PDF file and returns the text content of each page as a list."""
    text_contents = []
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text_contents.append(page.extract_text())
    return text_contents

def send_to_openai(text_content):
    """Sends the given text content to the OpenAI GPT-4 model and returns the response."""
    try:
        prompt = f"""
        Describe in detail the memory map of the RK3399, including physical address ranges for various system components. Explain how virtual memory is implemented, including the use of the Memory Management Unit (MMU). Provide examples of memory-mapped I/O operations and how they relate to specific registers in the processor.
        {text_content}

        STRICTLY FOLLOW THIS SYNTAX FOR EACH, DO NOT ADD ANYTHING ELSE to the SYNTAX:
        {{
            "messages": [
                {{"role": "system", "content": "expert embedded systems engineer specializing in memory management for ARM-based processors"}},
                {{"role": "user", "content": "questions about the Rockchip RK3399 SoC used in the FriendlyElec NanoPi M4"}},
                {{"role": "assistant", "content": "response_to_question"}}
            ]
        }}
        {{
            "messages": [
                {{"role": "system", "content": "expert embedded systems engineer specializing in memory management for ARM-based processors"}},
                {{"role": "user", "content": "questions about the Rockchip RK3399 SoC used in the FriendlyElec NanoPi M4"}},
                {{"role": "assistant", "content": "response_to_question"}}
            ]
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are an expert computer architect who is specializing in the FriendlyElec NanoPi M4, with a focus on the Rockchip RK3399 SoC architecture. You are creating fine-tuning data on how we can simulate engineering creations with the FriendlyElec NanoPi M4."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.7,
            top_p=1
        )

        response_text = response.choices[0].message.content

        return response_text

    except Exception as e:
        print("An error occurred:", e)
        return None

def process_pdf(file_path, output_dir):
    """Processes the PDF and saves the responses in a single output file within the output directory."""
    text_contents = read_pdf(file_path)
    all_responses = ""

    for page_num, text_content in enumerate(text_contents):
        print(f"Processing page {page_num + 1}/{len(text_contents)} of {os.path.basename(file_path)}")
        response_text = send_to_openai(text_content)
        if response_text:
            all_responses += response_text + "\n\n"

    output_file_path = os.path.join(output_dir, os.path.basename(file_path).replace('.pdf', '_fine_tuning.json'))
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(all_responses)
    print(f"Finished processing {os.path.basename(file_path)}. Output saved to {output_file_path}")

def process_directory(directory_path):
    """Processes all PDF files within a directory and saves the fine-tuning data in a new folder."""
    output_dir = os.path.join(directory_path, 'processed_fine_tuning')
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(directory_path, file_name)
            process_pdf(file_path, output_dir)

if __name__ == "__main__":
    directory_path = r"/Users/drew/Development/OpenQ/NanoPi_M4/Datasheets"  # Specify the path to the directory containing your PDF files
    process_directory(directory_path)
