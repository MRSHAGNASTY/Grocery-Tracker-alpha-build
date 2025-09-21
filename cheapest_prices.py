from backend.database import SessionLocal
from backend.models import Product, PriceEntry

def get_cheapest_prices():
    session = SessionLocal()
    products = session.query(Product).all()

    for product in products:
        # Get the PriceEntry with the lowest price for this product
        cheapest = session.query(PriceEntry)\
                          .filter(PriceEntry.product_id == product.id)\
                          .order_by(PriceEntry.price.asc())\
                          .first()
        if cheapest:
            print(f"{product.name}: Cheapest at {cheapest.store.name} - R{cheapest.price:.2f}")
        else:
            print(f"{product.name}: No prices available")
    
    session.close()

if __name__ == "__main__":
    get_cheapest_prices()
