from fastapi import APIRouter, HTTPException
# mock DB
from models.tea_data import teas_db

router = APIRouter()

@router.get('/teas')
def get_teas():
  return teas_db

@router.get("/teas/{tea_id}")
def get_single_tea(tea_id: int):
  for tea in teas_db['teas']:
    if tea['id'] == tea_id:
        return tea
  raise HTTPException(status_code=404, detail="Tea not found")