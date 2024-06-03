# AttentionRX: A Medical Symptom Identification Program 💊🩺
</p>
<p align="center">
  <img src="assets/attentionrx.webp" width="50%" height="50%">
</p>

![Python](https://img.shields.io/badge/-Python-000?&logo=Python)
![LLamaindex](https://img.shields.io/badge/-LLamaindex-000?&logo=Data)
![Nomic Embeddings](https://img.shields.io/badge/-Nomic%20Embeddings-000?&logo=ArtificialIntelligence)
![ChromaDB](https://img.shields.io/badge/-ChromaDB-000?&logo=Database)

## Description

AttentionRX is an innovative software solution designed to enhance the analysis and interpretation of medical patient records by cross-referencing them with scholarly journal articles. By leveraging the latest advancements in artificial intelligence, AttentionX identifies symptoms from patient records and provides evidence-based prescription suggestions. The core technology stack includes Retrieval Augmented Generation (RAG), and agents powered by LLamaindex, Nomic embeddings, and ChromaDB, facilitating a robust and insightful analysis.

## Key Features

- **Symptom Identification:** Automated identification of symptoms from patient records using advanced natural language processing techniques.
- **Scholarly Journal Integration:** Cross-referencing symptoms with the latest scholarly articles and research for evidence-based diagnosis and prescription.
- **Evidence-Based Prescriptions:** Utilizes cutting-edge AI to suggest prescriptions based on the most current research and data.
- **Advanced Tech Stack:** Incorporates Retrieval Augmented Generation (RAG), LLamaindex, Nomic embeddings, and ChromaDB for comprehensive data analysis and retrieval.

## Tech Stack

- Retrieval Augmented Generation (RAG)
- LLamaindex
- Nomic Embeddings
- ChromaDB

## Folder Structure

- `data/`: Contains the dataset of medical patient records and scholarly journal articles.
- `cli_script.py`: Command-line interface script to run the program.
- `AttentionX.ipynb`: Jupyter notebook containing samples and demonstrations of the project.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/AttentionX.git
   ```
2. Navigate to the project directory:
   ```
   cd AttentionX
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
AttentionX can be used through a Command Line Interface (CLI), Jupyter notebooks for interactive sessions, or directly integrated into your projects.

- **Data Folder:** Contains sample patient records and scholarly articles for testing and development purposes.
- **CLI Script:** For processing records through the terminal, navigate to the project directory and run:

- **Jupyter Notebook:** For interactive examples and tutorials, open the provided Jupyter notebook:

To run the program, use the following command:
```
python cli_script.py
```

To run preliminary document processing, use the following command:
```
python document_processor.py --doc_dir ./sample --vector_store_path ./chroma_db --collection_name your_collection_name --n_batches 1 --llm_model mistral 
```

For samples and demonstrations, open the `AttentionX.ipynb` Jupyter notebook.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Reference

- [Retrieval Augmented Generation (RAG)](https://arxiv.org/abs/2004.04906)
- [LLamaindex](https://docs.llamaindex.ai/en/stable/optimizing/advanced_retrieval/advanced_retrieval/)
- [Nomic Embeddings](https://www.nomic.ai/)
- [ChromaDB](https://docs.trychroma.com/)
