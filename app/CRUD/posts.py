from sqlalchemy.orm import Session
from app.ORM.models.posts import PostsModel
from app.schemas.requests.posts import (
    CreatePostsRequestSchema
)
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

def create_post(db: Session, post: CreatePostsRequestSchema, createUser_id: str):
    try:
        post_as_dict = jsonable_encoder(post)
        post = PostsModel(**post_as_dict, created_by=createUser_id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )

def get_post(db: Session, post_id: int):
    try:
        post = db.query(PostsModel).get(post_id)
        if post == None:
            raise HTTPException(
                status_code=404,
                detail='Not found'
            )
        return post
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )

def delete_post(db: Session, post_id: int):
    try:
        post = db.query(PostsModel).get(post_id)
        if post == None:
            raise HTTPException(
                status_code=404,
                detail='Not found'
            )
        db.delete(post)
        db.commit()
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )

def get_posts_paginated(db: Session, page: int, limit: int):
    try:
        return db.query(PostsModel) \
            .offset(page*limit) \
            .limit(limit) \
            .all()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )
