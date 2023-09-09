from typing import Optional, List

from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import select

from db.models import CategoryORM
from schemas.category import Category


def get_all_categories(db: Session) -> List[Category]:
    categories = db.query(CategoryORM).where(CategoryORM.id != 1).all()
    cat = []

    for categorie in categories:
        cat.append(Category(**categorie.to_dict()))

    return cat


def get_category_hierarchy_from_db(name: str, db: Session):
    top_query = (
        db.query(CategoryORM)
        .filter(CategoryORM.name == name)
        .cte("cte", recursive=True)
    )

    # Query para el nivel inferior (recursive part)
    bottom_query = db.query(CategoryORM).join(
        top_query, CategoryORM.parent_id == top_query.c.id
    )

    # Unión de ambas consultas
    recursive_query = top_query.union(bottom_query)  # type: ignore

    # Consulta final
    result = db.query(recursive_query).all()

    return result
