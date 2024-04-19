from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..model import schemas, models
from ..database import get_db
from app import oauth2
from typing import List

"""
Mindmap-related API calls
"""

router = APIRouter(prefix='/mindmaps', tags=['Mindmaps'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MindmapOut)
def create_mindmap(mindmap: schemas.MindmapCreate, db: Session = Depends(get_db)):
    new_mindmap = models.Mindmap(**mindmap.model_dump())
    try:
        db.add(new_mindmap)
        db.commit()
        db.refresh(new_mindmap)
        return new_mindmap
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error de integridad en la base de datos")
    
@router.get("/", response_model=List[schemas.MindmapOut])
def get_mindmaps(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                 limit: int = 10, skip: int = 0):
    
    mindmaps = db.query(models.Mindmap).filter(models.Mindmap.owner_id == current_user.id).limit(limit).offset(skip).all()
    return mindmaps

@router.get("/{id}", response_model=schemas.MindmapOut)  
def get_mindmap(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    mindmap = db.query(models.Mindmap).filter(models.Mindmap.id == id).first()

    if not mindmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mindmap with id: {id} was not found",
        )
    
    if mindmap.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return mindmap