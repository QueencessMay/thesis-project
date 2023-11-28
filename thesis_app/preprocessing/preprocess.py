import re
import contractions

from . import emojis_to_unicode
from . import emoticons_dictionary

def convert_text_to_lowercase(input_text):
    #Convert text to lowercase
    text_lowercase = input_text.lower()

    return text_lowercase

def remove_special_characters(input_text):
    # Use regular expression to remove special characters
    processed_text = re.sub(r'[^\w\s\.-_+/]', '', input_text)

    return processed_text

def expand_contractions(text):
    # Expand contractions
    expanded_text = contractions.fix(text)

    return expanded_text


def preprocess_text(input_text, review_type):
    # Convert input text to lowercase
    text_lowercase = convert_text_to_lowercase(input_text)

    # Expand contractions
    expanded_text = expand_contractions(text_lowercase)

    if review_type == 'with':
        # Transform emoticons using Emoticons Dictionary
        transformed_text = emoticons_dictionary.transform_emoticons(expanded_text)
            
        # Convert text to Unicode using Emojis To Unicode
        text_unicode = emojis_to_unicode.convert_text_to_unicode(transformed_text)

        # Remove special characters
        processed_text = remove_special_characters(text_unicode)

        return processed_text
    else:
        # Remove special characters
        processed_text = remove_special_characters(expanded_text)

        return processed_text




