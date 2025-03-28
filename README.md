# Webtoon Chatbot: Your Guide to the World of Webtoons

**Context:**

We are a team specializing in LLMs and RAG, passionate about webtoons!

**Objective:**

To create a specialized chatbot that can answer questions, provide recommendations, and discuss all things webtoon-related, using the power of RAG.


## **Access our Deployed Application !** 

###  - [Application - TBD]() 

**Project Overview report:**
- Canvas : - [GenAI Presentation - TBD]() 

## Set-up Project 

1.  Clone the repository:

```bash
git clone https://github.com/Cyren4/genai_sda
cd genai_sda
```

2.  Activate virtual env
```shell
conda env create -f environment.yml
conda activate genai-rag
conda env update --file environment.yml --name genai-rag --prune 

```

3.  Launch streamlit application : 
```
streamlit run src/app.py
```


## Manual Deployement to Cloud Run 

- Set up environment variable : 
```bash
export PROJECT_ID=<my-project-id>
export REGION=europe-west1
```

- Connect to GCP and set the right project:
```bash
gcloud auth login
gcloud config set project $PROJECT_ID

```

## File structure 
```
├── README.md
└── .gitignore
```



**Key Improvements and Considerations**

*   **RAG Emphasis:** The introduction and other sections highlight the importance of RAG.
*   **New Pages:** The structure is set up for the new pages (RAG Implementation, Chatbot, Architecture).
*   **Dependencies:** The `environment.yml` file includes potential dependencies for web scraping and vector databases.

**Next Steps**

1.  **Implement RAG:** Build out the `/src/components/rag_implementation.py` file to show how we're using RAG.
2.  **Create Chatbot Interface:** Design the chatbot interface in `/src/components/chatbot.py`.
3.  **Data Acquisition:** Decide how you'll get webtoon data (scraping, API, manual curation).
4.  **Vector Database:** Choose a vector database and integrate it.
5.  **LLM Integration:** Connect your LLM to the chatbot.
6.  **Refine Content:** Continue to improve the text and explanations.



## Contributors 
- Cyrena Ramdani
- Yoav COHEN
- Hoang Thuy Duong VU
- Salma LAHBATI



This project is a student project fulfilling the requirements of a GenAI Course.


## Source documentation

- [Marmiton scrapper](https://github.com/remaudcorentin-dev/python-marmiton/tree/master)