#read pdf and turn it into csv
import pandas as pd
import pdfplumber

def pdf_to_csv(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        # Extract text from each page
        for page in pdf.pages:
            text += page.extract_text()
        
        # Split text into lines
        lines = text.split('\n')
        
        # Initialize lists to store data
        data = []
        current_entry = {}
        
        # Parse lines into structured data
        for line in lines:
            line = line.strip()
            if not line:
                if current_entry:
                    data.append(current_entry)
                    current_entry = {}
                continue
                
            if '@' in line:  # Email line
                current_entry['email'] = line
            elif 'Tel.' in line:  # Phone line
                current_entry['phone'] = line.replace('Tel.', '').strip()
            elif 'http' in line:  # Website line
                current_entry['website'] = line
            elif current_entry.get('name'):  # Address line
                current_entry['address'] = current_entry.get('address', '') + ' ' + line
            else:  # Name line
                current_entry['name'] = line
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Save to CSV
        output_path = pdf_path.replace('.pdf', '.csv')
        df.to_csv(output_path, index=False, encoding='utf-8')
        return output_path

pdf_to_csv("/Users/s.konchakova/study_helper/Kontakdaten-der-bundesweiten-Studienkollegs.pdf")
