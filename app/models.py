from typing import Optional
import sqlalchemy as sa  # includes general purpose database functions and classes such as types and query building helpers
import sqlalchemy.orm as so  # provides the support for using models
from app import db
from datetime import datetime, timezone
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)  # for password hash functionality
from flask_login import UserMixin
from app import login
from hashlib import md5  # for Avatar with Gravatar


# defines the initial database structure (or schema)
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # for high-level view of the relationship between users and posts
    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")

    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):  # it tells Python how to print objects of this class
        return f"<User {self.username!r}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


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


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
