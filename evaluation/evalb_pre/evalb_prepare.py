from scripts.data_preprocess import load_sentences


def save_constituency_parses_to_txt(file_path, output_file):
    """
    Save the `constituency_parse` from a file to a text file.

    Args:
        file_path (str): The path to the input data file.
        output_file (str): The path to the output text file.
    """
    data = load_sentences(file_path)  # Load the sentences from the file

    with open(output_file, "w", encoding="utf-8") as f:
        for i, sentence in enumerate(data):
            f.write(sentence['constituency_parse'])
            f.write("\n")  # Add spacing between sentences

    print(f"Saved constituency parses to {output_file}")


# Save the constituency parses for each file
save_constituency_parses_to_txt(
    'data/berkeley_neural_output.txt',
    'evaluation/evalb_pre/berkeley_constituency.txt'
)
save_constituency_parses_to_txt(
    'data/corenlp_output.txt',
    'evaluation/evalb_pre/corenlp_constituency.txt'
)
save_constituency_parses_to_txt(
    'data/allen_output.txt',
    'evaluation/evalb_pre/allen_constituency.txt'
)
