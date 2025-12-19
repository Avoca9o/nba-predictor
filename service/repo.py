from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from passlib.context import CryptContext

engine = create_engine('sqlite:///predictions.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    input = Column(String)
    prediction = Column(String)
    prediction_date = Column(DateTime)

    def __repr__(self):
        return f"Prediction(id={self.id}, input={self.input}, prediction={self.prediction}, prediction_date={self.prediction_date})"


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, role={self.role})"

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


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_username(username: str):
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user


def create_user(username: str, password: str, role: str):
    session = Session()
    existing_user = session.query(User).filter(User.username == username).first()
    if existing_user:
        session.close()
        raise ValueError(f"User with username {username} already exists")

    password_hash = hash_password(password)
    user = User(username=username, password_hash=password_hash, role=role)
    session.add(user)
    session.commit()
    session.close()
    return user


def has_admin():
    session = Session()
    admin = session.query(User).filter(User.role == "admin").first()
    session.close()
    return admin is not None
