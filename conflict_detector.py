import re


def detect_conflict(text_chunks):

    numbers = []

    for text in text_chunks:
        found = re.findall(r'\d+', text)
        numbers.extend(found)

    if len(set(numbers)) > 1:
        return True

    return False
