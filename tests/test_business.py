# tests/test_business.py
"""This script tests the functionality of Business class"""

from tests.test_weconnect import WeConnectTestCase


class TestLocation(WeConnectTestCase):
    """Test Business class functionality."""

    def test_business_creation(self):
        """Test if business is created"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_location('johndoe', 'Kabale', 'Kabale road')
        business = self.weconnect.create_business(
            'johndoe', 'Buyondo Hardware', 'One stop center for building materials...',
            'Construction', 'Kabale', 'path to photo')

        self.assertEqual(business.name, 'Buyondo Hardware', msg='Business was not created')

    def test_business_view(self):
        """Test if business is viewed"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_location('johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_business(
            'johndoe', 'Buyondo Hardware', 'One stop center for building materials...',
            'Construction', 'Kabale', 'path to photo')
        business = self.weconnect.view_business('johndoe', 'Buyondo Hardware')

        self.assertEqual('Buyondo Hardware', business.name,
                         msg='Business does not exist')

    def test_business_edit(self):
        """Test if business is edited"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_location('johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_business(
            'johndoe', 'Buyondo Hardware', 'One stop center for building materials...',
            'Construction', 'Kabale', 'path to photo')
        updated_business = self.weconnect.edit_business(
            'johndoe', 'Buyondo Hardware', 'We provide all your building needs',
            'Construction', 'Kabale', 'path to photo')

        self.assertEqual('We provide all your building needs',
                         updated_business.description, msg='Business was not edited')

    def test_business_deletion(self):
        """Test if business is deleted"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_location('johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_business(
            'johndoe', 'Buyondo Hardware', 'One stop center for building materials...',
            'Construction', 'Kabale', 'path to photo')
        businesses = self.weconnect.delete_business('johndoe', 'Buyondo Hardware')

        self.assertNotIn('Buyondo Hardware', businesses.keys(),
                         msg='Business was not deleted')
