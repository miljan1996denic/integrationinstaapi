from sqlalchemy.orm import Session
from app.ORM.models.hashtags import HashtagsModel
from app.schemas.requests.hashtags import (
    CreateHashtagsRequestSchema
)
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

def create_tag(db: Session, tag: CreateHashtagsRequestSchema, createUser_id: str):
    try:
        tag_as_dict = jsonable_encoder(tag)
        tag = HashtagsModel(**tag_as_dict, created_by=createUser_id)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )

def get_tag(db: Session, tag_id: int):
    try:
        tag = db.query(HashtagsModel).get(tag_id)
        if tag == None:
            raise HTTPException(
                status_code=404,
                detail='Not found'
            )
        return tag
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )

def delete_tag(db: Session, tag_id: int):
    try:
        tag = db.query(HashtagsModel).get(tag_id)
        if tag == None:
            raise HTTPException(
                status_code=404,
                detail='Not found'
            )
        db.delete(tag)
        db.commit()
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )

def get_tags_paginated(db: Session, page: int, limit: int):
    try:
        return db.query(HashtagsModel) \
            .offset(page*limit) \
            .limit(limit) \
            .all()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )
