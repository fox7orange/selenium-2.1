Scenario: Addition and deletion products
  Given 3 products added to the cart
  When all products are deleted from the cart
  Then no products in the cart
