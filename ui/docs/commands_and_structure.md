# 📘 Project: Inventory App
## Commands, Structure & Notes

This document tracks all important commands, files, and decisions made during development, to help you review or extend the project in the future.

---

## 📂 Project Structure Overview

### Initial Folder Structure

inventory_app/
│
├── db/                 # SQLite database file & related migrations/scripts
│   └── database.db
│
├── models/             # Database interaction logic
│   └── db_manager.py
│
├── ui/                 # PyQt5 UI windows
│   ├── login_window.py
│   ├── dashboard_window.py
│   ├── view_products_window.py
│   ├── add_product_window.py
│   ├── view_logs_window.py
│   └── manage_users_window.py
│
├── docs/               # Documentation
│   └── commands_and_structure.md
│
└── main.py             # Optional entry-point (if you use one)

## 🗄️ Database Setup & Commands

We use SQLite as our database.  
The database file is stored at:  
`db/database.db`

To initialize the database (create tables & insert dummy data), run:

```bash
python models/db_manager.py
```

What it does:
- Creates tables: `users`, `categories`, `products`, `inventory_logs`, `logs`
- Inserts default admin & user
- Inserts two categories: Electronics, Groceries
- Inserts two products: Laptop, Apples

You can safely delete/reset the database by renaming or deleting the file:
```bash
cd db/
mv database.db database.db.old
```
Then run the `db_manager.py` again to recreate it.

## 🖥️ UI Windows & Workflow

We use PyQt5 to build the GUI.  
Here are the main windows we’ve built and what they do.

### 🔐 Login Window
File: `ui/login_window.py`  
Run it to start the app:
```bash
python ui/login_window.py
```
- Lets user log in using `users` table.
- Opens Dashboard if login successful.

---

### 🏠 Dashboard Window
File: `ui/dashboard_window.py`
- Shown after successful login.
- Shows buttons:
  - 📦 View Products
  - ➕ Add Product
  - 📊 View Inventory Logs
  - 👥 Manage Users (visible only for admin)
  - 🚪 Logout

---

### 📦 View Products Window
File: `ui/view_products_window.py`
- Displays products table.
- Features:
  - Search products by name/SKU.
  - Filter by category.
  - Highlight low stock.
  - Export products to CSV.
  - Edit & Delete products.
  - Reset filters.

---

### ➕ Add Product Window
File: `ui/add_product_window.py`
- Add a new product to inventory.

---

### 📊 View Logs Window
File: `ui/view_logs_window.py`
- Shows logs of all actions.
- Tracks who did what & when.

---

### 👥 Manage Users Window
File: `ui/manage_users_window.py`
- Full CRUD for users.
- Only available for admin.
- Lets you add/edit/delete users & assign roles.

## 📝 Logging & Notes

We record all important actions into the `logs` table.  

### 📋 What gets logged?
Whenever a user edits, deletes, or adds a product (or user), a log is inserted with:
- `timestamp`
- `username`
- `action` (e.g., Deleted, Edited, Added)
- `product_name` or `user_name`

---

### 🔎 How to view logs?
Open the **View Logs** window from Dashboard → 📊 View Inventory Logs.  
It displays the logs in a table.

---

### 🚨 Why is logging important?
- Helps audit who made what changes.
- Helps debug mistakes.
- Makes the app more professional and secure.

## 🖥️ Helpful Commands

These are the key commands you used during development & testing.

---

### 📄 Run the app
Run the login screen (entry point):
```bash
python ui/login_window.py
```

---

### 🛠️ Create tables & insert dummy data
If you reset or delete the database, recreate it with:
```bash
python models/db_manager.py
```

---

### 🗑️ Reset the database
To reset the database (start fresh):
```bash
cd db/
mv database.db database.db.old
cd ..
python models/db_manager.py
```

This renames the old database, creates a fresh one, and populates it with default admin/user, products, and categories.

---

### 🌳 Git commands
Stage, commit, and push changes:
```bash
git add <file>
git commit -m "Your clear message"
git push origin main
```

---

### 📁 Optional: Check database content
You can open the SQLite database using tools like:
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- Or via CLI:
```bash
sqlite3 db/database.db
```

---

### 🔄 Why keep these commands?
You can quickly set up, test, or troubleshoot the app without guessing what to do next.

## 👥 User Management

We added a simple **user management panel** so that admins can manage users directly from the app.

---

### 🔷 Features
✅ Admins can view all users  
✅ Add a new user (username, password, role)  
✅ Edit an existing user’s password or role  
✅ Delete a user  
✅ Only users with `role='admin'` can access this panel

---

### 🔷 Where to find it
After logging in as an admin:
- On the **Dashboard**, you see a **👥 Manage Users** button.
- Regular users do **not** see this button.

---

### 🔷 Code files involved
- `ui/manage_users_window.py` → The user management UI & logic
- `ui/dashboard_window.py` → Shows/hides the button depending on role

---

### 🔷 Why it was added
To make the app feel more complete and realistic.  
Instead of editing the database manually to add users, admins can create & manage them easily through the app.

---

### 🔷 Notes
- Users table is created by `db_manager.py`.
- Default admin & user are inserted as:
  - `admin / admin123 / admin`
  - `user1 / user123 / user`
- You can reset the DB anytime (see Helpful Commands above).

## 🔎 Search, Filter, Export & Low Stock Alerts

We enhanced the **View Products** screen with more advanced features to make it easier to use.

---

### 🔷 Features
✅ Search products by name or SKU  
✅ Filter products by category  
✅ Reset filters to see all products  
✅ Export the currently visible product list to a CSV file  
✅ Highlight products that have **low stock** (below a certain threshold)

---

### 🔷 Where to find it
After logging in → Dashboard → 📦 View Products:
- You’ll see a **Search bar** and a **Category dropdown** above the products table.
- You’ll also see:
  - 🔄 Reset Filters button
  - 📄 Export to CSV button

---

### 🔷 Code files involved
- `ui/view_products_window.py` → updated with:
  - `QLineEdit` for search
  - `QComboBox` for category filter
  - low stock highlighting logic
  - export-to-CSV logic

---

### 🔷 Why it was added
This improves usability for inventory managers:
- Quickly find specific products
- Focus on a specific category
- Take a snapshot of current stock into Excel/CSV
- Get visual feedback about products that need reordering

---

### 🔷 Notes
- Low stock threshold can be adjusted in the code.
- Exported CSV includes all currently visible products (with filters applied).

---

### Helpful commands used here
Nothing special; this feature was added directly in the PyQt code.
You can reset the database as usual and it’ll still work because it reads live data.

## 🪵 Logs & Logging Actions

We implemented a **logging system** to track who does what in the application — very useful for audit and accountability.

---

### 🔷 Features
✅ Every important action (e.g., deleting a product) is recorded in the `logs` table.  
✅ You can view these logs from the dashboard.

---

### 🔷 Where to find it
After logging in → Dashboard → 📊 View Inventory Logs:
- You’ll see a table listing:
  - Timestamp
  - Username
  - Action
  - Product name (if applicable)

---

### 🔷 Code files involved
- `models/db_manager.py`
  - Function: `log_action(username, action, product_name)`  
  - Inserts a record into the `logs` table.

- `ui/view_logs_window.py`
  - Displays logs in a table when user clicks "View Inventory Logs".

- `ui/dashboard_window.py`
  - Adds a button for logs.

---

### 🔷 Why it was added
Logging is essential to:
- See which user deleted, added, or modified data
- Investigate mistakes or misuse
- Provide accountability

---

### 🔷 Notes
- Logs are written automatically whenever an action like delete occurs.
- You can also manually call `log_action()` anywhere in the code to log custom actions.

---

### Helpful commands used here
No external commands — logs are handled internally by the app in SQLite.

## 👥 Admin-Only Manage Users CRUD

We added full **CRUD (Create, Read, Update, Delete)** functionality for managing users — only available to **admins**.

---

### 🔷 Features
✅ Admin can create new users (username, password, role).  
✅ Admin can edit existing users.  
✅ Admin can delete users.  
✅ Admin can see all users in a table.  
✅ Regular users **cannot** access this feature.

---

### 🔷 Where to find it
After logging in **as admin** → Dashboard → 👥 Manage Users

---

### 🔷 Code files involved
- `ui/manage_users_window.py`
  - Handles the entire UI for adding, editing, deleting, and listing users.
  - Shows a table of all users with Edit/Delete buttons.
  - Provides inputs for creating a new user.
  
- `ui/dashboard_window.py`
  - Adds the 👥 **Manage Users** button.
  - The button is only shown if the logged-in user’s `role == 'admin'`.

- `models/db_manager.py`
  - Handles the `users` table.

---

### 🔷 Why it was added
- To allow admins to control who can log in and what roles they have.
- Essential for multi-user systems where you want fine-grained access.

---

### 🔷 Notes
- On login, the `role` of the user is fetched from the database.
- Regular users don’t even see the 👥 Manage Users button.
- User passwords are currently stored as plaintext in the database (🚨 improvement suggestion: hash them).

---

### Helpful commands / steps
No external commands needed — this is all within the app.

---

## 🔍 Search, Filter & Low Stock Alerts in Products Table

We improved the products table to make it easier to use and added a helpful stock alert.

---

### 🔷 Features
✅ Search products by Name or SKU (live filtering).  
✅ Filter products by Category (dropdown).  
✅ Reset Filters button to clear search & category.  
✅ Highlights (🔴) products with stock below a threshold (default: ≤ 5) right in the table.

---

### 🔷 Where to find it
Dashboard → 📦 View Products

---

### 🔷 Code files involved
- `ui/view_products_window.py`
  - Added `QLineEdit` for search.
  - Added `QComboBox` for categories.
  - Reloads product table based on search text and selected category.
  - Highlights low stock quantities in red text.
  - Adds a "Reset Filters" button.

---

### 🔷 Why it was added
- To make it easier to find specific products when the list is long.
- To quickly notice which products need to be restocked.
- Improves usability and helps with inventory management.

---

### Helpful commands / steps
No external commands — simply launch the app, log in, go to 📦 View Products and try searching, filtering, or spot low-stock products.

---

## 📄 Export Products Table to CSV

We added a feature to export the currently displayed products table (with search & filter applied) to a `.csv` file.  

---

### 🔷 Features
✅ Exports **only what is currently shown in the table**.  
✅ CSV includes headers: ID, Name, Category, SKU, Price, Quantity.  
✅ You choose where to save the file with a Save File dialog.  
✅ Success or error message is shown after export.

---

### 🔷 Where to find it
Dashboard → 📦 View Products → Button at bottom: `📄 Export to CSV`

---

### 🔷 Code files involved
- `ui/view_products_window.py`
  - Uses `csv` module and `QFileDialog` to save data.
  - Button added at bottom of product table.
  - Loops over `self.products_data` (already filtered) to write rows.

---

### 🔷 Why it was added
- Users often want to analyze, share, or back up their inventory data.
- CSV can be opened in Excel, Google Sheets, or any text editor.

---

### Helpful commands / steps
🖱 Run the app → Login → View Products → Filter/search if desired → Click `📄 Export to CSV` → Choose a location → Done!

---

## 👥 User Management (CRUD for Users)

We added a full **User Management Panel** where admins can create, edit, and delete users.

---

### 🔷 Features
✅ View a list of all users with their roles.  
✅ Add new users (username, password, role).  
✅ Edit existing users (change password or role).  
✅ Delete users.  
✅ Only accessible to admin accounts.

---

### 🔷 Where to find it
Dashboard → 👥 Manage Users (only visible when logged in as `admin`)

---

### 🔷 Code files involved
- `ui/manage_users_window.py` → New window implementing CRUD.
- `ui/dashboard_window.py` → Shows 👥 button only if `role == 'admin'`.
- `models/db_manager.py` → Uses existing database tables (`users`).

---

### 🔷 Why it was added
- Initially, the app only supported a hardcoded admin and user.
- We wanted the admin to dynamically manage team members and control access without touching the database directly.

---

### Helpful commands / steps
🖱 Run the app → Login as `admin` → Click 👥 Manage Users → Use Add/Edit/Delete as needed.

---

## 🚨 Low Stock Alerts

We added a feature to **highlight products with low stock** in the Products table.

---

### 🔷 Features
✅ When a product’s `quantity_in_stock` is less than `5`, its row is highlighted in the table (light red background).  
✅ Helps the admin quickly identify items that need restocking.  
✅ Works even when filters/search are applied.

---

### 🔷 Where to find it
Dashboard → 📦 View Products → See the table → Products with stock `< 5` are highlighted.

---

### 🔷 Code files involved
- `ui/view_products_window.py`
  - Added check inside `load_products()` to set row background color if stock is low.

---

### 🔷 Why it was added
- Makes inventory management more proactive.
- Saves time by visually indicating which products require attention.

---

### Helpful commands / steps
🖱 Run the app → Login → Go to 📦 View Products → Observe any highlighted rows if low stock exists.

---

