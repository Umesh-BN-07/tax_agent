import re

def extract_income(text):
    match = re.search(r'(\d+)\s*lakh', text.lower())
    if match:
        return int(match.group(1)) * 100000
    return 0