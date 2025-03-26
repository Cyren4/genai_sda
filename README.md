# Banking MLOps : Predicting Loan Defaults in Retail Banking

**Context:**

We are a new team specialising in LLMs and RAG.   

**Objective:**

Find a specific topic in which RAG can make an LLM more efficient.


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

## Contributors 
- Cyrena Ramdani
- Yoav COHEN
- Hoang Thuy Duong VU
- Salma LAHBATI



This project is a student project fulfilling the requirements of a GenAI Course.


## Source documentation
