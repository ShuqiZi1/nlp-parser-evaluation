package com.example;

import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.semgraph.*;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.util.CoreMap;

import java.io.*;
import java.util.*;

public class CoreNLPExample {
    public static void main(String[] args) {
        // 1. Set up the CoreNLP pipeline
        Properties props = new Properties();
        props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,depparse");
        props.setProperty("parse.maxlen", "120");
        props.setProperty("pos.confidence", "1.0");
        props.setProperty("threads", "4"); // e.g., use 4 threads

        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

        // 2. Input sentences
        String[] sentences = {
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
        };

        // use stanza to get pos and upos
        String filePath = "stanza_output.txt";

        List<String> stanza_input = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            int index = 0;
            while ((line = br.readLine()) != null) {
                stanza_input.add(line);
                index++;
            }
        } catch (IOException e) {
            System.err.println("Error reading the file: " + e.getMessage());
        }

        // 3. Output file setup
        String outputFileName = "corenlp_output.txt";
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputFileName))) {
            String lineSeparator = System.lineSeparator();
            for (int i = 0; i < sentences.length; i++) {
                String text = sentences[i];
                writer.write((i + 1) + ". " + text + lineSeparator);

                // 4. Annotate the sentence
                Annotation document = new Annotation(text);
                pipeline.annotate(document);

                // 5. Extract sentences and process each one
                List<CoreMap> annotatedSentences = document.get(CoreAnnotations.SentencesAnnotation.class);
                for (CoreMap sentence : annotatedSentences) {

                    // Tokens & POS tags from stanza
                    writer.write(stanza_input.get(i));
                    writer.write(lineSeparator);


                    // Parse Tree
                    Tree parseTree = sentence.get(TreeCoreAnnotations.TreeAnnotation.class);
                    writer.write(parseTree.pennString());

                    // Dependency parsing
                    SemanticGraph dependencies = sentence.get(SemanticGraphCoreAnnotations.BasicDependenciesAnnotation.class);

                    List<String> dependencyRows = new ArrayList<>();

                    // Get ROOT node
                    IndexedWord root = dependencies.getFirstRoot();
                    if (root != null) {
                        String rootRow = String.format("%d\t%s\t%s\t%d", root.index(), root.word(), "ROOT", 0);
                        dependencyRows.add(rootRow);
                    }

                    // Iterate through other dependencies
                    for (SemanticGraphEdge edge : dependencies.edgeListSorted()) {
                        String dependent = edge.getDependent().word();
                        String relation = edge.getRelation().toString();
                        String governor = edge.getGovernor().word();
                        int dependentIndex = edge.getDependent().index();
                        int governorIndex = edge.getGovernor().index();

                        // Add the dependency relation to the list
                        String edgeRow = String.format("%d\t%s\t%s\t%d", dependentIndex, dependent, relation, governorIndex);
                        dependencyRows.add(edgeRow);
                    }

                    // Sort all dependencies by the index of the dependent word
                    dependencyRows.sort(Comparator.comparingInt(row -> Integer.parseInt(row.split("\t")[0])));

                    // Write to file
                    for (String row : dependencyRows) {
                        writer.write(row + System.lineSeparator());
                    }
                    writer.write(lineSeparator);
                }
            }
            System.out.println("Output written to " + outputFileName);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

