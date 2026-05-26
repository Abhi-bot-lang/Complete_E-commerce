from fastapi import HTTPException, status
from app.models.categories import Category


def get_all_categories(db):
    try:
        categories = db.query(Category).all()

        if not categories:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No categories found"
            )

        return categories

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )

def get_category_by_id(category_id: int, db):

    try:

        category = db.query(Category).filter(
            Category.id == category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        return category

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )

def create_category(category_data, db):

    try:

        existing_category = db.query(Category).filter(
            Category.name == category_data.name
        ).first()

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )

#check this tomorow
def update_category(category_id: int,category_data,db):
    try:

        category = db.query(Category).filter(
            Category.id == category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        #Duplicate name
        existing_category = db.query(Category).filter(
            Category.name == category_data.name,
            Category.id != category_id
        ).first()
        #Duplicate name
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )

def delete_category(category_id: int, db):
    try:

        category = db.query(Category).filter(
            Category.id == category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )
