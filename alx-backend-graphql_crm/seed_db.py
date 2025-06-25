# crm/seed_db.py

from crm.models import Customer, Product

def seed():
    Customer.objects.create(name="Test User", email="test@user.com", phone="+1234567890")
    Product.objects.bulk_create([
        Product(name="Laptop", price=999.99, stock=5),
        Product(name="Mouse", price=25.00, stock=30),
    ])
