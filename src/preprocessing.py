import re
import string

def clean_text(text):
    """
    Clean text for NLP.
    """

    if not isinstance(text, str):
        return ""

    text = text.lower()

    text = re.sub(r"\d+", "", text)

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    text = re.sub(r"\s+", " ", text)

    return text.strip()