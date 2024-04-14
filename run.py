from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.v1.routes import router as apiv1_router 

app = FastAPI()

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Determine the appropriate status code
    status_code = exc.status_code if isinstance(exc, HTTPException) else 500

    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "data": None,
            "message": str(exc)  # Provide the original error message
        }
    )

app.include_router(apiv1_router, prefix="/api/v1")  # Mount API routes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)