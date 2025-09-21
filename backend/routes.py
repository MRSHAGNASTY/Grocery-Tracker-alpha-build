from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from PIL import Image
import pytesseract, io, re
from .database import SessionLocal, Base, engine
from .models import Product, Store, PriceEntry
from datetime import datetime

router = APIRouter()

Base.metadata.create_all(engine)

def normalize_unit(name):
    match = re.search(r'(\d+\.?\d*)\s*(kg|g|l|ml|each)?', name.lower())
    qty = 1.0
    unit = 'each'
    if match:
        qty = float(match.group(1))
        unit = match.group(2) if match.group(2) else 'each'
        if unit == 'g': qty /= 1000
        if unit == 'ml': qty /= 1000
    return qty, unit

@router.get("/products")
def list_products():
    session = SessionLocal()
    products = session.query(Product).all()
    session.close()
    return [{"id": p.id, "name": p.name, "unit": p.unit} for p in products]

@router.post("/add_product")
def add_product(name: str, unit: str = "each"):
    session = SessionLocal()
    product = Product(name=name, unit=unit)
    session.add(product)
    session.commit()
    session.close()
    return {"status": "ok"}

@router.post("/add_store")
def add_store(name: str, location: str = None):
    session = SessionLocal()
    store = Store(name=name, location=location)
    session.add(store)
    session.commit()
    session.close()
    return {"status": "ok"}

@router.post("/add_price")
def add_price(product_id: int, store_id: int, price: float):
    session = SessionLocal()
    pe = PriceEntry(product_id=product_id, store_id=store_id, price=price)
    session.add(pe)
    session.commit()
    session.close()
    return {"status": "ok"}

from sqlalchemy import func

@router.get("/compare/")
@router.get("/compare/{product_name}")
def compare_product(product_name: str = None):
    session = SessionLocal()
    comparisons = []

    query = session.query(Product)
    if product_name:
        query = query.filter(Product.name.ilike(f"%{product_name}%"))

    products = query.all()
    if not products:
        session.close()
        raise HTTPException(status_code=404, detail="Product not found")

    for prod in products:
        latest_price = session.query(PriceEntry).filter(PriceEntry.product_id == prod.id).order_by(PriceEntry.price.asc()).first()
        if latest_price:
            comparisons.append({
                "product": prod.name,
                "cheapest_store": latest_price.store.name,
                "price": latest_price.price
            })

    session.close()
    return {"comparisons": comparisons}

@router.post("/upload_receipt")
async def upload_receipt(file: UploadFile = File(...), store_name: str = Form(...)):
    if not store_name:
        return {"status": "error", "message": "Store name is required."}

    # Read image from uploaded file
    image = Image.open(io.BytesIO(file.file.read()))

    # Run OCR
    text = pytesseract.image_to_string(image)

    # Further processing...
    return {"status": "ok", "message": "Receipt processed.", "text": text}


    # Fetch or create store
    store = session.query(Store).filter(Store.name.ilike(f"%{store_name}%")).first()
    if not store:
        store = Store(name=store_name)
        session.add(store)
        session.commit()

    # Process receipt text
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) >= 2:
            try:
                price = float(parts[-1].replace('R','').replace(',',''))
                name = ' '.join(parts[:-1])
                qty, unit = normalize_unit(name)
                product = session.query(Product).filter(Product.name.ilike(f"%{name}%")).first()
                if not product:
                    product = Product(name=name.strip(), unit=unit)
                    session.add(product)
                    session.commit()
                pe = PriceEntry(product_id=product.id, store_id=store.id, price=price, quantity=qty)
                session.add(pe)
            except ValueError:
                continue

    session.commit()
    session.close()
    return {"status": "ok", "message": "Receipt processed", "text": text}
