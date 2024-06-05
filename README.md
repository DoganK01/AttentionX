# AttentionRX: Reflection Type Agent for Medical Symptom Identification Program 💊🩺(UNDER DEVELOPEMENT)
</p>
<p align="center">
  <img src="assets/attentionrx.webp" width="50%" height="50%">
</p>

![Langchain](https://img.shields.io/badge/-Langchain-000?&logo=Langchain)
![OpenAI](https://img.shields.io/badge/-OpenAI-000?&logo=Data)
![Qdrant](https://img.shields.io/badge/-Qdrant-000?&logo=ArtificialIntelligence)
![DSPy](https://img.shields.io/badge/-DSPy-000?&logo=Database)
![Langgraph](https://img.shields.io/badge/-Langgraph-000?&logo=Database)
![RAFT](https://img.shields.io/badge/-RAFT-000?&logo=Database)
![vLLM](https://img.shields.io/badge/-vLLM-000?&logo=Database)

## Description

AttentionRX is an innovative software solution designed to enhance the analysis and interpretation of medical patient records by cross-referencing them with scholarly journal articles. By leveraging the latest advancements in artificial intelligence, AttentionX identifies symptoms from patient records and provides evidence-based prescription suggestions. The core technology stack includes Retrieval Augmented Generation (RAG), and Reflection type agents powered by Langchain, 
Llama3-OpenBioLLM-70B, Qdrant, DSPy and Langsmith, facilitating a robust and insightful analysis.

## Key Features

- **Symptom Identification:** Automated identification of symptoms and getting information about microbe based diseases from patient records using advanced LLMs.
- **Scholarly Journal Integration:** Cross-referencing symptoms with the latest scholarly articles and research for evidence-based diagnosis and prescription.
- **Evidence-Based Prescriptions:** Utilizes cutting-edge AI to suggest prescriptions based on the most current research and data.
- **Advanced Tech Stack:** Incorporates Retrieval Augmented Generation (RAG), Langchain, Llama3-OpenBioLLM-70B, Qdrant, DSPy and Langsmith for comprehensive data analysis and retrieval as well as for optimization and evaluation.

## Tech Stack

| Feature  | Tech Stack |
| -------------------------- | -------------------------- |
| Data Collection Tools          | Arxiv, Scholar, Tavily         |
| VectorDB, RAG  | Qdrant, Cohore Reranker  |
| System Building  | Langchain, Langgraph  |
| Fine-tuning  | RAFT + QLoRa  |
| Optimization  | DSPy  |
| Evaluation  | Langsmith  |
| Serving  | Langserve  |
| Deployement  | Modal, vLLM  |

## Folder Structure

- `data/`: Contains the dataset of medical patient records and scholarly journal articles
- `Reflection_Agents.ipynb`: Jupyter notebook containing samples and demonstrations of the project.

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


For samples and demonstrations, open the `notebooks` folder.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Reference

