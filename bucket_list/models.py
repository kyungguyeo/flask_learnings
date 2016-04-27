from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

###Set up DB

engine = create_engine('mysql://root@localhost')
Base = declarative_base()
try:
	engine.execute("CREATE DATABASE Bucketlister") #create db
	engine.execute("USE Bucketlister") # select new db
except:
	engine.execute("USE Bucketlister") # select new db
Session = sessionmaker(bind=engine)
session = Session()

###Create Tables

class Users(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	first_name = Column(String(50), nullable=False)
	last_name = Column(String(50), nullable=False)
	username = Column(String(50), nullable=False)
	email = Column(String(50), nullable=False)
	password = Column(String(200), nullable=False)


class Tasks(Base):
	__tablename__ = "tasks"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	task_description = Column(String(200), nullable=False)
	date_created = Column(DateTime)
	completed = Column(Boolean, default=False)
	user = relationship(Users)

Base.metadata.create_all(engine)
session.commit()