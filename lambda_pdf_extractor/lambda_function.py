import base64
import json
import fitz  # PyMuPDF

def lambda_handler(event, context):
    try:
        # Decode base64 PDF
        file_content = base64.b64decode(event["body"])
        doc = fitz.open(stream=file_content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return {
            'statusCode': 200,
            'body': json.dumps({'text': text})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
