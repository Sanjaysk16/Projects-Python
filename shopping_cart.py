cart = ('mouse', 'printer', 'hard disk', 'mousepad')
options = ('Add to cart', 'Remove from cart', 'Display cart')
valid_choice = list(range(1, len(options) + 1))
shopping_cart = []


def display_menu():
    """Display the menu options."""
    print("\nMenu:")
    for index, item in enumerate(options, start=1):
        print(f"{index}. {item}")
    print("0. Exit")


def add_to_cart():
    """Prompt the user to add an item to the shopping cart."""
    print("\nAvailable items:")
    for num, item in enumerate(cart, start=1):
        print(f"{num}. {item.capitalize()}")

    add_item = input('Add item: ')
    if add_item.isnumeric():
        add_item = int(add_item)
        if 1 <= add_item <= len(cart):
            item_to_add = cart[add_item - 1]
            shopping_cart.append(item_to_add)
            print(f"{item_to_add.capitalize()} added to the cart!")
        else:
            print("Invalid item number!")
    else:
        print("Invalid input! Please enter a number.")


def remove_from_cart():
    """Prompt the user to remove an item from the shopping cart."""
    if shopping_cart:
        print("\nYour cart:", shopping_cart)
        option = input('Remove item: ').lower()
        if option in shopping_cart:
            shopping_cart.remove(option)
            print(f"{option.capitalize()} removed successfully!")
        else:
            print("Item not present in the cart!")
    else:
        print("Your cart is empty!")


def display_cart():
    """Display the current items in the shopping cart."""
    print("\n---- CART ----")
    if shopping_cart:
        for item in shopping_cart:
            print(f"- {item.capitalize()}")
    else:
        print("Your cart is empty!")


choice = None
while choice != 0:
    display_menu()
    try:
        choice = int(input('Enter your choice: '))
        if choice == 1:
            add_to_cart()  # invoking functions
        elif choice == 2:
            remove_from_cart()
        elif choice == 3:
            display_cart()
        elif choice == 0:
            print("Exiting...")
        else:
            print("Invalid choice! Please enter a valid option.")
    except ValueError:
        print("Invalid input! Please enter a number.")
