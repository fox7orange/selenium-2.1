from Apps.app import Application


def test_13(app: Application):
    app.add_products_to_cart(3)
    app.delete_all_products_from_cart()
