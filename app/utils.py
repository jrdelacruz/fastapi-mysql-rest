import logging
from fastapi import HTTPException

logging.basicConfig(level=logging.DEBUG)

def execute_query(db, query, values=None):
    with db.cursor() as cursor:
        try:
            cursor.execute(query, values)
            db.commit()
            return cursor.fetchall()
        except Exception as e:
            db.rollback()
            raise e

def handle_error(error):
    if isinstance(error, pymysql.err.IntegrityError):
        logging.error("Data integrity error: %s", error)
        raise HTTPException(status_code=400, detail="Data integrity error")
    elif isinstance(error, pymysql.err.OperationalError):
        logging.error("Database unavailable: %s", error)  
        raise HTTPException(status_code=503, detail="Database unavailable")
    elif isinstance(error, pymysql.err.ProgrammingError):
        logging.error("Incorrect query syntax or invalid parameters: %s", error)
        raise HTTPException(status_code=400, detail="Incorrect query syntax or invalid parameters")
    elif isinstance(error, pymysql.err.DataError):
        logging.error("Invalid data supplied: %s", error)
        raise HTTPException(status_code=400, detail="Invalid data supplied")
    elif isinstance(error, pymysql.err.NotSupportedError):
        logging.error("Feature not supported by the database: %s", error)
        raise HTTPException(status_code=501, detail="Feature not supported by the database")
    elif isinstance(error, pymysql.err.InternalError):
        logging.error("Internal database error: %s", error)
        raise HTTPException(status_code=500, detail="Internal database error")
    else:  # Catch-all for unexpected errors 
        logging.exception("An unexpected error occurred: ")  
        raise HTTPException(status_code=500, detail="Internal server error") 



def create_data(db, table_name, data):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    try:
        execute_query(db, query, list(data.values()))
        return {"message": f"Data inserted into table '{table_name}'"}
    except Exception as e:
        return handle_error(e)

def update_data(db, table_name, data, where_clause):
    set_columns = ", ".join([f"{key} = %s" for key in data.keys()])
    query = f"UPDATE {table_name} SET {set_columns} WHERE {where_clause}"
    try:
        execute_query(db, query, list(data.values()))
        return {"message": f"Data updated in table '{table_name}'"}
    except Exception as e:
        return handle_error(e)

def delete_data(db, table_name, where_clause):
    query = f"DELETE FROM {table_name} WHERE {where_clause}"
    try:
        execute_query(db, query)
        return {"message": f"Data deleted from table '{table_name}'"}
    except Exception as e:
        return handle_error(e)

def execute_custom_query(db, query, values=None):
    try:
        result = execute_query(db, query, values)
        return {"data": result}
    except Exception as e:
        return handle_error(e)
