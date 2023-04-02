import unittest
import tkinter as tk
from tkinter import messagebox

from cashregister import CashRegister


class TestCashRegister(unittest.TestCase):

    def setUp(self):
        self.app = CashRegister()

    def test_add_to_cart(self):
        item = {"name": "Item 1", "price": 10.0}
        self.app.add_to_cart(item)
        self.assertIn(item, self.app.cart)
        self.assertIn(f"{item['name']} - {item['price']:.2f}", self.app.cart_listbox.get(0, tk.END))

    def test_clear_cart(self):
        item = {"name": "Item 1", "price": 10.0}
        self.app.add_to_cart(item)
        self.app.clear_cart()
        self.assertEqual(len(self.app.cart), 0)
        self.assertEqual(self.app.total_price, 0)
        self.assertEqual(self.app.cart_listbox.size(), 0)

    def test_search_items(self):
        self.app.search_entry.insert(0, "Item 1")
        self.app.search_items()
        self.assertEqual(self.app.root.children['!label'].cget("text"), "Item 1")
        self.assertEqual(self.app.root.children['!label2'].cget("text"), "10.00 ₽")
        self.assertEqual(self.app.root.children['!button'].cget("text"), "Добавить")

    def test_scan_barcode(self):
        item = {"name": "Item 1", "price": 10.0, "barcode": "1234567890"}
        self.app.scanner.items = [item]
        self.app.barcode_entry.insert(0, item["barcode"])
        self.app.scan_barcode()
        self.assertIn(item, self.app.cart)
        self.assertIn(f"{item['name']} - {item['price']:.2f}", self.app.cart_listbox.get(0, tk.END))

    def test_calculate_tax(self):
        self.app.total_price = 100
        self.app.calculate_tax()
        self.assertEqual(self.app.total_price, 113)

    def test_filter_items(self):
        items = [
            {"name": "Item 1", "price": 10.0},
            {"name": "Item 2", "price": 20.0},
            {"name": "Item 3", "price": 30.0},
        ]
        self.assertEqual(self.app.filter_items("Item 1"), [items[0]])
        self.assertEqual(self.app.filter_items("2"), [items[1]])
        self.assertEqual(self.app.filter_items("item"), items)

    def test_checkout(self):
        self.app.discount_entry.insert(0, "0.1")
        self.app.total_price = 100
        self.app.checkout()
        self.assertEqual(self.app.total_price, 113)
        self.assertEqual(messagebox.showinfo.call_args[0][0], "Спасибо за покупку!")
        self.assertEqual(messagebox.showinfo.call_args[1]['message'], f"Сумма покупки: {self.app.total_price:.2f} ₽")


if __name__ == '__main__':
    unittest.main()
