from allennlp.predictors.predictor import Predictor
from allennlp_models import pretrained
import spacy
from nltk import Tree

# Load SpaCy and AllenNLP models
nlp = spacy.load("en_core_web_sm")  # Load SpaCy's small English model for tokenization and POS tagging

# Load pretrained AllenNLP models for coreference resolution, constituency parsing, and dependency parsing
coref_predictor = pretrained.load_predictor("coref-spanbert")  # Coreference resolution model
constituency_predictor = pretrained.load_predictor("structured-prediction-constituency-parser")  # Constituency parser
dependency_predictor = pretrained.load_predictor("structured-prediction-biaffine-parser")  # Dependency parser


def format_constituency_tree(tree_str):
    """
    Converts a single-line constituency tree string into a clean, indented format.

    Args:
        tree_str (str): A single-line string representation of a constituency tree.

    Returns:
        str: A properly indented and readable format of the tree.
    """
    # Parse the tree string into an NLTK Tree object
    tree = Tree.fromstring(tree_str)
    # Return the indented format of the tree
    return tree.pformat()


# Input sentences for processing
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

# Output file to save results
output_file = "data/allen_output.txt"

# Open the output file for writing
with open(output_file, "w", encoding="utf-8") as f:
    for i, sentence in enumerate(sentences):
        # Write the sentence number and text to the file
        f.write(f"{i + 1}. {sentence}\n")

        # Tokenization and POS tagging with SpaCy
        doc = nlp(sentence)  # Tokenize the sentence and perform POS tagging
        for token in doc:
            # Write token, lemma, part of speech, and detailed tag to the file
            f.write(
                f"{token.text}\\{token.lemma_}\\{token.pos_}\\{token.tag_}\t"
            )
        f.write("\n")  # Newline for better separation

        # Constituency parsing
        constituency_result = constituency_predictor.predict(sentence=sentence)  # Predict the constituency tree
        formatted_tree = format_constituency_tree(constituency_result["trees"])  # Format the tree
        f.write(formatted_tree + "\n")  # Write the formatted tree to the file

        # Dependency parsing
        dependency_result = dependency_predictor.predict(sentence=sentence)  # Predict dependency structure
        for idx, (word, head, rel) in enumerate(zip(dependency_result["words"], dependency_result["predicted_heads"],
                                                    dependency_result["predicted_dependencies"])):
            # Write dependency parsing results: token index, word, relation, and head index
            f.write(f"{idx + 1}\t{word}\t{rel}\t{head}\n")
        f.write("\n")  # Separate results for each sentence

print(f"Improved results saved to {output_file}")
