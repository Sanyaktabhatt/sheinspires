import re


def detect_conflict(text_chunks):

    numbers = []

    for text in text_chunks:

        found = re.findall(r'\d+', text)

        numbers.extend(found)

    unique_numbers = set(numbers)

    if len(unique_numbers) > 1:
        return True

    return False