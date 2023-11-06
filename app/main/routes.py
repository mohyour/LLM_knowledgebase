from app.main import bp


@bp.get('/')
def home():
    return {"data": "Home page"}
