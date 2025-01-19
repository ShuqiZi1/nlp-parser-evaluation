import benepar
from spacy import load

# Download the required Benepar model for constituency parsing
benepar.download('benepar_en3')

# Initialize the Benepar constituency parser with the downloaded model
parser = benepar.Parser("benepar_en3")

# Load a SpaCy model for dependency parsing and linguistic annotation
nlp = load("en_core_web_md")

# Input sentences
sentences = [
    "As she walked past it, the driver's glass started to open.",
    "With a handkerchief she wiped the sweat from her forehead.",
    "Prudently, they had diversified into banking and insurance, and as a result their influence was felt at the highest level.",
    "The arranged marriage would be the social event of the following year.",
    "When at last she spoke, her words were heavy and disjointed.",
    "The road to the coast was busy with traffic in both directions.",
    "The expected date came and went.",
    "She sighed at the irony of it all, the waste of it all.",
    "All through August the rain hardly stopped.",
    "Thank the gods he didn't have to know of this."
]


# Function to perform constituency and dependency parsing on a given sentence
# and return the results in a formatted string
def parse_sentence(sentence, index):
    # Generate constituency parse tree using Benepar
    constituency_tree = parser.parse(sentence)

    # Process the sentence using SpaCy for dependency parsing
    doc = nlp(sentence)
    # Extract tokens, their POS tags, and detailed morphological information
    tokens_pos = [(token.text, token.text.lower(), token.pos_, token.tag_) for token in doc]
    # Extract dependencies, including token index, word, dependency label, and head index
    dependencies = [(i + 1, token.text, token.dep_, token.head.i + 1 if token.head else 0) for i, token in enumerate(doc)]

    # Format the output to include original sentence, tokens with POS tags, constituency parse, and dependency relations
    formatted_output = f"{index + 1}. {sentence}\n"
    formatted_output += "".join([f"{text}\\{lower}\\{pos}\\{tag}\t" for text, lower, pos, tag in tokens_pos]).strip() + "\n"
    formatted_output += f"{constituency_tree}\n"
    formatted_output += "\n".join([f"{word_id}\t{word}\t{dep}\t{head}" for word_id, word, dep, head in dependencies]) + "\n"
    return formatted_output


# Parse all sentences in the list and save the formatted results to a file
output_file = "data/berkeley_neural_output.txt"

with open(output_file, "w") as f:
    for idx, sentence in enumerate(sentences):
        # Parse each sentence and write the result to the file
        parsed_output = parse_sentence(sentence, idx)
        f.write(parsed_output)
        f.write("\n")  # Add a blank line between sentences for readability

# Notify the user that parsing is complete and indicate the output file location
print(f"Parsing completed. Results saved to {output_file}")
