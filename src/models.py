from __future__ import annotations
from datetime import datetime
from typing import List
from sqlalchemy import (String, Integer, Boolean, ForeignKey, Table, Column, DateTime, func)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship



class Base(DeclarativeBase):
    pass


likes = Table(
    "likes",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("post_id", ForeignKey("post.id"), primary_key=True),
    Column("created_at", DateTime, server_default=func.now())
)

followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", ForeignKey("user.id"), primary_key=True),
    Column("following_id", ForeignKey("user.id"), primary_key=True),
    Column("created_at", DateTime, server_default=func.now())
)

saved_posts = Table(
    "saved_posts",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("post_id", ForeignKey("post.id"), primary_key=True),
    Column("created_at", DateTime, server_default=func.now())
)



class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(80))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    bio: Mapped[str | None] = mapped_column(String(250))
    profile_pic: Mapped[str | None] = mapped_column(String(255))

    
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author"
    )

    comments: Mapped[List["Comment"]] = relationship(
        back_populates="author"
    )

    
    liked_posts: Mapped[List["Post"]] = relationship(
        secondary=likes,
        back_populates="liked_by"
    )

   
    saved: Mapped[List["Post"]] = relationship(
        secondary=saved_posts,
        back_populates="saved_by"
    )

    
    following: Mapped[List["User"]] = relationship(
        secondary=followers,
        primaryjoin=id == followers.c.follower_id,
        secondaryjoin=id == followers.c.following_id,
        back_populates="followers"
    )

    followers: Mapped[List["User"]] = relationship(
        secondary=followers,
        primaryjoin=id == followers.c.following_id,
        secondaryjoin=id == followers.c.follower_id,
        back_populates="following"
    )



class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )

    image_url: Mapped[str] = mapped_column(String(255))
    caption: Mapped[str | None] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

    
    author: Mapped["User"] = relationship(
        back_populates="posts"
    )

    comments: Mapped[List["Comment"]] = relationship(
        back_populates="post"
    )

    
    liked_by: Mapped[List["User"]] = relationship(
        secondary=likes,
        back_populates="liked_posts"
    )

    saved_by: Mapped[List["User"]] = relationship(
        secondary=saved_posts,
        back_populates="saved"
    )



class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )

    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id")
    )

    content: Mapped[str] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

    author: Mapped["User"] = relationship(
        back_populates="comments"
    )

    post: Mapped["Post"] = relationship(
        back_populates="comments"
    )