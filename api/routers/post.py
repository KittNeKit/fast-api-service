import os
from typing import List
from uuid import uuid4

import cachetools
from fastapi import APIRouter, Depends, File, HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from api.crud import create_post, delete_post, get_posts_by_user
from api.dependencies import get_current_user, get_db
from api.models import User
from api.schemas import Post, PostCreate

router = APIRouter()

cache = cachetools.TTLCache(maxsize=100, ttl=300)

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/addpost", response_model=Post)
def add_post(
        text: str,
        file: UploadFile = File(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    file_path = None

    if file:
        if file.size > 1 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payload too large",
            )

        filename = f"{uuid4()}.jpg"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

    post = PostCreate(text=text)
    db_post = create_post(db, post, current_user.id, file_path)
    return db_post


@router.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.email in cache:
        return cache[current_user.email]

    posts = get_posts_by_user(db=db, user_id=current_user.id)
    cache[current_user.email] = posts

    return posts


@router.delete("/deletepost/{post_id}", response_model=Post)
def delete_post_endpoint(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = delete_post(db=db, post_id=post_id, user_id=current_user.id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    return post
