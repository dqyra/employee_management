from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String)
    surname = Column(String, index=True)
    age = Column(Integer)
    working_hours = Column(Integer)
    tasks = relationship("Task", back_populates="employee")


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employee", back_populates="tasks")




