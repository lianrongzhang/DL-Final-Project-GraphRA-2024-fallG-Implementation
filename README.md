# Deep Learning Final Project - GraphRAG Implementation

This project integrates **Knowledge Graph** and **Retrieval-Augmented Generation (RAG)** technologies to enhance the accuracy and relevance of generative AI in specific domains. The implementation leverages Microsoft GraphRAG for experimentation and uses tools like Ollama LM-Studio for model deployment and testing.

## Project Overview

**GraphRAG** is a framework that combines Knowledge Graphs with Large Language Models (LLMs). By providing structured knowledge through Knowledge Graphs and retrieval techniques, GraphRAG effectively enhances the quality of language generation outputs.

## Environment Setup and Tools

### Tools Used

- **Ollama**: Supports Llama models.
- **LM-Studio**: Embedding model toolkit.
- **Chainlit**: Framework for interactive applications.

### Environment Setup

#### 1. Create Conda Environment

```bash
conda create -n GraphRAG python=3.12
conda activate GraphRAG
```

#### 2. Install Required Packages

```bash
pip install graphrag
ollama pull llama3
```

#### 3. Activate LM-Studio Model

Use the following model version:

```
nomic-ai/nomic-embed-text-v1.5-GGUF
```

#### 4. Prepare Files

Create a folder to store test text files:

```bash
mkdir -p ./ragtest/input
```

Download a test text file:

```bash
curl https://www.gutenberg.org/cache/epub/24022/pg24022.txt > ./ragtest/input/book.txt
```

### Execution Steps

#### 1. Initialize Setup

Initialize the index directory and set parameters:

```bash
python -m graphrag.index --init --root ./ragtest
```

#### 2. Modify Configuration File

Update the `settings.yaml` file to specify the LLM and embedding model. Ensure the following configurations are set:

- **LLM Model**: Specify the Llama model version.
- **Embedding Model**: Set it to `nomic-ai/nomic-embed-text-v1.5-GGUF`.

#### 3. Build Index

Index the text files:

```bash
python -m graphrag.index --root ./ragtest
```

#### 4. Run Demo

Execute GraphRAG test examples to validate the setup:

```bash
python -m graphrag.demo --root ./ragtest
```

## Project Results

This implementation demonstrates the potential of GraphRAG technology in enhancing the quality and accuracy of generated outputs by leveraging Knowledge Graphs and retrieval-augmented techniques. The experiment showcases the value of structured knowledge in generative AI tasks.

---

For any issues or questions, please feel free to reach out via the project repository or contact the development team.
