# Antigravity E-Commerce Store

A full-featured, responsive, modern E-Commerce web application built with **HTML5, CSS3, JavaScript**, and **Django (Python)**.

---

## 🌟 Features Implemented

1. **Product Catalog & Listings**:
   - Filter by categories (Electronics, Fashion, Home & Living, Sports & Fitness).
   - Search bar with instant keyword matching across titles and descriptions.
   - Sorting options: Newest arrivals, Price low-to-high, Price high-to-low, Product name.
   - Badges for stock status and featured items.

2. **Product Details Page**:
   - Detailed specs, images, price display, and stock indicators.
   - Quantity selector & instant Add-to-Cart.
   - Verified customer reviews & star ratings list.
   - Interactive review submission form for authenticated users.
   - Related products recommendation grid.

3. **Shopping Cart**:
   - Guest session cart & authenticated user cart integration.
   - Automatic cart merging when a guest user logs in.
   - Quantity increment (+), decrement (-), and item removal.
   - Real-time subtotal, tax calculation (2%), shipping threshold calculation (Free shipping over $200), and grand total calculation.

4. **Order Processing & Checkout**:
   - Shipping address and contact information form with validation.
   - Multiple payment options (Credit/Debit Card, PayPal, Cash on Delivery).
   - Order placement logic generating unique Order Numbers (`ORD-YYYYMMDD-XXXXXX`) and Transaction IDs.
   - Stock auto-reduction upon completed purchase.
   - Printable order completion receipt and order tracking.

5. **User Registration & Login**:
   - Full user authentication flow (Register, Login via username/email, Logout).
   - User Dashboard displaying user profile details and full order history.
   - Detailed breakdown view for past orders.

6. **Database & Admin Management**:
   - SQLite Database storing Products, Categories, Users, Carts, Orders, Order Items, and Product Reviews.
   - Customized Django Admin panel (`/admin/`) to manage products, categories, stock, and order statuses ("Pending", "Processing", "Shipped", "Completed").

---

## 🚀 How to Run the Application

1. **Activate Virtual Environment & Start Server**:
   ```bash
   # In PowerShell / Command Prompt:
   .\venv\Scripts\python.exe manage.py runserver
   ```

2. **Access the Store in Browser**:
   - **Store URL**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - **Admin Dashboard**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔑 Pre-Configured Accounts

- **Admin Account**:
  - **Username**: `admin`
  - **Password**: `admin123`
- **Test User Account**:
  - **Username**: `johndoe`
  - **Password**: `password123`

---

## 🧪 Running Integration Tests

To verify all views, database models, and cart/checkout flows:
```bash
.\venv\Scripts\python.exe test_store.py
```
