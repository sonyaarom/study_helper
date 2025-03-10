#ask openai to generate a json from the text file
#json file should have this format:
# {
#     "stk_name": "University Name",
#     "url": "URL",
#     "application_dates": "Application Dates",
#     "entrance_test_date": "Entrance Test Date",
#     "entrance_test_online": "Entrance Test Online Boolean (True/False)",
#     "entrance_test_subjects": "Entrance Test Subjects",
#     "required_language_level": "Required Language Level",
#     "public": "Public Boolean (True/False)",
#     "hochshule_or_uni": "Hochshule or University",
#     "notes": "Notes"
# }

import json
import os
from openai import OpenAI
from config import config

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=config.openai_api_key)

def generate_json_from_text(text_file):
    """Generate JSON data from a text file using OpenAI."""
    # Read the text file
    with open(text_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Create the prompt for OpenAI
    prompt = f"""
    Extract information from the following text about a university's Studienkolleg program and return it in JSON format.
    
    The JSON should have this exact structure:
    {{
        "stk_name": "University Name",
        "url": "URL of the university's Studienkolleg page",
        "application_dates": "Application Dates",
        "entrance_test_date": "Entrance Test Date",
        "entrance_test_online": boolean (true/false),
        "entrance_test_subjects": "Entrance Test Subjects",
        "required_language_level": "Required Language Level",
        "public": boolean (true/false),
        "hochschule_or_uni": "hochschule" or "uni",
        "notes": "Any additional important information"
    }}
    
    Note: "hochschule_or_uni" should be "hochschule" if it's a University of Applied Sciences (Hochschule) or "uni" if it's a University. This determines whether students can apply to universities after finishing the Studienkolleg.
    
    Text:
    {text}
    """
    
    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured information from text about university programs."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1000
    )
    
    # Get the response content
    json_str = response.choices[0].message.content.strip()
    
    # Try to parse the JSON
    try:
        # Sometimes the model returns markdown-formatted JSON with ```json and ``` markers
        if json_str.startswith('```json'):
            json_str = json_str.split('```json')[1].split('```')[0].strip()
        elif json_str.startswith('```'):
            json_str = json_str.split('```')[1].split('```')[0].strip()
        
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw response: {json_str}")
        return None

def main():
    #get all files in the current directory in the universities folder
    text_files = [f for f in os.listdir('universities') if f.endswith('.txt')]
    
    # Process each file and combine results
    results = {}
    for text_file in text_files:
        university_name = text_file.split('.')[0]  # Get name from filename
        print(f"Processing {university_name}...")
        
        json_data = generate_json_from_text(text_file)
        if json_data:
            results[university_name] = json_data
            print(f"Successfully processed {university_name}")
        else:
            print(f"Failed to process {university_name}")
    
    # Save combined results
    with open('universities_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print(f"Saved data for {len(results)} universities to universities_data.json")

if __name__ == "__main__":
    main()
