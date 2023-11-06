from flask import Flask

import logging

logging.basicConfig(format="%(levelname)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Path to store knowledge base vector db
store_path = "vector_store/"


def create_app():
    app = Flask(__name__)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.knowledge_base import bp as kb_bp
    app.register_blueprint(kb_bp)

    from app.documents import bp as docs_bp
    app.register_blueprint(docs_bp)

    return app
