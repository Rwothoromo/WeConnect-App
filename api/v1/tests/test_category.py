# tests/test_category.py
"""This script tests the functionality of Category class"""

from api.v1.tests.test_weconnect import WeConnectTestCase


class TestCategory(WeConnectTestCase):
    """Test Category class functionality."""

    def test_category_creation(self):
        """Test if category is created"""

        self.weconnect.register(self.user)
        categories = self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')

        self.assertTrue(categories['Construction'],
                        msg='Category was not created')

    def test_category_view(self):
        """Test if category is viewed"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        category = self.weconnect.view_category('johndoe', 'Construction')

        self.assertEqual('Construction', category.name,
                         msg='Category does not exist')

    def test_category_edit(self):
        """Test if category is edited"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        categories = self.weconnect.edit_category(
            'johndoe', 'Construction', 'building materials')

        self.assertEqual('building materials',
                         categories['Construction'].description, msg='Category was not edited')

    def test_category_deletion(self):
        """Test if category is deleted"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        categories = self.weconnect.delete_category('johndoe', 'Construction')

        self.assertNotIn('Construction', categories.keys(),
                         msg='Category was not deleted')

    def test_category_creation_fails_for_bad_input(self):
        """Test if category creation fails for bad input"""

        self.weconnect.register(self.user)

        self.assertRaises(
            TypeError, self.weconnect.create_category, 'johndoe', 1, 2)

    def test_category_creation_fails_for_non_user(self):
        """Test if category creation fails for non user"""

        self.assertEqual("Username does not exist!", self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials'))

    def test_category_creation_fails_for_existent_category(self):
        """Test if category creation fails if category exists"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')

        self.assertEqual("This category already exists!", self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials'))

    def test_category_view_fails_for_bad_input(self):
        """Test if category is not viewed"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')

        self.assertEqual("Category does not exist!",
                         self.weconnect.view_category('johndoe', 'Fake category'))
        self.assertEqual("Username does not exist!",
                         self.weconnect.view_category('fakeuser', 'Construction'))

    def test_category_edit_fails_for_bad_input(self):
        """Test if category edit fails"""

        self.weconnect.register(self.user)
        self.weconnect.register(self.b_user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_category(
            'janedoe', 'Furniture', 'General furniture')

        self.assertRaises(
            TypeError, self.weconnect.edit_category, 'johndoe', 'Construction', 2)
        self.assertEqual("User did not create the category!", self.weconnect.edit_category(
            'janedoe', 'Construction', 'building materials'))

    def test_category_delete_fails_for_bad_input(self):
        """Test if category delete fails"""

        self.weconnect.register(self.user)
        self.weconnect.register(self.b_user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_category(
            'janedoe', 'Furniture', 'General furniture')

        self.assertEqual("User did not create the category!", self.weconnect.delete_category(
            'janedoe', 'Construction'))
