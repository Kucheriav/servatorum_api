from sqlalchemy import Column, Integer, String, Table, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


# Таблицы связок many-to-many

user_spheres = Table(
    "user_spheres", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("sphere_id", Integer, ForeignKey("spheres.id"), primary_key=True),
)

company_spheres = Table(
    "company_spheres", Base.metadata,
    Column("company_id", Integer, ForeignKey("companies.id"), primary_key=True),
    Column("sphere_id", Integer, ForeignKey("spheres.id"), primary_key=True),
)

foundation_spheres = Table(
    "foundation_spheres", Base.metadata,
    Column("foundation_id", Integer, ForeignKey("foundations.id"), primary_key=True),
    Column("sphere_id", Integer, ForeignKey("spheres.id"), primary_key=True),
)

class Sphere(Base):
    __tablename__ = "spheres"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    users = relationship("User", secondary=user_spheres, back_populates="spheres")
    companies = relationship("Company", secondary=company_spheres, back_populates="spheres")
    foundations = relationship("Foundation", secondary=foundation_spheres, back_populates="spheres")
