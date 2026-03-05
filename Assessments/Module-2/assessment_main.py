from assessment import *


def main():
    while True:
        print("\n===== FixTrack Menu =====")
        print("1. Add Repair Order")
        print("2. View Repair Orders")
        print("3. Generate Bill")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            add_repair_order()

        elif choice == "2":
            view_orders()

        elif choice == "3":
            generate_bill()

        elif choice == "4":
            print("Exiting FixTrack. Have a great day!")
            break

        else:
            print("Invalid option. Try again.")


main()