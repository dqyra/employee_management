from typing import Optional
from wsgiref.validate import validator

from pydantic import BaseModel, constr


class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    employee_id: int

    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    name: str
    surname: str
    email: str
    age: int
    working_hours: int


class EmployeeCreate(EmployeeBase):
    password: str


class Employee(EmployeeBase):
    id: int
    tasks: list[Task] = []

    class Config:
        from_attributes = True


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    working_hours: Optional[int] = None
    age: Optional[int] = None

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    employee_id: Optional[int] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
