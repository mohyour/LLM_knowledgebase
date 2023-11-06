from app.documents import bp
from app import helper, logger, store_path
from flask import request


@bp.post('/document')
def add_document():
    request_data = request.get_json()
    logger.info(f"add_document(): {request_data}")
    knowledge_base = request_data.get("knowledge_base")
    document = request_data.get("document")
    try:
        helper.add_document_to_knowledge_base(document,
                                              store_path+knowledge_base)
    except Exception:
        return {"error": "Cannot add document to knowledge base, "
                "check request data"}, 400
    return {"message": "Document added to knowledge base"}, 200


@bp.delete('/document')
def delete_document():
    request_data = request.get_json()
    logger.info(f"delete_document(): {request_data}")
    knowledge_base = request_data.get("knowledge_base")
    document = request_data.get("document")
    try:
        helper.delete_document_from_knowledge_base(document,
                                                   store_path+knowledge_base)
    except Exception:
        return {"error": "Cannot delete document, check request data"}, 400
    return {"message": "Document deleted from knowledge base"}, 200


@bp.get('/documents')
def get_similar_documents():
    logger.info(f"get_similar_documents(): {request.args}")
    query_doc = request.args.get('query_doc')
    knowledge_base = request.args.get('knowledge_base')
    try:
        similar_docs = helper.find_similar_document(query_doc,
                                                    store_path+knowledge_base)
    except Exception:
        return {"error": "Cannot get similar documents, "
                "check query params"}, 400
    response = []
    for docs in similar_docs:
        doc, score = docs
        response.append({"document": doc.metadata["source"],
                         "content": doc.page_content, "score": str(score)})

    return {"documents": response}, 200
