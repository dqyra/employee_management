from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from src.models import Base
import crud, schemas
from schemas import EmployeeUpdate, TaskUpdate

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
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
async def update_employee_endpoint(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    employee_data = employee.dict(exclude_unset=True)
    updated_employee = crud.update_employee(db, employee_id, employee_data)
    if updated_employee:
        return {"message": "Employee updated successfully", "employee": updated_employee}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")


@app.patch("/task/{task_id}", response_model=None)
async def update_task_endpoint(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
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
