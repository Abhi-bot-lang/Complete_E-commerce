from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.product_schema import ProductSchema
from app.config.database import get_db
from app.models.product_model import Product



router = APIRouter()





# Get All Products
@router.get("/")
def get_all_products(db: Session = Depends(get_db)):
   #SELECT * FROM PRODUCTS
    return db.query(Product).all()

# Get Single Product by ID
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first() #SELECT * FROM PRODUCTS WHERE ID=?
    if not product:
        raise HTTPException(detail="Product not found")
    return product

# Create Product
@router.post("/")
def create_product(product_in: ProductSchema, db: Session = Depends(get_db)):
    
    db_product = Product(
        Name=product_in.Name,
        Description=product_in.Description,
        Price=product_in.Price,
        Quantity=product_in.Quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Update Product
@router.put("/{product_id}")
def update_product(product_id: int, product_in: ProductSchema, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    #UPDATE PRODUCTS SET=1 WHERE ID="1";
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
        
        
    db_product.Name = product_in.Name
    db_product.Description = product_in.Description
    db_product.Price = product_in.Price
    db_product.Quantity = product_in.Quantity
    
    db.commit()
    db.refresh(db_product)
    return db_product

# Delete Product
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    db.delete(db_product)
    db.commit()
    return None
    