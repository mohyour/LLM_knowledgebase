from app.knowledge_base import bp
from flask import request
from app import helper, logger, store_path


@bp.post('/knowledge_base')
def create_knowledge_base():
    request_data = request.get_json()
    logger.info(f"create_knowledge_base(): {(request_data)}")
    knowledge_base = request_data.get("knowledge_base")
    document = request_data.get("document")
    try:
        helper.create_knowledge_base(document, store_path+knowledge_base)
    except Exception:
        return {"message": "Cannot create knowledge base, "
                "check request data and logs"}, 400
    return {"message": "Knowledge base created"}, 201


@bp.delete('/knowledge_base')
def delete_knowledge_base():
    request_data = request.get_json()
    logger.info(f"delete_knowledge_base() {request_data}")
    knowledge_base = request_data.get("knowledge_base")
    try:
        helper.delete_knowledge_base(store_path+knowledge_base)
    except Exception:
        return {"message": "Cannot delete knowledge base, "
                "check request data and logs"}, 400
    return {"message": "Knowledge base deleted"}, 200
