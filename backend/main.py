from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
import requests

def upload_receipt_cli():
    file_path = input("Enter receipt image path: ")
    store_name = input("Enter store name: ")

    url = "http://127.0.0.1:8000/upload_receipt"
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {"store_name": store_name}
            response = requests.post(url, files=files, data=data)
        result = response.json()
        print(result["message"])
        print("OCR Text:", result["text"])
    except Exception as e:
        print("Error uploading receipt:", e)

# CLI menu
while True:
    print("\nGrocery Price Tracker CLI")
    print("1. Search product")
    print("2. Add product to basket")
    print("3. Upload receipt")
    print("4. Exit")
    choice = input("Choose option: ")

    if choice == "1":
        # your search code here
        pass
    elif choice == "2":
        # your basket code here
        pass
    elif choice == "3":
        upload_receipt_cli()
    elif choice == "4":
        break

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

