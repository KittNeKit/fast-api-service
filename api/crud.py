from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.models import Post, User
from api.schemas import PostCreate, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        return False

    return user


def create_post(db: Session, post: PostCreate, user_id: int, file_path: str = None):
    db_post = Post(**post.dict(), owner_id=user_id, file_path=file_path)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def get_posts_by_user(db: Session, user_id: int):
    return db.query(Post).filter(Post.owner_id == user_id).all()


def delete_post(db: Session, post_id: int, user_id: int):
    db_post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user_id).first()

    if db_post:
        db.delete(db_post)
        db.commit()
        return db_post

    return None
