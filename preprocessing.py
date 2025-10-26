import re

def preprocess_transcript(text):
    """
    Basic preprocessing:
    - Remove timestamps like [00:03:12]
    - Remove extra whitespaces
    """
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    text = ' '.join(text.split())
    return text
