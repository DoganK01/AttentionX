# AttentionX: Reflection Type Agent for Medical Symptom Identification Program 💊🩺(UNDER DEVELOPEMENT)
</p>
<p align="center">
  <img src="assets/attentionrx.webp" width="100%" height="100%">
</p>

![Langchain](https://img.shields.io/badge/-Langchain-000?&logo=Langchain)
![OpenAI](https://img.shields.io/badge/-OpenAI-000?&logo=Data)
![Qdrant](https://img.shields.io/badge/-Qdrant-000?&logo=ArtificialIntelligence)
![DSPy](https://img.shields.io/badge/-DSPy-000?&logo=Database)
![Langgraph](https://img.shields.io/badge/-Langgraph-000?&logo=Database)
![RAFT](https://img.shields.io/badge/-RAFT-000?&logo=Database)
![vLLM](https://img.shields.io/badge/-vLLM-000?&logo=Database)

## Diagram

![Unbenanntes Diagramm drawio (3)](https://github.com/DoganK01/AttentionX/assets/98788987/06066a2b-7869-43fa-80e0-d190ea7f104b)


## Description

AttentionX is an innovative software solution designed to enhance the analysis and interpretation of medical patient records by cross-referencing them with scholarly journal articles. By leveraging the latest advancements in artificial intelligence, AttentionX identifies symptoms from patient records and provides evidence-based prescription suggestions. The core technology stack includes Retrieval Augmented Generation (RAG), and Reflection type agents powered by Langchain, 
Llama3-OpenBioLLM-70B, Qdrant, DSPy and Langsmith, facilitating a robust and insightful analysis.

A dataset is created using GPT4o compatbile with RAFT resarch paper. Using this dataset, Qwen3-14B is trained. After the training, evaluation done on test dataset which has the same format with train dataset. %88 accuracy was achieved. After the documents related to the vector database are loaded and stored, the system itself is set up. The patient record and a query must be entered as input. Depending on these two inputs, relevant articles and texts are collected from the Qdrant vector database, Arxiv, Scholar and Tavily search tool in parallel and prompt editing is done. Then, the LLM-based agent of the Reflection Agent type produces the necessary response and presents it to the user in a structured way.


## Key Features

- **Symptom Identification:** Automated identification of symptoms and getting information about microbe based diseases from patient records using advanced LLMs.
- **Scholarly Journal Integration:** Cross-referencing symptoms with the latest scholarly articles and research for evidence-based diagnosis and prescription.
- **Evidence-Based Prescriptions:** Utilizes cutting-edge AI to suggest prescriptions based on the most current research and data.
- **Advanced Tech Stack:** Incorporates Retrieval Augmented Generation (RAG), Langchain, Llama3-OpenBioLLM-70B, Qdrant, DSPy and Langsmith for comprehensive data analysis and retrieval as well as for optimization and evaluation.
- **RAFT:** Qwen3-14B Model was trained using RAFT training technique to enhance the RAG compatibility (to reduce the hallucination and get more accurate answers) of the model itself.
- **Reflection:** This simple example composes two LLM calls: a generator and a reflector. The generator tries to respond directly to the user's requests. The reflector is prompted to role play as a teacher and offer constructive criticism for the initial response.
The loop proceeds a fixed number of times, and the final generated output is returned. Generator LLM is trained Qwen3-14B itself and reflector is "Llama3-OpenBioLLM-70B" model which is an advanced open source language model designed specifically for the biomedical domain. Developed by Saama AI Labs, this model leverages cutting-edge techniques to achieve state-of-the-art performance on a wide range of biomedical tasks.



## Tech Stack

| Feature  | Tech Stack |
| -------------------------- | -------------------------- |
| Data Collection Tools          | Arxiv, Scholar, Tavily         |
| VectorDB, RAG  | Qdrant, Cohore Reranker  |
| System Building  | Langchain, Langgraph  |
| Fine-tuning  | RAFT + LoRa  |
| Optimization  | DSPy  |
| Evaluation  | Langsmith |
| Deployement  | Azure, Chainlit |

## Wandb Tracing
![image](https://github.com/user-attachments/assets/55cbe8b1-f671-45ab-8d7c-d9d81a800c19)
![image](https://github.com/user-attachments/assets/245aedef-ddcc-40f1-a5de-84c469821bc9)


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

