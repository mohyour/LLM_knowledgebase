# Documents Knowledge Base

Service to manage knowledge bases, add documents to a knowledge base and query the service to return similar documents.
Uses static document for now

Includes endpoints to:
- Create and delete knowledge bases
- Add and remove documents from a knowledge base
- Retrieve similar documents from a knowledge base given a query document

## Setup
### From local directory
Create a virtual environment using python3 and activate it.
```
 $ python -m venv venv
 $ source venv/bin/activate
```

Install requirements.txt
 ```
 $ pip install -r requirements.txt
 ```

Add to flask app to shell
```
    $ export FLASK_APP="app"
```

Run app with 
```
    $ flask run
```

Navigate to `http://127.0.0.1:5000/` to use api


### Using Docker
- Build Image
```
$ docker build --tag my_app .
```
Run docker image
```
$ docker run my_app
```

Navigate to `http://127.0.0.1:5000/` to use api



## Test
Run test with unittest using:

    $ python -m unittest
    
Run test with pytest using any command belowe. Pytest needs to be installed

    $ python -m pytest

or

    $ pytest

A test knowledge base is created and deleted withing the `vector_store` directory


## API Endpoints

| Endpoints	| Methods	| Description| Request data/param|
| ------------- | ------------- | -----| -----|
|/ | GET | Home message |
|/knowledge_base	| POST	| Creates a knowledge base | knowledge_base: str, document: str
|/knowledge_base	| DELETE	| Deletes a knowledge base | knowledge_base: str
|/document | POST | Adds document to knowledge base| knowledge_base: str, document: str
|/document	| DELETE	| Deletes a document from knowledge base| knowledge_base: str, documents: str
|/documents	| GET	| Gets similar documents for given query document | query params ==> query_doc: str, knowledge_base: str

#### Definitions and Usage
- knowledge_base(str): Vector db store representing knowledge base
- document(str): Document file name
- query_doc(str): Document file name used as query document for knowledge base

Requests content type is `json`.
Created vector db are stored by default in the `vector_store` directory. To create a knowledge base, a document needs to be included.
Creating new knowledge base with already existing name throws error
While adding document, if knowledge base does not exist, it creates one.

Below represents the in-memory data structure to store documents within application:
```json
{
    "hello.txt": "Hello, this document is just to say hello",
    "railway.txt": "Stephenson is considered the renowned as the 'Father of Railways'",
    "promo.pdf": "This promo is valid till 31 January 2024 and you definitely don't want to miss out on these prizes.",
    "beer.pdf": "Hold my beer!",
    "stephen.txt": "Stephenson was considered by the Victorians as a great example of diligent application and thirst for improvement to railway",
    "greetings.pdf": "A warmth hello from your great pub. We serve or beer cold"
    }
```
Document has to be from the above store. A valid document to be used in the endpoints will include any of "hello.txt", "railway.txt", "promo.pdf", "beer.pdf", "stephen.txt", "greetings.pdf",

## Improvements: Todo and possible improvements

- Load various custom document types from various source(s)
- Better Error handling with custom and detailed error message rather than general exceptions
- Check if document already in store before adding to knowledge base. To avoid duplicates
- Better and detailed logs for easy debugging
- Improved documentations
- Refactor to make it more readability and testing
- Split helper.py to each module
