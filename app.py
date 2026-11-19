from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "shopnex-demo-secret-key"
DB_PATH = Path(__file__).with_name("shopnex.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL CHECK(price >= 0),
                category TEXT NOT NULL,
                image TEXT NOT NULL,
                stock INTEGER NOT NULL DEFAULT 10
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                total REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Placed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                FOREIGN KEY(order_id) REFERENCES orders(id)
            )
        """)
        products = [
            ('Wireless Headphones', 'Comfortable over-ear headphones with clear everyday sound.', 1499, 'Electronics', "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80", 15),
            ('Smart Watch', 'Smart watch with activity tracking and notification support.', 2299, 'Electronics', "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80", 12),
            ('Bluetooth Speaker', 'Portable speaker for music at home or outdoors.', 1199, 'Electronics', "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=900&q=80", 18),
            ('Wireless Mouse', 'Ergonomic wireless mouse for work and study.', 499, 'Electronics', "https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=900&q=80", 25),
            ('Mechanical Keyboard', 'Compact mechanical-style keyboard for everyday typing.', 1899, 'Electronics', "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=900&q=80", 10),
            ('HD Webcam', 'Full HD webcam for online classes and video calls.', 1399, 'Electronics', "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=900&q=80", 14),
            ('USB-C Hub', 'Multi-port USB-C hub for laptops and tablets.', 999, 'Electronics', "https://images.unsplash.com/photo-1625842268584-8f3296236761?auto=format&fit=crop&w=900&q=80", 20),
            ('Power Bank', 'Portable power bank for charging devices on the go.', 1299, 'Electronics', "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?auto=format&fit=crop&w=900&q=80", 16),
            ('Laptop Stand', 'Adjustable stand for a more comfortable desk setup.', 899, 'Electronics', "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=900&q=80", 13),
            ('Gaming Controller', 'Comfortable wireless-style controller for gaming.', 1599, 'Electronics', "https://images.unsplash.com/photo-1593305841991-05c297ba4575?auto=format&fit=crop&w=900&q=80", 8),
            ('Desk Microphone', 'USB desktop microphone for calls and recordings.', 1799, 'Electronics', "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=900&q=80", 9),
            ('Portable SSD Case', 'Protective storage case for portable drives.', 399, 'Electronics', "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=900&q=80", 22),
            ('LED Monitor Light', 'Space-saving LED light for your monitor setup.', 1099, 'Electronics', "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80", 11),
            ('Phone Tripod', 'Compact adjustable tripod for mobile photography.', 649, 'Electronics', "https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?auto=format&fit=crop&w=900&q=80", 17),
            ('Tablet Sleeve', 'Padded sleeve to protect your tablet while travelling.', 599, 'Electronics', "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=900&q=80", 19),
            ('Running Shoes', 'Breathable shoes designed for daily use and light exercise.', 1799, 'Fashion', "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80", 9),
            ('Travel Backpack', 'Lightweight backpack for college, work and travel.', 999, 'Fashion', "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80", 20),
            ('Classic Wrist Watch', 'Minimal wrist watch with a clean everyday design.', 1499, 'Fashion', "https://images.unsplash.com/photo-1524592094714-0f0654e20314?auto=format&fit=crop&w=900&q=80", 10),
            ('Cotton T-Shirt', 'Soft cotton crew-neck T-shirt for everyday wear.', 499, 'Fashion', "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=80", 30),
            ('Casual Sneakers', 'Versatile casual sneakers for daily outfits.', 1599, 'Fashion', "https://images.unsplash.com/photo-1495555961986-6d4c1ecb7be3?auto=format&fit=crop&w=900&q=80", 14),
            ('Denim Jacket', 'Classic denim jacket for casual styling.', 2199, 'Fashion', "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=900&q=80", 7),
            ('Sunglasses', 'Lightweight sunglasses with a timeless frame.', 799, 'Fashion', "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=900&q=80", 16),
            ('Leather Wallet', 'Slim wallet with practical card compartments.', 599, 'Fashion', "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=900&q=80", 21),
            ('Baseball Cap', 'Adjustable cap for casual everyday wear.', 349, 'Fashion', "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=900&q=80", 18),
            ('Everyday Hoodie', 'Comfortable hoodie for relaxed everyday styling.', 1199, 'Fashion', "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=900&q=80", 12),
            ('Canvas Tote Bag', 'Reusable tote bag for shopping and daily essentials.', 299, 'Fashion', "https://images.unsplash.com/photo-1586350977771-b3b0c4a2c4a8?auto=format&fit=crop&w=900&q=80", 25),
            ('Sports Socks Pack', 'Soft sports socks suitable for everyday use.', 249, 'Fashion', "https://images.unsplash.com/photo-1624222247344-550fb8e50e6f?auto=format&fit=crop&w=900&q=80", 40),
            ('Formal Belt', 'Simple adjustable belt for formal and casual outfits.', 499, 'Fashion', "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?auto=format&fit=crop&w=900&q=80", 15),
            ('Travel Duffel Bag', 'Roomy duffel bag for short trips and gym use.', 1299, 'Fashion', "https://images.unsplash.com/photo-1514228742587-6b1558f?auto=format&fit=crop&w=900&q=80", 8),
            ('Winter Scarf', 'Soft scarf for cool-weather outfits.', 399, 'Fashion', "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=900&q=80", 13),
            ('Desk Lamp', 'Adjustable LED lamp for your study desk.', 699, 'Home & Living', "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?auto=format&fit=crop&w=900&q=80", 18),
            ('Coffee Mug', 'Ceramic mug for your everyday coffee or tea.', 299, 'Home & Living', "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?auto=format&fit=crop&w=900&q=80", 30),
            ('Water Bottle', 'Reusable bottle for home, college and travel.', 399, 'Home & Living', "https://images.unsplash.com/photo-1490312278390-ab64016e0aa9?auto=format&fit=crop&w=900&q=80", 24),
            ('Cushion Cover Set', 'Decorative cushion covers for a simple room refresh.', 499, 'Home & Living', "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=900&q=80", 17),
            ('Wall Clock', 'Minimal wall clock for your living space.', 799, 'Home & Living', "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80", 10),
            ('Storage Basket', 'Multipurpose basket to organize everyday items.', 349, 'Home & Living', "https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=900&q=80", 20),
            ('Bedsheet Set', 'Comfortable bedsheet set for a restful bedroom.', 1299, 'Home & Living', "https://images.unsplash.com/photo-1495521821757-a1efb6729352?auto=format&fit=crop&w=900&q=80", 9),
            ('Table Organizer', 'Keep stationery and desk essentials neatly arranged.', 449, 'Home & Living', "https://images.unsplash.com/photo-1600369671236-e74521d4b6ad?auto=format&fit=crop&w=900&q=80", 14),
            ('Plant Pot', 'Simple decorative pot for indoor plants.', 249, 'Home & Living', "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=900&q=80", 22),
            ('LED String Lights', 'Warm decorative lights for your room.', 399, 'Home & Living', "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=900&q=80", 16),
            ('Non-stick Frying Pan', 'Everyday frying pan for quick home cooking.', 899, 'Home & Living', "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80", 8),
            ('Kitchen Storage Jars', 'Reusable jars to organize pantry essentials.', 599, 'Home & Living', "https://images.unsplash.com/photo-1503602642458-232111445657?auto=format&fit=crop&w=900&q=80", 12),
            ('Bath Towel Set', 'Soft absorbent towels for daily use.', 699, 'Home & Living', "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=80", 15),
            ('Laundry Hamper', 'Foldable hamper for laundry organization.', 549, 'Home & Living', "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=900&q=80", 11),
            ('Doormat', 'Durable mat for your home entrance.', 299, 'Home & Living', "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80", 19),
            ('Phone Case', 'Protective everyday phone case with a slim profile.', 299, 'Accessories', "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?auto=format&fit=crop&w=900&q=80", 30),
            ('Screen Protector', 'Clear screen protector for everyday device protection.', 199, 'Accessories', "https://images.unsplash.com/photo-1503602642458-232111445657?auto=format&fit=crop&w=900&q=80", 35),
            ('Laptop Sleeve', 'Padded sleeve to help protect your laptop.', 699, 'Accessories', "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=900&q=80", 14),
            ('Cable Organizer', 'Simple organizer to keep charging cables tidy.', 149, 'Accessories', "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80", 40),
            ('Keychain', 'Small everyday keychain with a clean design.', 99, 'Accessories', "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=900&q=80", 50),
            ('Reusable Shopping Bag', 'Foldable reusable bag for daily shopping.', 129, 'Accessories', "https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?auto=format&fit=crop&w=900&q=80", 28),
            ('Travel Adapter Pouch', 'Compact pouch for organizing travel adapters and cables.', 349, 'Accessories', "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=900&q=80", 16),
            ('Card Holder', 'Slim holder for essential cards.', 249, 'Accessories', "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=900&q=80", 21),
            ('Laptop Cleaning Kit', 'Basic cleaning kit for screens and keyboards.', 299, 'Accessories', "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80", 18),
            ('Phone Ring Holder', 'Compact grip accessory for compatible phones.', 179, 'Accessories', "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=900&q=80", 25),
            ('Wireless Charging Pad', 'Convenient charging pad for compatible devices.', 899, 'Accessories', "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80", 10),
            ('Camera Strap', 'Adjustable strap for carrying a camera comfortably.', 499, 'Accessories', "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=900&q=80", 12),
            ('Travel Neck Pillow', 'Soft neck pillow for more comfortable journeys.', 599, 'Accessories', "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80", 13),
            ('Compact Umbrella', 'Portable umbrella for unexpected rain.', 449, 'Accessories', "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80", 20),
            ('Notebook Set', 'Set of notebooks for notes, lists and planning.', 199, 'Accessories', "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=900&q=80", 32),
        ]
        existing_names = {row["name"] for row in db.execute("SELECT name FROM products").fetchall()}
        for product in products:
            if product[0] not in existing_names:
                db.execute(
                    "INSERT INTO products (name, description, price, category, image, stock) VALUES (?, ?, ?, ?, ?, ?)",
                    product
                )

def cart_details():
    cart = session.get("cart", {})
    if not cart:
        return [], 0
    ids = [int(pid) for pid in cart.keys()]
    placeholders = ",".join("?" for _ in ids)
    with get_db() as db:
        rows = db.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", ids).fetchall()
    items, total = [], 0
    for product in rows:
        quantity = int(cart.get(str(product["id"]), 0))
        subtotal = product["price"] * quantity
        items.append({"product": product, "quantity": quantity, "subtotal": subtotal})
        total += subtotal
    return items, total

@app.context_processor
def inject_cart_count():
    return {"cart_count": sum(int(q) for q in session.get("cart", {}).values())}

@app.route("/")
def home():
    search = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    sql = "SELECT * FROM products WHERE 1=1"
    params = []
    if search:
        sql += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    if category:
        sql += " AND category = ?"
        params.append(category)
    sql += " ORDER BY id DESC"
    with get_db() as db:
        products = db.execute(sql, params).fetchall()
        categories = [r["category"] for r in db.execute("SELECT DISTINCT category FROM products ORDER BY category")]
    return render_template("index.html", products=products, categories=categories, search=search, selected_category=category)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    with get_db() as db:
        product = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if product is None:
        flash("That product could not be found.", "error")
        return redirect(url_for("home"))
    return render_template("product.html", product=product)

@app.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    with get_db() as db:
        product = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if product is None:
        flash("Product not found.", "error")
    elif product["stock"] < 1:
        flash("This product is currently out of stock.", "error")
    else:
        cart = session.get("cart", {})
        key = str(product_id)
        current = int(cart.get(key, 0))
        if current < product["stock"]:
            cart[key] = current + 1
            session["cart"] = cart
            flash(f'{product["name"]} added to your cart.', "success")
        else:
            flash("You have reached the available stock quantity.", "error")
    return redirect(request.referrer or url_for("home"))

@app.route("/cart")
def cart():
    items, total = cart_details()
    return render_template("cart.html", items=items, total=total)

@app.post("/cart/update")
def update_cart():
    cart_data = session.get("cart", {})
    for key in list(cart_data.keys()):
        try:
            quantity = int(request.form.get(f"quantity_{key}", cart_data[key]))
        except ValueError:
            quantity = 1
        if quantity <= 0:
            cart_data.pop(key, None)
            continue
        with get_db() as db:
            product = db.execute("SELECT stock FROM products WHERE id = ?", (int(key),)).fetchone()
        if product:
            cart_data[key] = min(quantity, product["stock"])
    session["cart"] = cart_data
    flash("Cart updated.", "success")
    return redirect(url_for("cart"))

@app.post("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart_data = session.get("cart", {})
    cart_data.pop(str(product_id), None)
    session["cart"] = cart_data
    flash("Item removed from cart.", "success")
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = cart_details()
    if not items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("home"))
    if request.method == "POST":
        name = request.form.get("customer_name", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        if not name or not email or "@" not in email or not address:
            flash("Please enter a valid name, email and delivery address.", "error")
            return render_template("checkout.html", items=items, total=total)
        with get_db() as db:
            # Re-check stock at order time.
            for item in items:
                current = db.execute("SELECT stock FROM products WHERE id = ?", (item["product"]["id"],)).fetchone()
                if current is None or current["stock"] < item["quantity"]:
                    flash(f'Not enough stock for {item["product"]["name"]}. Please update your cart.', "error")
                    return redirect(url_for("cart"))
            cursor = db.execute(
                "INSERT INTO orders (customer_name, email, address, total) VALUES (?, ?, ?, ?)",
                (name, email, address, total)
            )
            order_id = cursor.lastrowid
            for item in items:
                product = item["product"]
                db.execute(
                    "INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price) VALUES (?, ?, ?, ?, ?)",
                    (order_id, product["id"], product["name"], item["quantity"], product["price"])
                )
                db.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (item["quantity"], product["id"]))
        session["cart"] = {}
        return redirect(url_for("order_success", order_id=order_id))
    return render_template("checkout.html", items=items, total=total)

@app.route("/order-success/<int:order_id>")
def order_success(order_id):
    with get_db() as db:
        order = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        order_items = db.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,)).fetchall()
    if order is None:
        return redirect(url_for("home"))
    return render_template("success.html", order=order, order_items=order_items)

@app.route("/orders")
def orders():
    email = request.args.get("email", "").strip()
    results = []
    if email:
        with get_db() as db:
            results = db.execute("SELECT * FROM orders WHERE email = ? ORDER BY created_at DESC", (email,)).fetchall()
    return render_template("orders.html", orders=results, email=email)

# Simple JSON API endpoints for Postman and capstone testing.
@app.get("/api/products")
def api_products():
    with get_db() as db:
        products = db.execute("SELECT id, name, description, price, category, stock FROM products ORDER BY id").fetchall()
    return jsonify([dict(row) for row in products])

@app.get("/api/products/<int:product_id>")
def api_product_detail(product_id):
    with get_db() as db:
        product = db.execute("SELECT id, name, description, price, category, stock FROM products WHERE id = ?", (product_id,)).fetchone()
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(dict(product))

@app.get("/health")
def health():
    return jsonify({"status": "ok", "application": "SHOPNEX"})

init_db()

if __name__ == "__main__":
    app.run(debug=True)