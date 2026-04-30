from typing import Optional
import sqlalchemy as sa  # includes general purpose database functions and classes such as types and query building helpers
import sqlalchemy.orm as so  # provides the support for using models
from app import db
from datetime import datetime, timezone


# defines the initial database structure (or schema)
class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # for high-level view of the relationship between users and posts
    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")

    def __repr__(self):  # it tells Python how to print objects of this class
        return f"<User {self.username!r}>"


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    # for high-level view of the relationship between users and posts
    author: so.Mapped[User] = so.relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post {self.body!r}>"
