from pytest_bdd import given, when, then
from Apps.app import Application


@given('3 products added to the cart')
def add_products_to_cart(app: Application):
    app.add_products_to_cart(3)


@when('all products are deleted from the cart')
def delete_all_products_from_cart(app: Application):
    app.delete_all_products_from_cart()


@then('no products in the cart')
def is_any_product_in_the_cart(app: Application):
    app.is_any_product_in_cart()
