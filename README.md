# Plant Health Monitoring — NLP & Machine Learning

**Automated Text Processing and Machine Learning for Plant Health Bulletins**

## Overview

This project explores the application of **Natural Language Processing (NLP)** and **Machine Learning (ML)** to plant health monitoring, with a particular focus on French *Bulletins de Santé du Végétal* (BSV).

Developed during a four-week research internship at the **ImViA laboratory**, in collaboration with Institut Agro Dijon, the project aims to transform unstructured agricultural reports into structured textual data that can be used for automated analysis and classification.

The main objective is to build a **modular and extensible machine learning pipeline** capable of processing textual data, comparing classification approaches, and supporting future applications in precision agriculture.

## Objectives

- **PDF text extraction:** investigate the extraction and segmentation of textual content from agricultural reports.
- **Data structuring:** identify recurring document patterns and explore rule-based methods to organize unstructured text.
- **Text preprocessing and vectorization:** experiment with Bag of Words, N-grams, TF-IDF and word embeddings.
- **Machine learning:** implement a flexible framework for supervised classification and unsupervised clustering.
- **Model evaluation:** explore performance metrics such as accuracy, precision, recall, F1-score and silhouette score.
- **Modular architecture:** design a structured JSON input format to manage samples, labels, vectorization settings and model metadata.

## Technical Stack

- **Language:** Python
- **PDF processing:** PyMuPDF
- **Natural Language Processing:** spaCy, NLTK, regular expressions
- **Machine Learning:** scikit-learn
- **Text vectorization:** Bag of Words, N-grams, TF-IDF and word embeddings
- **Dimensionality reduction:** TruncatedSVD
- **Data augmentation:** exploration of text augmentation techniques, including back-translation and synonym replacement
- **Data representation:** JSON

## Key Technical Challenges

### 1. Extracting structured information from PDFs

Agricultural bulletins vary in layout, formatting and terminology across regions and publication years. The project investigates several approaches to paragraph-title detection, combining textual patterns with document formatting characteristics.

Rule-based extraction and logical combinations of features were explored to improve the identification of relevant sections.

### 2. Building a flexible text classification pipeline

The machine learning component was designed to support multiple vectorization and classification algorithms rather than relying on a single model. This modular approach makes it possible to experiment with alternative methods depending on the dataset and classification task.

### 3. Preparing data for machine learning

The project considers the challenges associated with limited datasets, text labeling, data augmentation and the representation of textual samples and their metadata in a consistent JSON structure.

## Results and Contributions

- Developed and tested approaches for extracting and organizing text from plant health bulletins.
- Investigated the limitations of rule-based PDF parsing, particularly when document layouts vary.
- Established a modular framework for text classification using machine learning algorithms.
- Explored both supervised learning and unsupervised clustering approaches.
- Designed a JSON-based data structure to improve interoperability, traceability and future extensibility.
- Identified technical limitations and documented directions for further development.

**Scope note:** PDF extraction and structuring remained partially completed because of document complexity and time constraints. The machine learning component was operationally tested on datasets from this project and a previous student project. The end-to-end processing of heterogeneous BSV documents remains an area for improvement.

## Potential Applications

- Automated analysis of agricultural reports.
- Classification of plant disease descriptions.
- Identification of phytosanitary risk levels from textual observations.
- Integration of textual information with image-based crop monitoring systems.

These applications represent potential extensions of the work rather than a fully deployed agricultural decision-support system.

## Skills Demonstrated

`Python` · `Natural Language Processing` · `Machine Learning` · `Text Classification` · `Data Preprocessing` · `Feature Extraction` · `TF-IDF` · `scikit-learn` · `spaCy` · `PyMuPDF` · `Data Structuring` · `Research & Experimentation`

## Context

Research internship carried out over four weeks during the first year of engineering studies, within the ImViA research environment at Université Bourgogne Europe and Institut Agro Dijon.

The project contributes to the broader goal of making heterogeneous agricultural data easier to analyze and reuse in precision agriculture.

## Future Improvements

- Improve PDF parsing and paragraph reconstruction across different document layouts.
- Expand and validate the training dataset.
- Benchmark classification algorithms using consistent evaluation protocols.
- Improve the robustness of text labeling and preprocessing.
- Integrate the pipeline into a complete end-to-end workflow.
- Explore a user interface for agricultural researchers and practitioners.