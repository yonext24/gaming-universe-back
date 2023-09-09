from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    Text,
    Float,
    CheckConstraint,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from db.dbconfig import engine


Base = declarative_base()


class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    username = Column(String(60), nullable=False)
    password = Column(String(30), nullable=False)
    email = Column(String(30), nullable=True, unique=True)
    active = Column(Boolean, default=False)

    def to_dict(self):
        required_attrs = [
            "id",
            "first_name",
            "last_name",
            "username",
            "password",
            "email",
            "active",
        ]
        return {attr: getattr(self, attr) for attr in required_attrs}


class SessionORM(Base):
    __tablename__ = "sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    expiration_at = Column(TIMESTAMP)

    user = relationship("UserORM", backref="sessions")

    def to_dict(self):
        required_attrs = ["session_id", "user_id", "created_at", "expiration_at"]
        return {attr: getattr(self, attr) for attr in required_attrs}


class CategoryORM(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"))

    def to_dict(self):
        required_attrs = ["id", "name", "parent_id"]
        return {attr: getattr(self, attr) for attr in required_attrs}


class ProductORM(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String(255), nullable=False)
    rating = Column(
        Float, CheckConstraint("rating >= 0 AND rating <= 5"), default=0, nullable=False
    )
    featuredRating = Column(Boolean, default=False, nullable=False)
    slug = Column(String(120), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("CategoryORM", backref="products")

    def to_dict(self):
        required_attrs = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "rating",
            "featuredRating",
            "slug",
            "category_id",
        ]
        return {attr: getattr(self, attr) for attr in required_attrs}


Base.metadata.create_all(bind=engine)
