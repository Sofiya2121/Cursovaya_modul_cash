import tkinter as tk
from tkinter import messagebox

from barcode import BarcodeScanner
from items_dict import items


class CashRegister:

    def __init__(self):
        self.cart = []
        self.total_price = 0
        self.tax_rate = 0.13  # New variable for tax rate

        self.root = tk.Tk()  # Define root as an instance variable
        self.root.title("Кассовый аппарат")

        # Items
        tk.Label(self.root, text="Наименование:").grid(row=0, column=0)

        for i, item in enumerate(items):
            tk.Label(self.root, text=item["name"]).grid(row=i + 1, column=0)
            tk.Label(self.root, text="{:.2f} ₽".format(item["price"])).grid(row=i + 1, column=1)
            tk.Button(self.root, text="Добавить", command=lambda item=item: self.add_to_cart(item)).grid(row=i + 1,
                                                                                                         column=2)

        # Cart
        tk.Label(self.root, text="Корзина:").grid(row=0, column=3)
        self.cart_listbox = tk.Listbox(self.root)
        self.cart_listbox.grid(row=1, column=3, rowspan=5)
        tk.Label(self.root, text="Полная стоимость:").grid(row=6, column=3)
        tk.Label(self.root, text="{:.2f} ₽".format(self.total_price)).grid(row=6, column=4)
        tk.Button(self.root, text="Оплатить", command=self.checkout).grid(row=7, column=3)
        tk.Button(self.root, text="Очистить корзину", command=self.clear_cart).grid(row=7, column=4)

        # Cash change
        tk.Label(self.root, text="Оплата:").grid(row=8, column=3)
        self.payment_entry = tk.Entry(self.root)
        self.payment_entry.grid(row=8, column=4)
        tk.Label(self.root, text="Сдача:").grid(row=9, column=3)
        self.change_label = tk.Label(self.root, text="")
        self.change_label.grid(row=9, column=4)
        tk.Button(self.root, text="Рассчитать сдачу", command=self.calculate_change).grid(row=8, column=5)

        # Search
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=6, column=0)
        tk.Button(self.root, text="Найти", command=self.search_items).grid(row=6, column=1)

        # Discounts
        tk.Label(self.root, text="Скидки:").grid(row=0, column=5)
        self.discount_entry = tk.Entry(self.root)
        self.discount_entry.grid(row=1, column=5)
        tk.Label(self.root, text="Способ оплаты:").grid(row=2, column=5)
        options = ["Наличные", "Кредитная карта"]
        self.payment_option = tk.StringVar(self.root)
        self.payment_option.set(options[0])
        tk.OptionMenu(self.root, self.payment_option, *options).grid(row=3, column=5)

        # Scaner barcode
        self.scanner = BarcodeScanner(items, self.add_to_cart)
        tk.Label(self.root, text="Штрих-код:").grid(row=7, column=0)
        self.barcode_entry = tk.Entry(self.root)
        self.barcode_entry.grid(row=7, column=1)

        # Scan button
        tk.Button(self.root, text="Сканировать", command=self.scan_barcode).grid(row=7, column=2)

        self.root.mainloop()

    def calculate_change(self):
        try:
            payment = float(self.payment_entry.get())
            change = payment - self.total_price
            self.change_label.config(text="{:.2f} ₽".format(change))
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат оплаты.")

    def update_total_price(self):
        tk.Label(self.root, text="{:.2f} ₽".format(self.total_price)).grid(row=6, column=4)
        self.change_label.config(text="")

    def calculate_tax(self):
        tax = self.total_price * self.tax_rate
        self.total_price += tax

    def filter_items(self, keyword):
        filtered_items = []
        for item in items:
            if keyword.lower() in item["name"].lower():
                filtered_items.append(item)
        return filtered_items

    def search_items(self):
        keyword = self.search_entry.get()
        if keyword:
            filtered_items = self.filter_items(keyword)
        else:
            filtered_items = items

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == "Наименование:":
                row = widget.grid_info()["row"] + 1
                break

        for child in self.root.winfo_children():
            if isinstance(child, tk.Label) and child.grid_info()["row"] >= row:
                child.grid_forget()

        for i, item in enumerate(filtered_items):
            tk.Label(self.root, text=item["name"]).grid(row=i + row, column=0)
            tk.Label(self.root, text="{:.2f} ₽".format(item["price"])).grid(row=i + row, column=1)
            tk.Button(self.root, text="Добавить", command=lambda item=item: self.add_to_cart(item)).grid(row=i + row,
                                                                                                         column=2)

    def scan_barcode(self):
        barcode = self.barcode_entry.get()
        self.scanner.scan(barcode)

    def add_to_cart(self, product):
        for item in items:
            if item["name"] == product["name"]:
                self.cart.append(item)
                self.cart_listbox.insert(tk.END, item["name"] + " - {:.2f}".format(item["price"]))
                self.total_price += item["price"]
                self.update_total_price()
                break

    def update_total_price(self):
        tk.Label(self.root, text="{:.2f} ₽".format(self.total_price)).grid(row=6, column=4)

    def checkout(self):
        # Get discount, total, and payment method
        tax_price = (self.total_price // 100) * 13
        discount = float(self.discount_entry.get() or 0)
        total = self.total_price * (1 - discount)
        method_of_payment = self.payment_option.get()

        # Add tax to the total price
        self.calculate_tax()

        # Create receipt string
        receipt = "Квитанция кассового аппарата\n\n"
        receipt += "Наименования:\n"
        for item in self.cart:
            receipt += f"{item['name']} - {item['price']:.2f}\n"
        receipt += "\n"
        receipt += f"Скидка: {discount * 100}%\n"
        receipt += f"Итого: {total:.2f} руб.\n"
        receipt += f"Сумма НДС 13%: {tax_price} руб.\n"
        receipt += f"Сумма к оплате: {self.total_price:.2f} руб.\n"
        receipt += f"Способ оплаты: {method_of_payment}\n"

        # Show message box with receipt and clear cart
        tk.messagebox.showinfo("Кассовый аппарат", receipt)
        self.clear_cart()

    def clear_cart(self):
        self.cart = []
        self.cart_listbox.delete(0, tk.END)
        self.total_price = 0
        self.update_total_price()
