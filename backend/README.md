# YESID: Your Efficient and Smart Insurance Datastore
## Policy Insurance Chatbot Project - Backend

### Description
This project aims to provide users with a platform in which they can interact with an intelligent assistant for the Chilean insurance market.
This repository contains the project's backend, which includes an API that the frontend can consume to get the chatbot's responses.

**System capabilites:**
- Answer questions about any insurance policy in Chile (currently over 6k).
- Compare policies, highlighting the pros and cons of each one.
- Retrieve data from both an SQLite and a Chroma database, generating custom and specialized queries to contextualize the LLM. 
- Search news on the internet related to insurance policies.
- Conversation memory and persistent data storage (per user)
- Policy search engine with hybrid search.
- Generate new articles based on articles from two different policies.


### Technologies 
- Python
- Django (Backend API)
- SQLite (for policy data storage)
- ChromaDB (for policy similarity search)
- Langchain (Gemini Pro LLMs)
- PyTest (Testing)


### Project Structure
**|-- apps** --> Django apps in this project.<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;|-- ai --> Main app with the agents, prompts and Chroma connection.<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;|-- doc --> App containing the Policy model used for the project.<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;|-- users --> App for storing user information (including chat history)<br/>
|<br/>
**|-- common** --> Common functionalities across modules like logging and connecting to AWS<br/>
|<br/>
**|-- config** --> Project configuration (Django settings, middlewares, paths, etc)<br/>
|<br/>
**|-- EDA** --> Analysis of the initial and complete datasets (+ cleaning for the full dataset).<br/>
|<br/>
**|-- storage** --> Database and datasets folder, vital for the project to work.<br/>
|
**|-- test_apps** --> Database and datasets folder, vital for the project to work.<br/>
|<br/>
**|-- tmp** --> Temporal storage for API logs and other unimportant files.<br/>
|<br/>
**|-- utils** --> Utility functions for different purposes.<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;|-- extraction_legacy --> The original data extraction from AWS S3.<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;|-- extraction_pipeline --> The pipeline used to extract the policies from the data source.<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;|-- transform_load_pipeline --> The pipeline used to store the previously extracted data into SQLite and Chroma.<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;|-- validators --> Decorator and validation functions used in the project.<br/>
|<br/>
|-- pipelines_execution.ipynb --> You can execute the ETL pipelines here.<br/>
|-- download_datasets.ipynb --> Download the datasets **(CRITICAL for the project to work)**


### Setup and Installation
**Prequisites** - To run this, you will need Docker installed in your computer. You can refer to this installation guide: https://docs.docker.com/get-docker/

**Setup** -
Before running the project, you will need some files and dependencies:
1. The following environment variables, specified in `.env.example`:
- **DJANGO_SECRET_KEY**: Secret key for cryptographic signing in Django.
- **JWT_SECRET_KEY**: Secret key for encoding and decoding JWT tokens.
- **GOOGLE_APPLICATION_CREDENTIALS**: Path to JSON file with Google Cloud Project.
- **YOU_API_KEY_RAG**: API key for You.com (news API) RAG functionality.
- **YOU_API_KEY_SEARCH**: API key for You.com (news API) search functionality.
2. The JSON file containing the credentials for the Google Cloud Service Account to be able to connect to the project and use the Gemini models. (the path in GOOGLE_APPLICATION_CREDENTIALS should point to this file).

3. The databases that contain the policy information and embeddings. 
Run the `download_datasets.ipynb` to automatically download them.

**Installation** - Once we have everything ready, you can just run `docker comopose up` and the project will start to build and run on `http://localhost:8000`.