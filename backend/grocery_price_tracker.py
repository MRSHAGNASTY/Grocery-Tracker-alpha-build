# grocery_price_tracker.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime, timedelta

# Simulated in-memory database
stores = ["ShopRite", "PicknPay", "Checkers"]
products_db = {
    "Milk 1L": {"ShopRite": 18.5, "PicknPay": 19.0, "Checkers": 17.8},
    "Bread": {"ShopRite": 12.0, "PicknPay": 12.5, "Checkers": 11.8},
    "Eggs 12pcs": {"ShopRite": 28.0, "PicknPay": 27.5, "Checkers": 28.2}
}

app = FastAPI()

class BasketItem(BaseModel):
    product_name: str
    quantity: float

@app.get("/products")
def list_products():
    return {"products": list(products_db.keys())}

@app.get("/compare/{product_name}")
def compare_product(product_name: str):
    if product_name not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    prices = products_db[product_name]
    sorted_prices = dict(sorted(prices.items(), key=lambda x: x[1]))
    return {"product": product_name, "prices": sorted_prices}

@app.post("/basket/estimate")
def basket_estimate(items: List[BasketItem]):
    total_per_store: Dict[str, float] = {store: 0.0 for store in stores}

    for item in items:
        if item.product_name not in products_db:
            continue
        for store in stores:
            price = products_db[item.product_name].get(store, 0)
            total_per_store[store] += price * item.quantity

    best_store = min(total_per_store.items(), key=lambda x: x[1])
    return {
        "total_per_store": total_per_store,
        "best_store": {"store": best_store[0], "total": best_store[1]}
    }

# Run using: uvicorn grocery_price_tracker:app --reload
