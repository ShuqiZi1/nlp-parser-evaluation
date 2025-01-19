import stanza

# Download and initialize the Stanza pipeline for English
stanza.download(lang='en')  # Downloads the English language model for Stanza
nlp = stanza.Pipeline('en')  # Initializes the pipeline for processing English text

# Input list of sentences to be processed
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

# Define the output file name to save the processed results
output_file = "../data/stanza_output.txt"

# Open the output file for writing
with open(output_file, "w", encoding="utf-8") as file:
    # Process each sentence in the input list
    for sentence in sentences:
        doc = nlp(sentence)  # Analyze the sentence using Stanza
        for sent in doc.sentences:  # Iterate through the parsed sentences (should be one per input sentence)
            for word in sent.words:  # Iterate through the words in the sentence
                # Write the word's text, lemma, UPOS (universal part of speech), and XPOS (language-specific POS) to the file
                file.write(f"{word.text}\\{word.lemma}\\{word.upos}\\{word.xpos}\t")
        file.write("\n")  # Add a newline after each processed sentence

# Print a message indicating that processing is complete and the file has been saved
print(f"Processing complete. Output saved to {output_file}")
