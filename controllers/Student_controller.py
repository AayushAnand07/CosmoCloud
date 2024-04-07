# controllers.py
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from models.Student_model import Address, Student
load_dotenv()

mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri)
db = client["Library"]
collection = db["Students"]

router = APIRouter()

@router.post("/students", status_code=201)
async def create_student(student: Student):
   
    result = collection.insert_one(student.dict())
    return {"id": str(result.inserted_id)}





@router.get("/students", response_model=List[Student], response_model_exclude_unset=True)
async def get_students(country: Optional[str] = None, age: Optional[int] = None):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}

    students = []
    for student in collection.find(query):
        student_data = {
            "name": student["name"],
            "age": student["age"],
            "address": Address(**student["address"]) if "address" in student else None
        }
        student_data["id"] = str(student["_id"])
        students.append(Student(**student_data))

    if not students:
        raise HTTPException(status_code=404, detail="No students found")

    return students


@router.get("/students/{id}", response_model=Student)
async def get_student(id: str):
   
    student = collection.find_one({"_id": ObjectId(id)})
    if student:
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    
    
    

@router.patch("/students/{id}", status_code=204)
async def update_student(id: str, student_data: dict):
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": student_data})
    if result.modified_count == 1:
        return {}
    else:
        raise HTTPException(status_code=404, detail="Cannot Update")
    
    

@router.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {}
    else:
        raise HTTPException(status_code=404, detail="Student not found")
