from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse 
from app.database import get_db_connection
from app.utils import execute_query, handle_error

router = APIRouter()

@router.get("/{table_name}")
async def read_data(table_name: str, db=Depends(get_db_connection)):
    query = f"SELECT * FROM {table_name}"
    try:
        result = execute_query(db, query)
        return JSONResponse(content={
            "status": 200,
            "data": result,
            "message": f"Data retrieved from table '{table_name}'"
        })
    except Exception as e:
        return handle_error(e)

@router.post("/{table_name}")
async def create_data(table_name: str, data: dict, db=Depends(get_db_connection)):
    result = create_data(db, table_name, data)
    return JSONResponse(content={
        "status": 201, 
        "message": result["message"] 
    })

@router.put("/{table_name}")
async def update_data(table_name: str, data: dict, where: str, db=Depends(get_db_connection)):
    result = update_data(db, table_name, data, where) 
    return JSONResponse(content={
        "status": 200, 
        "message": result["message"] 
    })

@router.delete("/{table_name}")
async def delete_data(table_name: str, where: str, db=Depends(get_db_connection)):
    result = delete_data(db, table_name, where)
    return JSONResponse(content={
        "status": 200, 
        "message": result["message"] 
    })

@router.post("/custom_query") 
async def custom_query(query: str, values: list = None, db=Depends(get_db_connection)):
    result = execute_custom_query(db, query, values)
    return JSONResponse(content={
        "status": 200,
        **result,
        "message": "Custom query executed successfully" 
    })
