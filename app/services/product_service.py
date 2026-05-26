from Complete_E-commerce.app.schemas.product_schema 
from app.models.product_model import Product
from fastapi import HTTPException, status
from app.config.database import get_db
from app.models.categories import Category
from app.models.store_model import Store
from app.schemas.product_schema import ProductCreate
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.product_schema import ProductUpdate



def create_product(
    product: ProductCreate,
    user_id: int,
    db: Session
):

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

    # Check Store Ownership
    if store.userId != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this store"
        )

    # Create Product Object
    db_product = Product(
        productName=product.productName,
        price=product.price,
        stock=product.stock,
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
def get_all_products(db: Session):

    products = db.query(Product).all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found"
        )

    return products

def get_product_by_id(product_id: str, db: Session):

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

    # Product Found?
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product Not Found"
        )

    return product


def delete_product(
    product_id: str,
    user_id: str,
    db: Session
):

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
            detail="You cannot delete this product"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product Deleted Successfully"
    }

def update_product(
    product_id: str,
    data: ProductUpdate,
    user_id: str,
    db: Session
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )

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

    return product

def delete_product(
    product_id: str,
    user_id: str,
    db: Session
):

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