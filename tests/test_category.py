# app/tests/test_category.py
"""This script tests the functionality of Category class"""

from tests.test_weconnect import WeConnectTestCase


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
