from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///predictions.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    input = Column(String)
    prediction = Column(String)
    prediction_date = Column(DateTime)

    def __repr__(self):
        return f"Prediction(id={self.id}, input={self.input}, prediction={self.prediction}, prediction_date={self.prediction_date})"

Base.metadata.create_all(engine)

def add_prediction(input, prediction):
    session = Session()
    prediction = Prediction(input=input, prediction=prediction, prediction_date=datetime.now())
    session.add(prediction)
    session.commit()
    session.close()

def get_predictions():
    session = Session()
    predictions = session.query(Prediction).all()
    session.close()
    return predictions

def delete_predictions():
    session = Session()
    session.query(Prediction).delete()
    session.commit()
    session.close()
