from typing import Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
class TaskCreate(TaskBase):
    pass
class Task(TaskBase):
    id: int
    employee_id: int

    class Config:
        orm_mode = True

class EmployeeBase(BaseModel):
    name: str
    surname: str
    age: int
    working_hours: int

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id:int
    tasks:list[Task] = []

    class Config:
        orm_mode=True

class EmployeeUpdate(BaseModel):
    name: Optional[str]=None
    surname: Optional[str]=None
    working_hours: Optional[int]=None
    age: Optional[int]=None
    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: Optional[str]=None
    description: Optional[str]=None
    employee_id: Optional[int]=None

    class Config:
        from_attributes=True
