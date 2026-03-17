def extract_result(text, start=None, end=None):
    """
    Extracts a substring from the text delimited by the start and end substrings.
    If start is not provided or not found, it begins from the start of the text.
    If end is not provided or not found, it goes up to the end of the text.

    Parameters:
    text (str): The given text
    start (str, optional): The start substring
    end (str, optional): The end substring

    Returns:
    str: The extracted substring
    """
    if not text:
        return ""

    # Determine the starting index
    if start:
        start_index = text.find(start)
        if start_index != -1:
            start_index += len(start)
        else:
            start_index = 0
    else:
        start_index = 0

    # Determine the ending index
    if end:
        end_index = text.find(end, start_index)
        if end_index == -1:
            end_index = len(text)
    else:
        end_index = len(text)

    # Extract the substring
    return text[start_index:end_index]




