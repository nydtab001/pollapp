from django.test import TestCase
from django.contrib.auth.models import User

from pollhome.models import Vote


class VoteModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')

    def test_vote_creation(self):
        self.assertIsInstance(self.user.vote, Vote)
        self.assertEqual(str(self.user.vote), f"{self.user.username} has voted")
        self.assertFalse(self.user.vote.has_voted)
        self.assertFalse(self.user.vote.choice)

    def test_create_user_profile_signal(self):
        user = User.objects.create_user(username='testuser2', password='testpass')
        self.assertTrue(Vote.objects.filter(user=user).exists())