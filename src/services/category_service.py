from src.models.category import Category
from src.schemas.category import create_category , response_category , update_category
from src.config.database import dbsession
from fastapi import HTTPException


def find_category_by_name(db: dbsession , name :str):
    
    return db.query(Category).filter(Category.name == name).first()

def create_cat(db : dbsession , request : create_category):
    

    if find_category_by_name(db , request.name):
        raise HTTPException(status_code=400 , detail="Category with this name already exists")
    
    cat = Category(
         name = request.name

    )

    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def get_cat(db):
    return db.query(Category).all()

def update_cat(db, id: int, request: update_category):
    cat = db.query(Category).filter(Category.id == id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    existing_cat = find_category_by_name(db, request.name)
    if existing_cat and existing_cat.id != id:
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    cat.name = request.name
    db.commit()
    db.refresh(cat)
    return cat

def get_category_by_id(db , id:int):
    cat = db.query(Category).filter(Category.id == id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat
    
