import json
import sys

from colorama import init
from internal.card import Logger, init_card
from internal.consts import *

init()


def buy(card, product: str, price: float):
    """
    Simulate a purchase transaction with the vending machine

    Args:
        card: The card instance
        product: Name of the product to purchase
        price: Price of the product
    """
    print(
        f"\nAttempting to purchase {GREEN(product)} for {YELLOW('$' + str(price))}..."
    )

    # Create transaction payload
    transaction = {"product": product, "price": price}

    # Convert transaction to bytes
    payload = json.dumps(transaction).encode("utf-8")

    try:
        # Encrypt the transaction data for the server
        encrypted = card.encrypt_for_server(payload)

        print("\nTransaction encrypted successfully!")
        print(f"Encrypted payload: {YELLOW(encrypted.data.hex())}")

        return encrypted.data

    except Exception as e:
        print(RED(f"\nError during transaction: {e}"))
        if Logger.log_verbose:
            import traceback

            traceback.print_exc()
        return None


def main():
    # Enable verbose logging if -v flag is present
    if "-v" in sys.argv:
        Logger.log_verbose = True

    print(CYAN("Initializing vending machine..."))
    card = init_card()
    print(GREEN("Vending machine ready!"))

    while True:
        print("\nAvailable products:")
        print(f"1. {YELLOW('Water')} - $1.50")
        print(f"2. {YELLOW('Soda')} - $2.00")
        print(f"3. {YELLOW('Snack')} - $2.50")
        print(f"4. {RED('Exit')}")

        try:
            choice = input(CYAN("\nSelect a product (1-4): "))

            if choice == "4":
                print(YELLOW("\nThank you for using our vending machine!"))
                break

            if choice not in ["1", "2", "3"]:
                print(RED("Invalid choice! Please select 1-4"))
                continue

            products = {"1": ("Water", 1.50), "2": ("Soda", 2.00), "3": ("Snack", 2.50)}

            product, price = products[choice]
            encrypted_data = buy(card, product, price)

            if encrypted_data:
                print(GREEN("\nTransaction completed successfully!"))
                print(f"Please collect your {YELLOW(product)}")

        except KeyboardInterrupt:
            print(YELLOW("\nTransaction cancelled"))
            break
        except Exception as e:
            print(RED(f"\nError: {e}"))
            if Logger.log_verbose:
                import traceback

                traceback.print_exc()


if __name__ == "__main__":
    main()
