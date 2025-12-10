# Connect to db
from sqlalchemy.orm import Session
from database import get_db

# API related helpers
from fastapi import APIRouter, HTTPException, Depends

# Model related items
from models.tea import TeaModel
from serializers.tea import TeaSchema, CreateTeaSchema, UpdateTeaSchema
from typing import List


router = APIRouter()


# First we need to make sure the db connection is active
# once the record is pulled, i want to convert it to JSON
# after the record is pulled & converted to JSON, i want to make sure it is the correct format

@router.get('/teas', response_model=List[TeaSchema])
def get_teas(db: Session = Depends(get_db)):
  return db.query(TeaModel).all()

@router.get("/teas/{tea_id}", response_model=TeaSchema)
def get_single_tea(tea_id: int, db: Session = Depends(get_db)):
  tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()
  if not tea:
    raise HTTPException(status_code=404, detail="Tea not found")
  return tea


@router.post("/teas", response_model=TeaSchema)
def create_tea(tea: CreateTeaSchema, db: Session = Depends(get_db)):
    new_tea = TeaModel(**tea.dict())
    db.add(new_tea)
    db.commit()
    db.refresh(new_tea)
    return new_tea

@router.put("/teas/{tea_id}", response_model=TeaSchema)
def update_tea(tea_id: int, tea: UpdateTeaSchema, db: Session = Depends(get_db)):
  db_tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()
  if not tea:
    raise HTTPException(status_code=404, detail="Tea not found")
  tea_data = tea.dict(exclude_unset=True)  # Only update the fields provided
  for key, value in tea_data.items():
        setattr(db_tea, key, value)

  db.commit()  # Save changes
  db.refresh(db_tea)  # Refresh to get updated data
  return db_tea

@router.delete("/teas/{tea_id}")
def delete_tea(tea_id: int, db: Session = Depends(get_db)):
    db_tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()
    if not db_tea:
        raise HTTPException(status_code=404, detail="Tea not found")

    db.delete(db_tea)  # Remove from database
    db.commit()  # Save changes
    return {"message": f"Tea with ID {tea_id} has been deleted"}
