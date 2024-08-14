import re
import json
from pypdf import PdfReader

# Read PDF
pdf_file = "/home/paulj/niru/AppliedNLP/data/IPCC_AR6_WGII_TechnicalSummary.pdf"
reader = PdfReader(pdf_file)
texts = [page.extract_text().strip() for page in reader.pages]

# Filter and clean text
filtered_texts = texts[5: -5]  # Adjust indices based on content
cleaned_texts = [re.sub(r'\d+\nTechnical Summary', '', s) for s in filtered_texts]
cleaned_texts = [re.sub(r'\nTS', '', s) for s in cleaned_texts]
cleaned_texts = [re.sub(r'TS\n', '', s) for s in cleaned_texts]

# Extract key sections and generate questions
# Example process - you might want to improve this based on actual content
def extract_key_info(texts):
    key_info = []
    for text in texts:
        # Simple heuristics to extract sections
        if "Impact on Ocean" in text:
            key_info.append({
                "prompt": "What is the impact of climate change on the ocean?",
                "response": text
            })
        elif "Main Findings" in text:
            key_info.append({
                "prompt": "What are the main findings of the IPCC report?",
                "response": text
            })
        # Add more conditions based on the content
    return key_info

key_info = extract_key_info(cleaned_texts)

# Save to JSON
with open("dataset.json", "w") as f:
    json.dump(key_info, f, indent=4)

print(f"Generated {len(key_info)} instruction-response pairs.")
