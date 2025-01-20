import requests
from config import config

def extract_text_with_adobe_sensei(pdf_data):
    """
    Extracts text from a PDF using Adobe Sensei API (Document Cloud API).
    Args:
        pdf_data (bytes): PDF file content in binary format.
    Returns:
        str: Extracted text from the PDF.
    """
    
    # Headers for Adobe Sensei API
    headers = {
        "Authorization": f"Bearer {config.ADOBE_ACCESS_TOKEN}",
        "x-api-key": config.ADOBE_API_KEY,
        "Content-Type": "application/pdf"
    }

    # Upload the PDF and extract text
    try:
        response = requests.post(config.ADOBE_ENDPOINT, headers=headers, data=pdf_data)
        
        if response.status_code == 202:
            # Get the result URL from the response
            result_url = response.json().get("outputs", [{}])[0].get("location")
            
            # Poll for the extraction result
            text_response = requests.get(result_url, headers={"Authorization": f"Bearer {config.ADOBE_ACCESS_TOKEN}"})
            if text_response.status_code == 200:
                return text_response.text  # Extracted text content
            else:
                raise Exception(f"Error fetching extracted text: {text_response.status_code} {text_response.text}")
        else:
            raise Exception(f"Error with Adobe Sensei API: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Adobe Sensei OCR failed: {e}")
        return None
