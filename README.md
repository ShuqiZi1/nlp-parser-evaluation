# L95 Final Assignment: Parser Evaluation Project

This project is a part of the L95 final assignment to evaluate and compare the performance of three parsers against a gold standard dataset. The objective is to critically analyze parser outputs through quantitative and qualitative methods and provide actionable insights based on linguistic knowledge.

## Task Objectives

1. **Evaluate Parsers:** Use two parsers to evaluate the gold standard dataset containing 10 sentences.
2. **Quantitative Analysis:** Compute metrics such as UAS, LAS, POS accuracy, and others.
3. **Qualitative Analysis:** Identify and classify error types, provide illustrative examples, and discuss downstream impacts.
4. **Reporting Standards:** Format the final report using the ACL 2023 Proceedings Template with a maximum of 8 pages (excluding references).

## Environment Requirements
- **Python Version:** Python 3.8 or higher
- **Java Version:** Java 8 or higher
- **Maven Version:** Maven 3.6 or higher

Ensure the above versions are installed and configured correctly in your environment.

## Features

- **Parser Support:**
  - AllenNLP
  - Berkeley Neural Parser
  - Stanza (Use with CoreNLP)
  - CoreNLP (Java-based)
- **Evaluation Metrics:**
  - Dependency Parsing: UAS, LAS, Root Accuracy, Complete Match Rate.
  - POS and UPOS Tagging: Accuracy, Precision, Recall, F1-score.
  - Constituency Parsing preparation for EVALB.
  - - **Error Analysis:**
  - Error classification with examples from the dataset
  - Severity analysis and downstream consequences
- **Gold Standard Comparisons:**
  - Evaluate parser output against provided gold standard sentences.
  - Analyze and categorize errors for qualitative and quantitative evaluation.

## Project Structure

```plaintext
.
├── java_core_nlp                # Java-related files
│   ├── pom.xml          # Maven configuration file (if using Maven)
│   └── src
│       └── main
│           ├── java
│               └── com/example/CoreNLPExample.java # Main Java program for parsing
├── data                # Input and parser output data
│   ├── allen_output.txt
│   ├── berkeley_neural_output.txt
│   ├── corenlp_output.txt
│   ├── gold_standard.txt
│   └── stanza_output.txt
├── evaluation          # Evaluation and comparison scripts
│   └── evalb_pre       # Constituency parse preparation for EVALB
│       ├── allen_constituency.txt
│       ├── berkeley_constituency.txt
│       ├── corenlp_constituency.txt
│       ├── evalb_prepare.py
│       └── gold_standard_improved_tree.txt
├── requirements        # Requirements files for different environments
├── results             # Results generated from evaluations
├── scripts             # Individual parser scripts
│   ├── allen_nlp_parser.py
│   ├── berkeley_neural_parser.py
│   ├── data_preprocess.py
│   └── stanza_parser.py
├── venv_library        # Virtual environments for different parsers
│   ├── allen_venv
│   ├── berkeley_venv
│   └── stanza_venv
└── README.md           # Project documentation
```


## Installation

To replicate the setup, create separate virtual environments for different parsers and install the required dependencies.

### AllenNLP
```bash
python -m venv allen_venv
source allen_venv/bin/activate  # On Windows: allen_venv\Scripts\activate
pip install -r requirements/allen_requirements.txt
```

### Berkeley Neural Parser
```bash
python -m venv berkeley_venv
source berkeley_venv/bin/activate
pip install -r requirements/berkeley_requirements.txt
```

### Stanza
```bash
python -m venv stanza_venv
source stanza_venv/bin/activate
pip install -r requirements/stanza_requirements.txt
```

### CoreNLP (Java & Maven)
1. **Install Maven**:
   - On macOS/Linux:
     ```bash
     brew install maven
     ```
   - On Windows:
     Download [Maven](https://maven.apache.org/download.cgi), extract it, and add `bin` to your system PATH.

2. **Set Up CoreNLP Project**:
   - Navigate to the `java-corenlp` directory in this project.

3. **Provided `pom.xml`**:
   The `pom.xml` file is included in the project and already contains the required dependencies for Stanford CoreNLP.

4. **Compile and Run**:
   - Compile the project:
     ```bash
     mvn compile
     ```
   - Run the program:
     ```bash
     mvn exec:java -Dexec.mainClass="com.example.CoreNLPExample"

### Evaluation
```bash
python -m venv eval_venv
source eval_venv/bin/activate
pip install -r requirements/eval_requirements.txt
```

### EVALB Tool
EVALB is used to evaluate constituency parses. Follow the steps below to set it up and run evaluations:

1. **Download EVALB**:
   - Clone the EVALB repository or download it from [EVALB GitHub](https://github.com/AbigailMcGovern/EVALB/).

2. **Compile EVALB**:
   - Navigate to the EVALB directory and run:
     ```bash
     make
     ```

3. **Run EVALB**:
   - Use the following command to evaluate constituency parses:
     ```bash
     ./EVALB evalb/evalb_pre/gold_constituency.txt evalb/evalb_pre/parser_constituency.txt > evalb/results.txt
     ```
     Replace `gold_constituency.txt` with the gold standard parses and `parser_constituency.txt` with the parser's output.

   - Example for Berkeley parser:
     ```bash
     ./EVALB evaluation/evalb_pre/gold_constituency.txt evaluation/evalb_pre/berkeley_constituency.txt > evaluation/evalb_pre/berkeley_eval_results.txt
     ```

4. **EVALB Output**:
   - Results include metrics such as precision, recall, and F1-score for constituency parsing.


## Usage

### Data Preprocessing
Preprocess the input files and gold standards:
```bash
python scripts/data_preprocess.py
```

### Running Parsers

#### AllenNLP Parser
```bash
source allen_venv/bin/activate
python scripts/allen_nlp_parser.py
deactivate
```

#### Berkeley Neural Parser
```bash
source berkeley_venv/bin/activate
python scripts/berkeley_neural_parser.py
deactivate
```

#### Stanza Parser
```bash
source stanza_venv/bin/activate
python scripts/stanza_parser.py
deactivate
```

#### CoreNLP Parser
```bash
cd java-corenlp
mvn exec:java -Dexec.mainClass="com.example.CoreNLPExample"
```


### Evaluation

#### Dependency Parsing Evaluation
Evaluate dependency parses against the gold standard:
```bash
source eval_venv/bin/activate
python evaluation/dependency_eval.py
deactivate
```

#### POS and UPOS Evaluation
Compare POS and UPOS metrics across parsers:
```bash
source eval_venv/bin/activate
python evaluation/pos_upos_eval.py
deactivate
```

#### Constituency Parsing Preparation
Prepare constituency parses for EVALB evaluation:
```bash
source eval_venv/bin/activate
python evaluation/evalb_pre/evalb_prepare.py
deactivate
```

#### Constituency Parsing Evaluation with EVALB
```bash
./EVALB evaluation/evalb_pre/gold_constituency.txt evaluation/evalb_pre/parser_constituency.txt > evalb/results.txt
```

### Gold Standard and Evaluation Guidelines

This project uses a gold standard provided in `gold_standard.txt`. Each sentence includes:

- The input text.
- Tokens and Penn Treebank tags.
- Constituency parse using a Penn Treebank style formalism.
- Dependency parse using a Universal Dependencies formalism (converted from RASP annotations).

#### Evaluation Process

- **Quantitative Evaluation:**
  - Use metrics such as UAS, LAS, POS/UPOS accuracy, and F1-scores to benchmark parsers.
- **Qualitative Evaluation:**
  - Categorize and analyze errors using illustrative examples from the dataset.
  - Discuss the severity and downstream consequences of error types.
  - Suggest modifications to the gold standard if needed, referencing external guidelines like Penn Treebank or dictionaries.

#### Reproducibility

- All evaluations are reproducible with provided scripts and version-controlled dependencies in the `requirements/` folder.
- Parser outputs and evaluation parameters are documented for transparency.

## Results

Evaluation results are stored in the `results/` directory. Key metrics for each parser are summarized, and detailed error analysis is provided. 


## Contributions

Contributions are welcome! Please fork the repository and submit a pull request for any changes or improvements.











