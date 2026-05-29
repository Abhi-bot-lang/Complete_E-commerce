from fastapi import HTTPException, status

from app.models.categories import Category
from app.schemas.categories import CategoryUpdateSchema,CategoryCreate


def get_all_categories(db):
    try:
        categories = db.query(Category).all()

        if not categories:
            raise HTTPException(
                status_code=404,
                detail="No categories found"
            )

        return categories

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )

def get_category_by_id(category_id: int, db):

    try:

        category = db.query(Category).filter(
            Category.id == category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        return category

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )

def create_category(category_data:CategoryCreate, db):

    try:

        existing_category = db.query(Category).filter(
            Category.name == category_data.name
        ).first()

        if existing_category:
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )

        category = Category(
            name=category_data.name
        )

        db.add(category)
        db.commit()
        db.refresh(category)

        return {
            "message": "Category created successfully",
            "data": category
           
        }

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
    

        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )

def update_category(category_id: int,category_data:CategoryUpdateSchema,db):
    try:

        category = db.query(Category).filter(
            Category.id == category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )
        #Duplicate name
        existing_category = db.query(Category).filter(
            Category.name == category_data.name

        ).first()
        if existing_category:
            raise HTTPException(
                status_code=404,
                detail="Category already exists"
            )

        category.name = category_data.name

        db.commit()
        db.refresh(category)

        return {
            "message": "Category updated successfully",
            "data": category
        }

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
       raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )

def delete_category(category_id: int, db):
    try:

        category = db.query(Category).filter(
            Category.id == category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        db.delete(category)
        db.commit()

        return {
            "message": "Category deleted successfully"
        }

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
      raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )
