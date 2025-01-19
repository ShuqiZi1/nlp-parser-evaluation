import re


# Function to parse the input file
def load_sentences(file_path):
    sentences = []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()

    # Split into sentence blocks (based on numbering)
    sentence_blocks = re.split(r'(\d+\.\s)', data)[1:]
    for i in range(0, len(sentence_blocks), 2):
        sentence_info = {}
        sentence_number = sentence_blocks[i].strip()
        sentence_block = sentence_blocks[i + 1]

        # Extract different parts
        match = re.search(r'(.*?\n)(.*?)\n(\(.*\))\n(\d+\t.*)', sentence_block, re.DOTALL)

        if match:
            sentence_info['number'] = sentence_number
            sentence_info['text'] = match.group(1).strip()
            sentence_info['tokens_tags'] = [
                tuple(tok.split('\\')) for tok in match.group(2).strip().split('\t')
            ]

            # Process the constituency parse to remove outermost layer
            constituency_parse = match.group(3).replace('\n', '').strip()
            sentence_info['constituency_parse'] = clean_constituency_parse(remove_outer_layer(constituency_parse))

            sentence_info['dependency_parse'] = [
                line.split('\t') for line in match.group(4).strip().split('\n')
            ]

        sentences.append(sentence_info)
    return sentences


def clean_constituency_parse(constituency_parse):
    """
    Cleans up the constituency parse string by removing unnecessary spaces.

    Parameters:
    constituency_parse (str): The original constituency parse string.

    Returns:
    str: The cleaned constituency parse string.
    """
    # Replace multiple spaces with a single space
    # This ensures consistent spacing throughout the string
    constituency_parse = re.sub(r'\s+', ' ', constituency_parse)

    # Remove any unnecessary space after an opening parenthesis '('
    # For example, "( NP" becomes "(NP"
    constituency_parse = re.sub(r'\(\s+', '(', constituency_parse)

    # Remove any unnecessary space before a closing parenthesis ')'
    # For example, "NP )" becomes "NP)"
    constituency_parse = re.sub(r'\s+\)', ')', constituency_parse)

    return constituency_parse


# Function to remove the outermost layer of the constituency parse
def remove_outer_layer(tree):
    # Match the outermost layer and extract the inner tree
    match = re.match(r'^\((?:TOP|ROOT)\s+(.*)\)$', tree)
    return match.group(1) if match else tree




