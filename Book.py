import pandas as pd
from openpyxl import load_workbook

# === Sheet 1: Sets Summary ===
sets_data = [
    # Set ID, Set Name, Total Quantity, Ad Expense, Packaging Expense, Set Status (Open/Closed)
    ["001", "Starter Set", 15, 20.00, 10.00, "Open"],
    ["002", "Adventure Pack", 20, 15.00, 7.00, "Closed"],
]

sets_columns = [
    "Set ID", "Set Name", "Total Quantity", "Ad Expense", "Packaging Expense", "Set Status (Open/Closed)",
    "Total Cost", "Total Revenue", "Total Profit", "20% Equity Withdrawn", "Date Closed"
]

df_sets = pd.DataFrame(sets_data, columns=sets_columns[:6])
# Create empty columns for formulas
for col in sets_columns[6:]:
    df_sets[col] = ""

# === Sheet 2: Books Details ===
books_data = [
    # Set ID, Book Title, Quantity, Cost per Book, Selling Price per Book, Sold Quantity
    ["001", "Book A", 10, 5.00, 10.00, 5],
    ["001", "Book B", 5, 7.00, 15.00, 3],
    ["002", "Book C", 8, 6.00, 12.00, 8],
    ["002", "Book D", 12, 4.50, 11.00, 10],
]

books_columns = [
    "Set ID", "Book Title", "Quantity", "Cost per Book", "Selling Price per Book", "Sold Quantity",
    "Total Cost", "Total Revenue", "Total Profit"
]

df_books = pd.DataFrame(books_data, columns=books_columns[:6])
# Add empty columns for formulas
for col in books_columns[6:]:
    df_books[col] = ""

# === Save to Excel with two sheets ===
excel_filename = "Instagram_Bookstore_MultiSheet_Tracker.xlsx"
with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
    df_sets.to_excel(writer, sheet_name="Sets", index=False)
    df_books.to_excel(writer, sheet_name="Books", index=False)

# === Now load the workbook to add formulas ===
wb = load_workbook(excel_filename)

# --- Add formulas in the Books sheet ---
ws_books = wb["Books"]
for row in range(2, len(df_books) + 2):
    qty = f"C{row}"
    cost_per_book = f"D{row}"
    price_per_book = f"E{row}"
    sold_qty = f"F{row}"

    ws_books[f"G{row}"] = f"={qty}*{cost_per_book}"  # Total Cost
    ws_books[f"H{row}"] = f"={sold_qty}*{price_per_book}"  # Total Revenue
    ws_books[f"I{row}"] = f"=H{row}-G{row}"  # Total Profit

# --- Add formulas in the Sets sheet ---
ws_sets = wb["Sets"]
for row in range(2, len(df_sets) + 2):
    set_id = ws_sets[f"A{row}"].value
    ad_expense = f"D{row}"
    packaging_expense = f"E{row}"
    status_cell = f"F{row}"

    # Sum total cost of all books in this set (from Books sheet)
    ws_sets[f"G{row}"] = f'=SUMIF(Books!$A$2:$A${len(df_books)+1},"{set_id}",Books!$G$2:$G${len(df_books)+1}) + {ad_expense} + {packaging_expense}'

    # Sum total revenue of all books in this set (from Books sheet)
    ws_sets[f"H{row}"] = f'=SUMIF(Books!$A$2:$A${len(df_books)+1},"{set_id}",Books!$H$2:$H${len(df_books)+1})'

    # Profit = Revenue - Cost
    ws_sets[f"I{row}"] = f"=H{row}-G{row}"

    # Equity withdrawn = 20% of profit if closed else 0
    ws_sets[f"J{row}"] = f'=IF(F{row}="Closed", MAX(0, 0.2*I{row}), 0)'

wb.save(excel_filename)

print(f"✅ Excel workbook with 'Sets' and 'Books' sheets created: {excel_filename}")
