import csv
import os

class PersonalizedBudgetManager:
    def __init__(self, data_file='budget_data.csv'):
        self.data_file = data_file
        self.categories = ["Food", "Rent", "Transport", "Entertainment", "Other"]
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Category', 'Amount'])

    def add_expense(self, category_index, amount):
        category = self.categories[category_index - 1]
        with open(self.data_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([category, amount])
        print(f"✅ Recorded: {category} - ${amount}")

    def calculate_stats(self):
        amounts = []
        with open(self.data_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                amounts.append(float(row['Amount']))
        
        if not amounts:
            return None

        # --- Manual Statistics (Course Concept Application) ---
        total = sum(amounts)
        count = len(amounts)
        mean = total / count
        
        # Variance calculation for 'Volatility'
        variance = sum((x - mean) ** 2 for x in amounts) / count
        std_deviation = variance ** 0.5
        
        return {
            "total": total,
            "mean": mean,
            "std_dev": std_deviation,
            "count": count
        }

    def provide_logic_advice(self, budget_limit):
        stats = self.calculate_stats()
        if not stats: return "No data recorded yet."

        total = stats['total']
        # Logical Rule: Assessing spending vs budget
        if total > budget_limit:
            return "🛑 STATUS: Over-Budget. Reduce 'Other' category spending immediately."
        elif total > (budget_limit * 0.8):
            return "⚠️ STATUS: Tight. You have less than 20% of your budget left."
        else:
            return "✅ STATUS: Healthy. You are managing your finances well."

def main():
    manager = PersonalizedBudgetManager()
    print("--- 💰 BYOP: Personalized Budget Manager ---")
    
    try:
        limit = float(input("Enter your monthly budget goal: "))
    except ValueError:
        print("Invalid input. Defaulting to 1000.")
        limit = 1000.0

    while True:
        print("\n[1] Add Expense [2] Financial Report [3] Exit")
        choice = input("Select: ")

        if choice == '1':
            print("\nCategories:")
            for i, cat in enumerate(manager.categories, 1):
                print(f"{i}. {cat}")
            
            try:
                c_idx = int(input("Category Number: "))
                amt = float(input("Amount spent: "))
                manager.add_expense(c_idx, amt)
            except (ValueError, IndexError):
                print("❌ Invalid input. Please try again.")

        elif choice == '2':
            stats = manager.calculate_stats()
            if stats:
                print("\n--- STATISTICAL SUMMARY ---")
                print(f"Total Expenditure:  {stats['total']:.2f}")
                print(f"Average Spending:   {stats['mean']:.2f}")
                print(f"Spending Volatility: {stats['std_dev']:.2f} (Std Dev)")
                print(f"Advice: {manager.provide_logic_advice(limit)}")
            else:
                print("No data found.")

        elif choice == '3':
            break

if __name__ == "__main__":
    main()
