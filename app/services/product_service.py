from app.schemas.product_schema import ProductCreate,ProductUpdate 
from app.models.product_model import Product
from fastapi import HTTPException, status
from app.config.database import get_db
from app.models.categories import Category
from app.models.store_model import Store
from app.schemas.product_schema import ProductCreate
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.product_schema import ProductUpdate
from app.utils.Slug import generate_slug



def create_product(
    product: ProductCreate,
    user_id: int,
    db: Session
):
    try:

        # Check Category Exists
        category = db.query(Category).filter(
            Category.id == product.categoryId
        ).first()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        # Check Store Exists
        store = db.query(Store).filter(
            Store.id == product.storeId
        ).first()

        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Store not found"
            )

 
        # Create Product
        db_product = Product(
            productName=product.productName,
            price=product.price,
            stock=product.stock,
            slug=generate_slug(product.productName),
            categoryId=product.categoryId,
            storeId=product.storeId,
            userId=user_id
        )

        db.add(db_product)

        db.commit()

        db.refresh(db_product)

        return {
            "message": "Product created successfully",
            "product": db_product
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def get_all_products(db: Session):

    try:

        products = db.query(Product).all()

        if not products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No products found"
            )

        return products

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def get_product_by_id(product_id: str, db: Session):

    try:

        # Validate UUID
        UUID(product_id)

        # Find Product
        product = db.query(Product).filter(
            Product.id == product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product Not Found"
            )

        return product

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Product ID"
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

def update_product(
    product_id: str,
    data: ProductUpdate,
    user_id: str,
    db: Session
):

    try:

        # Find Product
        product = db.query(Product).filter(
            Product.id == product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product Not Found"
            )

     

        # Update Fields
        if data.productName is not None:
            product.productName = data.productName

        if data.price is not None:
            product.price = data.price

        if data.stock is not None:
            product.stock = data.stock

        if data.categoryId is not None:
            product.categoryId = data.categoryId

        if data.storeId is not None:
            product.storeId = data.storeId

        db.commit()

        db.refresh(product)

        return {
            "message": "Product Updated Successfully",
            "product": product
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def delete_product(
    product_id: str,
    user_id: str,
    db: Session
):

    try:

        # Validate UUID
        try:
            UUID(product_id)

        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Product ID"
            )

        # Find Product
        product = db.query(Product).filter(
            Product.id == product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product Not Found"
            )

        # Ownership Check
        if product.userId != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this product"
            )

        # Delete Product
        db.delete(product)

        db.commit()

        return {
            "message": "Product Deleted Successfully"
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

def search_products(search: str, db: Session):
    try:
        search_slug = generate_slug(search)
        products = db.query(Product).filter(
            Product.slug.ilike(f"%{search_slug}%")
        ).all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

