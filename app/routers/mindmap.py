from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..model import schemas, models
from ..database import get_db
from app import oauth2

"""
Mindmap-related API calls
"""

router = APIRouter(prefix='/mindmaps', tags=['Mindmaps'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MindmapOut)
def create_entity(mindmap: schemas.MindmapCreate, db: Session = Depends(get_db)):
    new_mindmap = models.Mindmap(**mindmap.model_dump())
    try:
        db.add(new_mindmap)
        db.commit()
        db.refresh(new_mindmap)
        return new_mindmap
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error de integridad en la base de datos")