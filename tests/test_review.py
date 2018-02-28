# tests/test_review.py
"""This script tests the functionality of Review class"""

from tests.test_weconnect import WeConnectTestCase


class TestReview(WeConnectTestCase):
    """Test Review class functionality."""

    def test_review_creation(self):
        """Test if review is created"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_location('johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_business(
            'johndoe', 'Buyondo Hardware', 'One stop center for building materials...',
            'Construction', 'Kabale', 'path to photo')
        review = self.weconnect.create_review(
            'johndoe', 'Good service', 'I even got a soda', 'Buyondo Hardware')

        self.assertEqual(review.name, 'Good service', msg='Review was not created')

    def test_review_view(self):
        """Test if review is viewed"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_location('johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_business(
            'johndoe', 'Buyondo Hardware', 'One stop center for building materials...',
            'Construction', 'Kabale', 'path to photo')
        self.weconnect.create_review(
            'johndoe', 'Good service', 'I even got a soda', 'Buyondo Hardware')
        review = self.weconnect.view_review('johndoe', 'Good service')

        self.assertEqual('Good service', review.name, msg='Review does not exist')

    def test_review_edit(self):
        """Test if review is edited"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_location('johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_business(
            'johndoe', 'Buyondo Hardware', 'One stop center for building materials...',
            'Construction', 'Kabale', 'path to photo')
        self.weconnect.create_review(
            'johndoe', 'Good service', 'I even got a soda', 'Buyondo Hardware')
        reviews = self.weconnect.edit_review(
            'johndoe', 'Good service', 'I even got a soda and cake', 'Buyondo Hardware')

        self.assertEqual('I even got a soda and cake',
                         reviews['Good service'].description, msg='Review was not edited')

    def test_review_deletion(self):
        """Test if review is deleted"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_location('johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_business(
            'johndoe', 'Buyondo Hardware', 'One stop center for building materials...',
            'Construction', 'Kabale', 'path to photo')
        self.weconnect.create_review(
            'johndoe', 'Good service', 'I even got a soda', 'Buyondo Hardware')
        reviews = self.weconnect.delete_review('johndoe', 'Good service')

        self.assertNotIn('Good service', reviews.keys(),
                         msg='Review was not deleted')
