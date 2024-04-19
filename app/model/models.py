from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

class Mindmap(Base):
    __tablename__ = "mindmaps"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User")