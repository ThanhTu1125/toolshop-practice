from pages.base_page import BasePage


def money(text: str) -> float:
    """'$28.30' -> 28.3"""
    return float(text.replace("$", "").replace(",", "").strip())


class CartPage(BasePage):
    path = "/checkout"

    def __init__(self, page):
        super().__init__(page)
        # TODO B1.4: product_titles, quantities, line_prices, total
        # TODO B1.6: continue_shopping
        self.product_titles = page.get_by_test_id("product-title")
        self.quantities = page.get_by_test_id("product-quantity")
        self.line_prices = page.get_by_test_id("line-price")
        self.total = page.get_by_test_id("cart-total")
        self.continue_shopping = page.get_by_test_id("continue-shopping")

    def line_totals(self) -> list[float]:    
        return [money(p) for p in self.line_prices.all_inner_texts()]    

    def total_value(self) -> float:
        return money(self.total.inner_text())
