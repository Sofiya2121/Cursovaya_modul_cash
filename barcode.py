from tkinter import messagebox


class BarcodeScanner:
    def __init__(self, products, add_to_cart):
        self.products = products
        self.add_to_cart = add_to_cart

    def scan(self, barcode):
        for product in self.products:
            if barcode == product["barcode"]:
                self.add_to_cart(product)
                return

        # Barcode not found
        messagebox.showerror("Ошибка", "Не верный ШК товара")

