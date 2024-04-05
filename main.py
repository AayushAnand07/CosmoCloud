from fastapi import FastAPI
from pymongo import MongoClient
from controllers.Student_controller import router as student_router
app = FastAPI()


app.include_router(student_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
