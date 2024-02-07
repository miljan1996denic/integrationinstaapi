from sqlalchemy.orm import Session
from app.ORM.models.users import UsersModel
from app.schemas.requests.users import (
    CreateUsersRequestSchema
)
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

def create_user(db: Session, user: CreateUsersRequestSchema, createUser_id: str):
    try:
        user_as_dict = jsonable_encoder(user)
        user = UsersModel(**user_as_dict, created_by=createUser_id)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )

def get_user(db: Session, user_id: int):
    try:
        user = db.query(UsersModel).get(user_id)
        if user == None:
            raise HTTPException(
                status_code=404,
                detail='Not found'
            )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )

def delete_user(db: Session, user_id: int):
    try:
        user = db.query(UsersModel).get(user_id)
        if user == None:
            raise HTTPException(
                status_code=404,
                detail='Not found'
            )
        db.delete(user)
        db.commit()
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )

def get_users_paginated(db: Session, page: int, limit: int):
    try:
        return db.query(UsersModel) \
            .offset(page*limit) \
            .limit(limit) \
            .all()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )
