import pandas as pd
from scripts.data_preprocess import load_sentences


def evaluate_dependency_parses(gold, predictions):
    """
    Evaluate dependency parses against the gold standard.

    Args:
        gold (list): Gold standard dependency parses.
        predictions (list): Parser-generated dependency parses.

    Returns:
        pd.DataFrame: Sentence-level evaluation results.
        dict: Overall evaluation summary.
    """
    results = []

    for i, gold_sentence in enumerate(gold):
        pred_sentence = predictions[i]

        # Extract gold and predicted dependencies
        try:
            gold_deps = {(int(dep[0]), int(dep[3])): dep[2] for dep in gold_sentence["dependency_parse"]}
            pred_deps = {(int(dep[0]), int(dep[3])): dep[2] for dep in pred_sentence["dependency_parse"]}
        except ValueError as e:
            print(f"Error in sentence {i + 1}: {gold_sentence['text']}")
            print(f"Dependency parse: {gold_sentence['dependency_parse']}")
            raise e

        # Total dependencies
        total = len(gold_deps)

        # Calculate UAS (Unlabeled Attachment Score)
        uas = sum(1 for dep in gold_deps if dep in pred_deps)

        # Calculate LAS (Labeled Attachment Score)
        las = sum(1 for dep in gold_deps if dep in pred_deps and gold_deps[dep] == pred_deps[dep])

        # Calculate Root Accuracy
        gold_root = next((dep[0] for dep in gold_sentence["dependency_parse"] if dep[2] == "ROOT"), None)
        pred_root = next((dep[0] for dep in pred_sentence["dependency_parse"] if dep[2] == "ROOT"), None)
        root_acc = 1 if gold_root == pred_root else 0

        # Calculate Complete Match
        complete_match = 1 if gold_deps == pred_deps else 0

        # Append results for the current sentence
        results.append({
            "sentence": gold_sentence["text"],
            "UAS": uas / total if total > 0 else 0,
            "LAS": las / total if total > 0 else 0,
            "Root Accuracy": root_acc,
            "Complete Match": complete_match,
        })

    # Convert results to a DataFrame
    df = pd.DataFrame(results)

    # Summary of metrics
    summary = {
        "Average UAS": df["UAS"].mean(),
        "Average LAS": df["LAS"].mean(),
        "Root Accuracy": df["Root Accuracy"].mean(),
        "Complete Match Rate": df["Complete Match"].mean(),
    }

    return df, summary


if __name__ == "__main__":
    # Load gold standard and parser outputs
    gold_standard = load_sentences('data/gold_standard.txt')
    berkeley = load_sentences('data/berkeley_neural_output.txt')
    corenlp = load_sentences('data/corenlp_output.txt')
    allen = load_sentences('data/allen_output.txt')

    # Evaluate Berkeley parser
    berkeley_results, berkeley_summary = evaluate_dependency_parses(gold_standard, berkeley)
    print("Berkeley Parser Results:")
    print(berkeley_results)
    print("\nSummary:")
    print(berkeley_summary)

    # Save Berkeley results to a txt file
    with open("results/berkeley_dependency_results.txt", "w", encoding="utf-8") as f:
        f.write("Berkeley Parser Results:\n")
        f.write(berkeley_results.to_string(index=False))  # Save DataFrame as string
        f.write("\n\nSummary:\n")
        for key, value in berkeley_summary.items():
            f.write(f"{key}: {value}\n")

    # Evaluate CoreNLP parser
    corenlp_results, corenlp_summary = evaluate_dependency_parses(gold_standard, corenlp)
    print("\nCoreNLP Parser Results:")
    print(corenlp_results)
    print("\nSummary:")
    print(corenlp_summary)

    # Save CoreNLP results to a txt file
    with open("results/corenlp_dependency_results.txt", "w", encoding="utf-8") as f:
        f.write("CoreNLP Parser Results:\n")
        f.write(corenlp_results.to_string(index=False))
        f.write("\n\nSummary:\n")
        for key, value in corenlp_summary.items():
            f.write(f"{key}: {value}\n")

    # Evaluate Allen parser
    allen_results, allen_summary = evaluate_dependency_parses(gold_standard, allen)
    print("\nAllen Parser Results:")
    print(allen_results)
    print("\nSummary:")
    print(allen_summary)

    # Save Allen results to a txt file
    with open("results/allen_dependency_results.txt", "w", encoding="utf-8") as f:
        f.write("Allen Parser Results:\n")
        f.write(allen_results.to_string(index=False))
        f.write("\n\nSummary:\n")
        for key, value in allen_summary.items():
            f.write(f"{key}: {value}\n")

