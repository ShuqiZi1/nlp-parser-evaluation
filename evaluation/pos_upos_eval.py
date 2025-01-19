from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
import pandas as pd

# Evaluate POS and UPOS with accuracy, precision, recall, and F1-score
from scripts.data_preprocess import load_sentences


# Function to evaluate detailed POS and UPOS metrics for a single parser's output against the gold standard
def evaluate_pos_upos_detailed(gold, parser):
    """
    Calculates accuracy, precision, recall, and F1-score for both UPOS and POS tags
    and identifies mismatched tokens between the gold standard and parser output.

    Args:
        gold (dict): Gold standard data for a single sentence.
        parser (dict): Parser output data for a single sentence.

    Returns:
        dict: Metrics including accuracy, precision, recall, F1-score for UPOS and POS.
    """
    gold_upos = [tag[3] for tag in gold['tokens_tags']]  # Extract UPOS tags from gold standard
    gold_pos = [tag[2] for tag in gold['tokens_tags']]  # Extract POS tags from gold standard

    parser_upos = [tag[3] for tag in parser['tokens_tags']]  # Extract UPOS tags from parser output
    parser_pos = [tag[2] for tag in parser['tokens_tags']]  # Extract POS tags from parser output

    # Calculate UPOS metrics
    upos_precision, upos_recall, upos_f1, _ = precision_recall_fscore_support(
        gold_upos, parser_upos, average='weighted', zero_division=0
    )
    upos_accuracy = accuracy_score(gold_upos, parser_upos)

    # Calculate POS metrics
    pos_precision, pos_recall, pos_f1, _ = precision_recall_fscore_support(
        gold_pos, parser_pos, average='weighted', zero_division=0
    )
    pos_accuracy = accuracy_score(gold_pos, parser_pos)

    return {
        'upos_accuracy': upos_accuracy,
        'upos_precision': upos_precision,
        'upos_recall': upos_recall,
        'upos_f1': upos_f1,
        'pos_accuracy': pos_accuracy,
        'pos_precision': pos_precision,
        'pos_recall': pos_recall,
        'pos_f1': pos_f1
    }


# Function to compare multiple parser outputs against a gold standard
def compare_parsers_pos_upos(gold_standard, parser_outputs, parser_names):
    """
    Compares POS and UPOS tagging performance of multiple parsers against the gold standard.

    Args:
        gold_standard (list): List of gold standard sentences with token-level tags.
        parser_outputs (list): List of parser outputs (one list per parser).
        parser_names (list): List of parser names corresponding to the outputs.

    Returns:
        tuple: A summary of results for all parsers and detailed error analysis.
    """
    results = []  # Store overall results for each parser
    detailed_errors = []  # Store detailed mismatch information for each parser

    for parser_output, parser_name in zip(parser_outputs, parser_names):
        parser_result = {'Parser': parser_name, 'Sentences': []}

        for gold, parser in zip(gold_standard, parser_output):
            metrics = evaluate_pos_upos_detailed(gold, parser)

            # Extract mismatches for UPOS and POS tags
            gold_upos = [tag[3] for tag in gold['tokens_tags']]
            gold_pos = [tag[2] for tag in gold['tokens_tags']]
            parser_upos = [tag[3] for tag in parser['tokens_tags']]
            parser_pos = [tag[2] for tag in parser['tokens_tags']]

            upos_mismatches = [
                (i, g, p) for i, (g, p) in enumerate(zip(gold_upos, parser_upos)) if g != p
            ]
            pos_mismatches = [
                (i, g, p) for i, (g, p) in enumerate(zip(gold_pos, parser_pos)) if g != p
            ]

            parser_result['Sentences'].append({
                'text': gold['text'],  # Sentence text
                **metrics,  # Metrics for the sentence
                'upos_mismatches': upos_mismatches,  # Detailed UPOS mismatches
                'pos_mismatches': pos_mismatches  # Detailed POS mismatches
            })

            # Append detailed error information
            detailed_errors.append({
                'Parser': parser_name,
                'Sentence': gold['text'],
                'UPOS Mismatches': upos_mismatches,
                'POS Mismatches': pos_mismatches
            })

        results.append(parser_result)

    return results, detailed_errors


# Function to summarize comparison results into a table
def summarize_results_to_table(comparison_results):
    """
    Aggregates metrics across all sentences for each parser into a summary table.

    Args:
        comparison_results (list): List of parser results with sentence-level metrics.

    Returns:
        DataFrame: Summary table with average metrics for each parser.
    """
    summary_data = []

    for parser_result in comparison_results:
        total_sentences = len(parser_result['Sentences'])

        # Calculate average metrics across all sentences
        avg_upos_accuracy = sum(s['upos_accuracy'] for s in parser_result['Sentences']) / total_sentences
        avg_upos_precision = sum(s['upos_precision'] for s in parser_result['Sentences']) / total_sentences
        avg_upos_recall = sum(s['upos_recall'] for s in parser_result['Sentences']) / total_sentences
        avg_upos_f1 = sum(s['upos_f1'] for s in parser_result['Sentences']) / total_sentences

        avg_pos_accuracy = sum(s['pos_accuracy'] for s in parser_result['Sentences']) / total_sentences
        avg_pos_precision = sum(s['pos_precision'] for s in parser_result['Sentences']) / total_sentences
        avg_pos_recall = sum(s['pos_recall'] for s in parser_result['Sentences']) / total_sentences
        avg_pos_f1 = sum(s['pos_f1'] for s in parser_result['Sentences']) / total_sentences

        # Add summary metrics for the parser
        summary_data.append({
            'Parser': parser_result['Parser'],
            'UPOS Accuracy': avg_upos_accuracy,
            'UPOS Precision': avg_upos_precision,
            'UPOS Recall': avg_upos_recall,
            'UPOS F1': avg_upos_f1,
            'POS Accuracy': avg_pos_accuracy,
            'POS Precision': avg_pos_precision,
            'POS Recall': avg_pos_recall,
            'POS F1': avg_pos_f1
        })

    # Create and return a DataFrame with the summary data
    df = pd.DataFrame(summary_data)
    return df


# Function to generate a detailed error analysis table
def generate_detailed_error_table(detailed_errors):
    """
    Converts detailed error information into a DataFrame.

    Args:
        detailed_errors (list): List of detailed error dictionaries.

    Returns:
        DataFrame: Detailed error table with mismatches for each sentence.
    """
    error_data = []
    for error in detailed_errors:
        error_data.append({
            'Parser': error['Parser'],
            'Sentence': error['Sentence'],
            'UPOS Mismatches': error['UPOS Mismatches'],
            'POS Mismatches': error['POS Mismatches']
        })
    return pd.DataFrame(error_data)


# Load data from specified file paths
gold_standard = load_sentences('data/gold_standard.txt')
berkeley = load_sentences('data/berkeley_neural_output.txt')
corenlp = load_sentences('data/corenlp_output.txt')
allen = load_sentences('data/allen_output.txt')

# Compare parser outputs and generate metrics
parser_outputs = [berkeley, corenlp, allen]
parser_names = ["Berkeley", "CoreNLP", "Allen"]
comparison_results, detailed_errors = compare_parsers_pos_upos(gold_standard, parser_outputs, parser_names)

# Summarize results and generate error tables
summary_table = summarize_results_to_table(comparison_results)
detailed_error_table = generate_detailed_error_table(detailed_errors)


# Function to display and save results to files
def display_and_save_results(summary_table, detailed_error_table, output_dir="results"):
    """
    Displays and saves the summary metrics and detailed error analysis to files.

    Args:
        summary_table (DataFrame): Summary of average metrics for each parser.
        detailed_error_table (DataFrame): Detailed error analysis for each parser and sentence.
        output_dir (str): Directory to save the results.
    """
    import os

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Display results in the console
    print("Summary of POS and UPOS Metrics:")
    print(summary_table.to_string(index=False))
    print("\nDetailed Error Analysis:")
    print(detailed_error_table.to_string(index=False))

    # Save summary metrics to a text file
    summary_file = os.path.join(output_dir, "summary_metrics.txt")
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("Summary of POS and UPOS Metrics:\n")
        f.write(summary_table.to_string(index=False))
        f.write("\n")

    # Save detailed error analysis to a text file
    error_file = os.path.join(output_dir, "detailed_error_analysis.txt")
    with open(error_file, "w", encoding="utf-8") as f:
        f.write("Detailed Error Analysis:\n")
        f.write(detailed_error_table.to_string(index=False))
        f.write("\n")

    print(f"\nSummary saved to: {summary_file}")
    print(f"Detailed errors saved to: {error_file}")

# Call the function to display and save results
display_and_save_results(summary_table, detailed_error_table)
