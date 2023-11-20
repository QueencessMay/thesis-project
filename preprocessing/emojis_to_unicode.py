import re

def convert_text_to_unicode(input_text):
    # Regular expression pattern to identify emojis in the input text
    emoji_pattern = r"[^\w\s!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]"

    def replace_emoji(match):
        # Replace each emoji with its Unicode representation
        emoji_str = match.group(0)
        unicode_representation = " U+" + hex(ord(emoji_str))[2:].upper()

        return unicode_representation

    # Use the regular expression to replace emojis with their Unicode equivalents
    text_with_unicode = re.sub(emoji_pattern, replace_emoji, input_text)
    
    return text_with_unicode
