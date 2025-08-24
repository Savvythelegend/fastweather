# performing CRUD operations on weather requests

from db import supabase
from datetime import datetime
TABLE = "weather_requests"
# CREATE
def create_request(data: dict) -> dict:
    try:
        result = supabase.table(TABLE).insert(data).execute()
        return result.data[0] if result.data else {"error": "No data returned from insert"}
    except Exception as e:
        print(f"Database error: {e}")  # Debug print
        return {"error": str(e)}
    
# READ ALL
def get_requests(filters: dict = None):
    query = supabase.table(TABLE)
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value) # just adds the filter 
    res = query.select("*").execute()
    return res.data

# READ ONE
def get_request_by_id(record_id: int):
    res = supabase.table(TABLE).select("*").eq("id", record_id).execute()
    return res.data[0] if res.data else {"error": "Not found"}

# UPDATE
def update_request(record_id: int, data: dict):
    res = supabase.table(TABLE).update(data).eq("id", record_id).execute()
    return res.data[0] if res.data else {"error": "Update failed"}

# DELETE
def delete_request(record_id: int):
    res = supabase.table(TABLE).delete().eq("id", record_id).execute()
    return {"deleted": True} if res.status_code == 200 else {"error": "Delete failed"}
