import unittest
from app import app
from models import Category

class ProductCRUDTestcases(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        app.config["SERVER_NAME"] = "grupp5.se"
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHODS'] = []  # This is the magic
        app.config['TESTING'] = True


    def test_to_add_new_category_that_already_existis(self):
        test_client = app.test_client()
        url = '/addcategory'
        count = Category.query.count()
        category = Category.query.first()
        with test_client:
            response = test_client.post(url, data={"CategoryName": category.CategoryName, "Description": "lalalaal"})
            count2 = Category.query.count()
            self.assertEqual(count, count2)
            assert response.status_code != 302

    def test_to_update_category_with_categoryname_that_already_exists(self):
        test_client = app.test_client()
        categoryToEdit = Category.query.first()
        url = f'/editcategory/{categoryToEdit.CategoryID}'
        othercategory = Category.query.filter(Category.CategoryID == categoryToEdit.CategoryID+1).first()
        with test_client:
            response = test_client.post(url, data={"CategoryName": othercategory.CategoryName, "Description": "lalalaal"})
            self.assertNotEqual(categoryToEdit.CategoryName, othercategory.CategoryName)
            assert response.status_code != 302

if __name__ == "__main__":
    unittest.main()