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

    def test_location_creation_fails_for_bad_input(self):
        """Test if location creation fails for bad input"""

        self.weconnect.register(self.user)

        self.assertRaises(
            TypeError, self.weconnect.create_location, 'johndoe', 1, 2)

    def test_location_creation_fails_for_non_user(self):
        """Test if location creation fails for non user"""

        self.assertEqual("Username does not exist!", self.weconnect.create_location(
            'johndoe', 'Kabale', 'Kabale road'))

    def test_location_creation_fails_for_existent_location(self):
        """Test if location creation fails if location exists"""

        self.weconnect.register(self.user)
        self.weconnect.create_location(
            'johndoe', 'Kabale', 'Kabale road')

        self.assertEqual("This location already exists!", self.weconnect.create_location(
            'johndoe', 'Kabale', 'Kabale road'))

    def test_location_view_fails_for_bad_input(self):
        """Test if location is not viewed"""

        self.weconnect.register(self.user)
        self.weconnect.create_location(
            'johndoe', 'Kabale', 'Kabale road')
        self.weconnect.view_location('johndoe', 'Kabale')

        self.assertEqual("Location does not exist!",
                         self.weconnect.view_location('johndoe', 'Fake location'))
        self.assertEqual("Username does not exist!",
                         self.weconnect.view_location('fakeuser', 'Kabale'))

    def test_location_edit_fails_for_bad_input(self):
        """Test if location edit fails"""

        self.weconnect.register(self.user)
        self.weconnect.register(self.b_user)
        self.weconnect.create_location(
            'johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_location(
            'janedoe', 'Kampala', 'Kampala road')

        self.assertRaises(
            TypeError, self.weconnect.edit_location, 'johndoe', 'Kabale', 2)
        self.assertEqual("User did not create the location!", self.weconnect.edit_location(
            'janedoe', 'Kabale', 'Kabale road opposite shell'))

    def test_location_delete_fails_for_bad_input(self):
        """Test if location delete fails"""

        self.weconnect.register(self.user)
        self.weconnect.register(self.b_user)
        self.weconnect.create_location(
            'johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_location(
            'janedoe', 'Kampala', 'Kampala road')

        self.assertEqual("User did not create the location!", self.weconnect.delete_location(
            'janedoe', 'Kabale'))