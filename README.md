# SHOPNEX — Lightweight Full-Stack E-Commerce Demo

A small Flask + SQLite shopping website created as the first test website for the capstone project.

## Features
- Product catalogue with search and category filtering
- Product detail pages
- Session-based shopping cart (add, update, remove)
- Checkout form with server-side validation
- Orders saved in SQLite, including order items
- Order lookup by checkout email
- JSON API endpoints for source-code/API testing
- Stock validation and stock reduction after checkout

## Requirements
- Python 3.10+
- pip

## Run on Windows
1. Extract the project ZIP.
2. Open the `SHOPNEX` folder in VS Code.
3. Open Terminal in that folder.
4. Create and activate a virtual environment:

   ```powershell
   py -m venv venv
   .\venv\Scripts\activate
   ```

5. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

6. Start the website:

   ```powershell
   python app.py
   ```

7. Open http://127.0.0.1:5000

The SQLite database `shopnex.db` is created automatically on first run and 60 sample products across Electronics, Fashion, Home & Living, and Accessories are inserted. If you already ran an older version, restart the app; missing catalogue products will be added automatically without deleting existing orders.

## Useful routes
- `/` — product catalogue
- `/cart` — shopping cart
- `/checkout` — checkout
- `/orders` — find orders by email
- `/health` — application health endpoint
- `/api/products` — list products as JSON
- `/api/products/1` — product detail as JSON

## Notes for capstone testing
This is the clean baseline version. Keep an untouched copy before introducing deliberate bugs. The project contains real server-side routes, SQL queries, validation, stock checks and order persistence, so it can be used for both static source-code analysis and runtime testing.

This is a student demonstration project, not a production payment system. It does not collect real payments or implement production-grade user authentication, CSRF protection, or deployment secrets.


## Admin dashboard
- Open `/admin` and sign in.
- Demo username: `admin`
- Demo password: `ShopNex@2026!`
- Dashboard: `/admin/dashboard`
- Before public/production use, set `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and `SECRET_KEY` as environment variables in Render. Use strong unique values; do not keep the demo credentials.
- This is a capstone demo admin area. Add CSRF protection, rate limiting, HTTPS enforcement, and persistent database storage before production use.
