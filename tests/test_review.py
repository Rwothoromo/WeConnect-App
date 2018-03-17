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

        self.assertEqual(review.name, 'Good service',
                         msg='Review was not created')

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

        self.assertEqual('Good service', review.name,
                         msg='Review does not exist')

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

    def test_review_creation_fails_for_bad_input(self):
        """Test if review creation fails for bad input"""

        self.weconnect.register(self.user)

        self.assertRaises(
            TypeError, self.weconnect.create_review, 'johndoe', 1, 2)

    def test_review_creation_fails_for_non_user(self):
        """Test if review creation fails for non user"""

        self.assertEqual("Username does not exist!", self.weconnect.create_review(
            'johndoe', 'Good care', 'I was served well', 'Buyondo Hardware'))

    def test_review_creation_fails_for_existent_review(self):
        """Test if review creation fails if review exists"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_location('johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_business(
            'johndoe', 'Buyondo Hardware', 'One stop center for building',
            'Construction', 'Kabale', 'path to photo')
        self.weconnect.create_review(
            'johndoe', 'Good care', 'I was served well', 'Buyondo Hardware')

        self.assertEqual("This review already exists!", self.weconnect.create_review(
            'johndoe', 'Good care', 'I was served well', 'Buyondo Hardware'))

    def test_review_view_fails_for_bad_input(self):
        """Test if review is not viewed"""

        self.weconnect.register(self.user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_location('johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_business(
            'johndoe', 'Bondo', 'One stop center for all',
            'Construction', 'Kabale', 'path to photo')
        self.weconnect.create_business(
            'johndoe', 'Buyondo Hardware', 'One stop center for building',
            'Construction', 'Kabale', 'path to photo')
        self.weconnect.create_review(
            'johndoe', 'Good care', 'I was served well', 'Buyondo Hardware')

        self.assertEqual("Review does not exist!",
                         self.weconnect.view_review('johndoe', 'Fake review'))
        self.assertEqual("Username does not exist!",
                         self.weconnect.view_review('fakeuser', 'Kabale'))

    def test_review_edit_fails_for_bad_input(self):
        """Test if review edit fails"""

        self.weconnect.register(self.user)
        self.weconnect.register(self.b_user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_location('johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_business(
            'johndoe', 'Bondo', 'One stop center for all',
            'Construction', 'Kabale', 'path to photo')
        self.weconnect.create_business(
            'janedoe', 'Buyondo Hardware', 'One stop center for building',
            'Construction', 'Kabale', 'path to photo')
        self.weconnect.create_review(
            'johndoe', 'Good care', 'I was served well', 'Buyondo Hardware')
        self.weconnect.create_review(
            'janedoe', 'Good', 'I was served well', 'Bondo')

        self.assertRaises(
            TypeError, self.weconnect.edit_review, 'johndoe', 'Good care', 1, 'Buyondo Hardware')
        self.assertEqual("User did not create the review!", self.weconnect.edit_review(
            'janedoe', 'Good care', 'I was served so well', 'Buyondo Hardware'))

    def test_review_delete_fails_for_bad_input(self):
        """Test if review delete fails"""

        self.weconnect.register(self.user)
        self.weconnect.register(self.b_user)
        self.weconnect.create_category(
            'johndoe', 'Construction', 'General hardware and construction materials')
        self.weconnect.create_location('johndoe', 'Kabale', 'Kabale road')
        self.weconnect.create_business(
            'johndoe', 'Bondo', 'One stop center for all',
            'Construction', 'Kabale', 'path to photo')
        self.weconnect.create_business(
            'janedoe', 'Buyondo Hardware', 'One stop center for building',
            'Construction', 'Kabale', 'path to photo')
        self.weconnect.create_review(
            'johndoe', 'Good care', 'I was served well', 'Buyondo Hardware')
        self.weconnect.create_review(
            'janedoe', 'Good', 'I was served well', 'Bondo')

        self.assertEqual("User did not create the review!", self.weconnect.delete_review(
            'janedoe', 'Bondo'))
