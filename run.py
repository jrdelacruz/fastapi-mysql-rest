from fastapi import FastAPI
from app.v1.routes import router as apiv1_router 

app = FastAPI()

app.include_router(apiv1_router, prefix="/api/v1")  # Mount API routes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)