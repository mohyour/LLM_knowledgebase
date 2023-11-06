import shutil
import pandas as pd
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.schema.document import Document
from app import logger


documents_store = {
    "hello.txt": "Hello, this document is just to say hello",
    "railway.txt": "Stephenson is considered the renowned as the 'Father of Railways'",
    "promo.pdf": "This promo is valid till 31 January 2024 and you definitely don't want to miss out on these prizes.",
    "beer.pdf": "Hold my beer!",
    "stephen.txt": "Stephenson was considered by the Victorians as a great example of diligent application and thirst for improvement to railway",
    "greetings.pdf": "A warmth hello from your great pub. We serve or beer cold"
}

# Create embedding
embeddings = SentenceTransformerEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L12-v2")


def create_knowledge_base(doc_name: str, knowledge_base: str):
    """
    Creates a new knowledge base if it doesn't exist.
    Raise exception if knowledge base already exist

    Parameters
    ----------
    doc_name: str
        document name to be added to knowledge base when created
    knowledge_base: str
        Name of knowledge base to create
    """
    logger.info(f"create_knowledge_base(): {(doc_name, knowledge_base)}")

    if os.path.exists(knowledge_base):
        logger.error("knowledge base already exists, update knowledge base")
        raise Exception
    logger.info("Creating new knowledge base... and adding document")
    add_document_to_knowledge_base(doc_name, knowledge_base)


def delete_knowledge_base(knowledge_base: str):
    """
    Deletes a knowledge base if it exist.
    Raise exception if knowledge base does not exist

    Parameters
    ----------
    knowledge_base: str
        Name of knowledge base to be deleted
    """
    logger.info(f"delete_knowledge_base(): {(knowledge_base)}")
    try:
        shutil.rmtree(knowledge_base)
    except OSError as e:
        logger.error("Error: %s - %s." % (e.filename, e.strerror))
        raise OSError


def add_document_to_knowledge_base(doc_name: str, knowledge_base: str):
    """
    Adds document to an existing knowledge base. Creates
    knowledge base if it does not exist

    Parameters
    ----------
    doc_name: str
        document name to be added to knowledge base
    knowledge_base: str
        Name of knowledge base to add document to
    """
    logger.info(f"add_document_to_knowledge_base(): "
                f"{(doc_name, knowledge_base)}")
    doc = documents_store.get(doc_name)
    if not doc:
        logger.error('Document not in document store')
        raise Exception

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    metadata = {'source': doc_name}
    docs = [Document(page_content=x, metadata=metadata)
            for x in text_splitter.split_text(doc)]

    if os.path.exists(knowledge_base):
        try:
            update_knowledge_base(docs, knowledge_base)
        except Exception:
            logger.error("add_document_to_knowledge_base(): "
                         "Cannot add document to knowledge base")
            raise Exception
    else:
        logger.info("add_document_to_knowledge_base(): Knowledge base does "
                    "not exist, creating knowledge base")
        db = FAISS.from_documents(docs, embeddings)
        db.save_local(knowledge_base)


def update_knowledge_base(docs: list, knowledge_base: str):
    """
    Updates existing knowledge base with new document

    Parameters
    ----------
    docs: list
        Document embeddings to be updated to knowledge base
    knowledge_base: str
        Name of knowledge base to update
    """
    new_db = FAISS.from_documents(docs, embeddings)
    db = FAISS.load_local(knowledge_base, embeddings)
    db.merge_from(new_db)
    db.save_local(knowledge_base)


def find_similar_document(query_doc: str, knowledge_base: str):
    """
    Retrieve similar documents from a knowledge base given a query document

    Parameters
    ----------
    query_doc: str
        Query document name
    knowledge_base: str
        Knowledge base to query

    Returns
    -------
    list
        A list of similar documents
    """
    logger.info(f"find_similar_document(): {(query_doc, knowledge_base)}")
    query_text = documents_store.get(query_doc)
    try:
        db = FAISS.load_local(knowledge_base, embeddings)
        query_result = db.similarity_search_with_score(query_text)
    except Exception:
        logger.error("find_similar_document(): Error occurred while "
                     "getting similar documents")
        raise Exception
    return query_result


def store_to_dataframe(store):
    """
    Load Vector db store into DataFrame

    Parameters
    ----------
    store: Any
        Vector db to load into DataFrame

    Returns
    -------
    DataFrame
        Panda dataframe holding data from vector db
    """
    rows = []
    store_dict = store.docstore._dict
    for key in store_dict.keys():
        name = store_dict[key].metadata['source'].split('/')[-1]
        content = store_dict[key].page_content
        rows.append({"chunk_id": key, "document": name, "content": content})
    store_dataframe = pd.DataFrame(rows)
    return store_dataframe


def delete_document_from_knowledge_base(document, knowledge_base):
    """
    Deletes a document from knowledge base

    Parameters
    ----------
    documents: str
        Name of document to delete from knowledge base
    knowledge_base: str
        Knowledge base to delete from

    Returns
    -------
    list
        A list of similar documents
    """
    logger.info(f"delete_document(): {(document, knowledge_base)}")
    try:
        db = FAISS.load_local(knowledge_base, embeddings)
        store_df = store_to_dataframe(db)
        chunks_list = store_df.loc[store_df["document"] ==
                                   document]["chunk_id"].tolist()
        db.delete(chunks_list)
    except Exception:
        logger.error("delete_document_from_knowledge_base(): Cannot delete "
                     "document from knowledge base")
        raise Exception
    db.save_local(knowledge_base)
