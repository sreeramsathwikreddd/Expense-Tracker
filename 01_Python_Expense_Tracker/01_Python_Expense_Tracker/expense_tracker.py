import csv
from datetime import date
from pathlib import Path

FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["date", "category", "description", "amount"]

def ensure_file():
    if not FILE.exists():
        with FILE.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()

def add_expense():
    category = input("Category: ").strip() or "Other"
    description = input("Description: ").strip() or "No description"
    try:
        amount = float(input("Amount: ₹").strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Enter a valid amount greater than zero.")
        return
    with FILE.open("a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerow({
            "date": date.today().isoformat(), "category": category,
            "description": description, "amount": f"{amount:.2f}"
        })
    print("Expense saved.")

def read_expenses():
    ensure_file()
    with FILE.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def show_expenses():
    rows = read_expenses()
    if not rows:
        print("No expenses yet.")
        return
    print(f"\n{'DATE':<12} {'CATEGORY':<16} {'DESCRIPTION':<24} {'AMOUNT':>10}")
    print("-" * 66)
    for r in rows:
        print(f"{r['date']:<12} {r['category'][:16]:<16} {r['description'][:24]:<24} ₹{float(r['amount']):>9.2f}")

def show_totals():
    totals = {}
    for r in read_expenses():
        totals[r["category"]] = totals.get(r["category"], 0) + float(r["amount"])
    if not totals:
        print("No expenses yet.")
        return
    for category, total in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"{category:<20} ₹{total:.2f}")
    print(f"{'TOTAL':<20} ₹{sum(totals.values()):.2f}")

def main():
    ensure_file()
    while True:
        print("\n=== Expense Tracker ===\n1. Add expense\n2. View expenses\n3. Category totals\n4. Exit")
        choice = input("Select: ").strip()
        if choice == "1": add_expense()
        elif choice == "2": show_expenses()
        elif choice == "3": show_totals()
        elif choice == "4": break
        else: print("Choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
