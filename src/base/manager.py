from base.database import SessionLocal


class BaseManager():
    def __init__(self, model) -> None:
        self.model = model

    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @property
    def db(self):
        return self.db

    def create(self, instance):
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
