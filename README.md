# Webtoon Chatbot: Your Guide to the World of Webtoons

**Context:**

We are a team specializing in LLMs and RAG, passionate about efficient food!

**Objective:**

To create a specialized chatbot that can answer questions, provide recommendations, and discuss all things food-related, using the power of RAG.
Also allow you to get recipes based on what you have in youre fridge and will soon enable you to add your own recipe to its knowledge base. 

**Project Overview report:**
- Canvas - [Can RAG help you eat better](https://www.canva.com/design/DAGi3urCNRc/qY44G1L6n32EEHqqGp8YuA/edit?utm_content=DAGi3urCNRc&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) 
- Source Code - [GenAI project](https://github.com/Cyren4/genai_sda) 

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



## File structure (TBD)
```
├── README.md
└── .gitignore
```


**Next Steps**

1.  **Implement RAG:** Check out the `/src/rag` and `data_loading` folder to see how we're using implementing RAG.
2.  **Create Chatbot Interface:** Design the chatbot interface in `/src/components/chatbot.py`.
3.  **Data Acquisition:**Check out the `data_loading` folder to see how we're getting recipes data (scraping, API, manual curation).
4.  **Vector Database:** We tried various a vector database and integrate it.
5.  **LLM Integration:** Connect your LLM to the chatbot (qwe tried with Mistral, gemini and gemma)


## Contributors 
- Cyrena Ramdani
- Yoav COHEN


This project is a student project fulfilling the requirements of a GenAI Course.


## Source documentation

- [Marmiton scrapper](https://github.com/remaudcorentin-dev/python-marmiton/tree/master)
- [Gemini embedding](https://ai.google.dev/gemini-api/docs/models#text-embedding)