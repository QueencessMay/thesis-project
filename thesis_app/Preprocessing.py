from . import EmojisToUnicode
from . import EmoticonsDictionary

def convert_text_to_lowercase(input_text):
    text_lowercase = input_text.lower()
    return text_lowercase

def preprocess_text(input_text):
    # Convert input text to lowercase
    text_lowercase = input_text.lower()
    
    # Convert text to Unicode using EmojisToUnicode
    text_unicode = EmojisToUnicode.convert_text_to_unicode(text_lowercase)
    
    # Transform emoticons using EmoticonsDictionary
    transformed_text = EmoticonsDictionary.transform_emojis_and_emoticons(text_unicode)
    
    return transformed_text




