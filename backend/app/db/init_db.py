from backend.app.db.session import Base, engine
from backend.app.models import user, order



def init_db():
    Base.metadata.create_all(bind=engine)


