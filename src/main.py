from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

import auth
import crud
import schemas
from database import SessionLocal, engine, Base
from auth import create_access_token, verify_password, get_password_hash
from schemas import  Token
Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_employee(db, email:str, password:str):
    emplyee = crud.get_employee_by_email(db, email)
    if not emplyee or not verify_password(password, schemas.Employee.password):
        return False
    return schemas.Employee

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_employee_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_employee(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = auth.decode_token(token)
    if payload is None:
        raise credentials_exception
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    user = crud.get_employee_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

@app.get("/emploees/me", response_model=schemas.Employee)
def read_users_me(current_employee: schemas.Employee = Depends(get_current_employee)):
    return current_employee

@app.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = crud.get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_employee(db=db, employee=employee)


@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@app.get("/employees/", response_model=list[schemas.Employee])
def read_employees(db: Session = Depends(get_db)):
    employees = crud.get_employees(db=db)
    return employees


@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_all_tasks(db)
    if not tasks:
        raise HTTPException(status_code=404, detail="There are no tasks in table")
    return tasks


@app.post("/employees/{employee_id}/tasks/", response_model=schemas.Task)
def create_task_for_employee(employee_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task, employee_id=employee_id)


@app.patch("/employee/{employee_id}", response_model=None)
async def update_employee_endpoint(employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    employee_data = employee.dict(exclude_unset=True)
    updated_employee = crud.update_employee(db, employee_id, employee_data)
    if updated_employee:
        return {"message": "Employee updated successfully", "employee": updated_employee}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@app.patch("/task/{task_id}", response_model=None)
async def update_task_endpoint(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db, task_id, task.dict(exclude_unset=True))
    if updated_task:
        return {"message": "Task updated successfully", "task": updated_task}
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/employee/{employee_id}", response_model=None)
async def delete_employee_endpoint(employee_id: int, db: Session = Depends(get_db)):
    if crud.delete_employee(db, employee_id):
        return {"message": "Employee deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@app.delete("/task/{task_id}", response_model=None)
async def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    if crud.delete_task(db, task_id):
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Task not found")
