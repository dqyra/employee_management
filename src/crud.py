from sqlalchemy.orm import Session

import schemas
from auth import get_password_hash
from src.models import Employee, Task
from schemas import EmployeeCreate, TaskCreate, EmployeeUpdate, TaskUpdate
from src import models


def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employee_by_email(db: Session, email: str):
    return db.query(models.Employee).filter(models.Employee.email == email).first()


def get_employees(db: Session):
    return db.query(models.Employee).all()


def get_all_tasks(db: Session):
    return db.query(models.Task).all()


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    hashed_password = get_password_hash(employee.password)
    db_employee = models.Employee(
        name=employee.name,
        surname=employee.surname,
        email=employee.email,
        age=employee.age,
        working_hours=employee.working_hours,
        password=hashed_password
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task: TaskCreate, employee_id: int):
    db_task = Task(**task.dict(), employee_id=employee_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_employee(db: Session, employee_id: int, employee_update: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        return None
    for key, value in employee_update.items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        return None
    for key, value in task_update.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_employee(db: Session, employee_id: int) -> bool:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee:
        db.delete(employee)
        db.commit()
        return True
    return False



def delete_task(db: Session, task_id: int) -> bool:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False
