from sqlalchemy.orm import Session

class Service:
    def __init__(self, db: Session) -> None:
        self.db = db
        