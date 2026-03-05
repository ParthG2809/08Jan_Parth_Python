repair_orders = []

def add_repair_order():
    print("\n--- New Repair Order ---")
    customer = input("Customer Name: ").strip()
    device = input("Device Type: ").strip()
    issue = input("Issue Description: ").strip()
    due_date = input("Due Date (DD-MM-YYYY): ").strip()

    order = {
        "customer": customer,
        "device": device,
        "issue": issue,
        "due_date": due_date,
        "status": "Pending"
    }

    repair_orders.append(order)
    print("Repair order added successfully!")


def view_orders():
    if not repair_orders:
        print("\nNo repair orders found.")
        return

    print("\n--- Repair Orders ---")

    for i in range(len(repair_orders)):
        order = repair_orders[i]
        print(str(i + 1) + ". " + order["customer"] + " | " + order["device"] + " | " + order["status"])


def generate_bill():
    if not repair_orders:
        print("\nNo repair orders available.")
        return

    view_orders()

    try:
        choice = int(input("\nSelect order number to generate bill: ")) - 1
        order = repair_orders[choice]
    except:
        print("Invalid selection.")
        return

    print("\n--- Billing Section ---")

    try:
        service_fee = float(input("Repair Service Fee (₹): "))
    except:
        print("Invalid amount.")
        return

    parts = []

    while True:
        part = input("Enter part name (or 'done' to finish): ").strip()

        if part.lower() == "done":
            break

        try:
            cost = float(input("Cost of " + part + " (₹): "))
            parts.append(cost)
        except:
            print("Invalid cost.")

    parts_total = sum(parts)
    subtotal = service_fee + parts_total

    tax = subtotal * 0.18
    discount = float(input("Discount (enter 0 if there is no discount): "))

    final_amount = subtotal + tax - discount

    order["status"] = "Completed"

    print("\n========== FIXTRACK INVOICE ==========")
    print("Customer Name :", order["customer"])
    print("Device        :", order["device"])
    print("Issue         :", order["issue"])
    print("-------------------------------------")
    print("Service Fee   : ₹", service_fee)
    print("Parts Cost    : ₹", parts_total)
    print("Subtotal      : ₹", subtotal)
    print("GST (18%)     : ₹", tax)
    print("Discount      : ₹", discount)
    print("-------------------------------------")
    print("TOTAL PAYABLE : ₹", final_amount)
    print("=====================================")