import unittest
from app import app
from models import Product

class ProductCRUDTestcases(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        app.config["SERVER_NAME"] = "grupp5.se"
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []  # This is the magic
        app.config['TESTING'] = True

    def test_to_add_new_product_that_already_existis(self):
        test_client = app.test_client()
        url = '/addproduct'
        count = Product.query.count()
        product = Product.query.first()
        with test_client:
            response = test_client.post(url, data={"ProductName": product.ProductName, "CategoryId": 1, "QuantityPerUnit": "36 boxes", "UnitPrice": 25, "UnitsInStock": 20, "ReorderLevel": 10, "Discontinued": True})
            count2 = Product.query.count()
            self.assertEqual(count, count2)
            assert response.status_code != 302

    def test_to_update_product_with_productname_that_already_exists(self):
        test_client = app.test_client()
        productToEdit = Product.query.first()
        url = f'/editproduct/{productToEdit.ProductID}'
        otherproduct = Product.query.filter(Product.ProductID == productToEdit.ProductID+1).first()
        with test_client:
            response = test_client.post(url, data={"ProductName": otherproduct.ProductName, "CategoryId": productToEdit.CategoryId, "QuantityPerUnit": productToEdit.QuantityPerUnit, "UnitPrice": productToEdit.UnitPrice, "UnitsInStock": productToEdit.UnitsInStock, "ReorderLevel": productToEdit.ReorderLevel, "Discontinued": productToEdit.Discontinued})
            self.assertNotEqual(productToEdit.ProductName, otherproduct.ProductName)
            assert response.status_code != 302

if __name__ == "__main__":
    unittest.main()