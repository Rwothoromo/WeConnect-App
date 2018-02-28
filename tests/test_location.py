# tests/test_location.py
"""This script tests the functionality of Location class"""

from tests.test_weconnect import WeConnectTestCase


class TestLocation(WeConnectTestCase):
    """Test Location class functionality."""

    def test_location_creation(self):
        """Test if location is created"""

        self.weconnect.register(self.user)
        locations = self.weconnect.create_location(
            'johndoe', 'Kampala', 'Kampala road')

        self.assertTrue(locations['Kampala'], msg='Location was not created')

    def test_location_view(self):
        """Test if location is viewed"""

        self.weconnect.register(self.user)
        self.weconnect.create_location('johndoe', 'Kampala', 'Kampala road')
        location = self.weconnect.view_location('johndoe', 'Kampala')

        self.assertEqual('Kampala', location.name,
                         msg='Location does not exist')

    def test_location_edit(self):
        """Test if location is edited"""

        self.weconnect.register(self.user)
        self.weconnect.create_location('johndoe', 'Kampala', 'Kampala road')
        locations = self.weconnect.edit_location(
            'johndoe', 'Kampala', 'Kampala shopping malls')

        self.assertEqual('Kampala shopping malls',
                         locations['Kampala'].description, msg='Location was not edited')

    def test_location_deletion(self):
        """Test if location is deleted"""

        self.weconnect.register(self.user)
        self.weconnect.create_location('johndoe', 'Kampala', 'Kampala road')
        locations = self.weconnect.delete_location('johndoe', 'Kampala')

        self.assertNotIn('Kampala', locations.keys(),
                         msg='Location was not deleted')
