import csv
import json

from app import db, app
from app.models import Item

def add_custom_items():
    with app.app_context():
        items = [
            Item(
                url="https://example.com/item",
                name="ASTRO LOOSE BAGGY LEG JEANS",
                size="S, M, L",
                category="Bottoms",
                price=30,
                color="Black",
                sku="TSHIRT001",
                images=json.dumps(["https://media.weekday.com/static/products/65/93/6593b955567dee13ac6250b67d92756351134910_lg-1.jpg?imwidth=1024"]),
                stock=10
            ),
             Item(
                url="https://example.com/item1",
                name="SWEATSHIRT",
                size="S, M, L",
                category="Outerwear",
                price=24,
                color="Black",
                sku="TSHIRT001",
                images=json.dumps(["https://media.weekday.com/static/products/cb/58/cb58054bd710ecbb0457d63527bcca1c4105848c_lg-1.jpg?imwidth=1024"]),
                stock=10
            ),
            Item(
                url="https://example.com/item2",
                name="SHRUNKEN FAUX LEATHER JACKET",
                size="28, 30, 32",
                category="Bottoms",
                price=49,
                color="Blue",
                sku="JEANS001",
                images=json.dumps(["https://media.weekday.com/static/products/b0/ff/b0ffe027a33998a09bbbae06880b7c54091f984b_lg-1.jpg?imwidth=1024"]),
                stock=3
            ),
            Item(
                url="https://example.com/item3",
                name="OVERSIZED GRAPHIC COTTON SHIRT",
                size="S, M, L",
                category="Tops",
                price=29,
                color="White",
                sku="SHIRT001",
                images=json.dumps(["https://media.weekday.com/static/products/a8/a9/a8a9a9d05818f8015771d1d2e96026c5f385613e_xl-1.jpg?imwidth=1600"]),
                stock=15
            ),
            Item(
                url="https://example.com/item4",
                name="REGULAR JACQUARD KNITTED GRAPHIC SWEATER",
                size="XS, S, M",
                category="Dresses",
                price=60,
                color="Red",
                sku="DRESS001",
                images=json.dumps(["https://media.weekday.com/static/products/e0/fb/e0fbb3670d4515a772be5bb9cf1093d246ebac4d_lg-1.jpg?imwidth=1024"]),
                stock=8
            ), 
            Item(
                url="https://example.com/item5",
                name="SCUBA ZIP HOODIE",
                size="S, M, L",
                category="Outerwear",
                price=44,
                color="Blue",
                sku="JEANS03502",
                images=json.dumps(["https://media.weekday.com/static/products/9f/e5/9fe50f7560241b9c6f3342821e28372abf14b1c7_lg-1.jpg?imwidth=1024"]),
                stock=12
            ),
            Item(
                url="https://example.com/item6",
                name="SINGLE BREASTED WOOL-BLEND COAT",
                size="S, M, L",
                category="Jackets",
                price=109,
                color="Black",
                sku="JACKET0301",
                images=json.dumps(["https://media.weekday.com/static/products/89/91/899138ee50083ce2ffccabb8418d7305b3824aa4_lg-1.jpg?imwidth=1024"]),
                stock=7
            ),
            Item(
                url="https://example.com/item7",
                name="COMO BLUE ASTRO BAGGY JEANS",
                size="S, M, L, XL",
                category="Jeans",
                price=40,
                color="White",
                sku="SHIssaJEANsRT002",
                images=json.dumps(["https://media.weekday.com/static/products/52/3c/523cfa173b862862a4bec8e9ca526e0c25f1cf8b_lg-1.jpg?imwidth=1024"]),
                stock=20
            ),
            Item(
                url="https://example.com/item8",
                name="LARGE MERCH TOTE BAG",
                size="one size",
                category="Bag",
                price=14,
                color="Blue",
                sku="JEANS003",
                images=json.dumps(["https://media.weekday.com/static/products/45/eb/45eb1d6c5c73ed09f705b75fcd4c37387a72ad75_lg-1.jpg?imwidth=1024"]),
                stock=2
            )
            # Add more items as needed --
        ]
        db.session.add_all(items)
        db.session.commit()
        print("Custom items added successfully.")

if __name__ == '__main__':
    add_custom_items()
