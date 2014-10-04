from sqlalchemy import create_engine, Column, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
engine = create_engine("sqlite:///todo.db", echo=True)
class TODO(Base):

    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)

    def __init__(self, task, status):
        """Constructor"""
        self.task = task
        self.status = status
        
def main():
    
    Base.metadata.create_all(engine)
    create_session = sessionmaker(bind=engine)
    session = create_session()
    
    session.add_all([
        TODO('Install SQLAlchemy', 1),
        TODO('Go to cmd prompt', 0),
        TODO('type the path', 0),
        TODO('practice the tutorials given', 1)
        ])
    session.commit()
if __name__ == "__main__":
    main()