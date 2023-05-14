from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Vote
from django.test import Client


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()

    def test_home_view_unauth(self):
        response = self.client.get(reverse('poll-home'))
        self.assertRedirects(response, '/login/?next=/home/', status_code=302, target_status_code=200)
        self.assertFalse(Vote.objects.get(user=self.user).has_voted)

    def test_home_view_auth_not_voted(self):
        self.client.login(username='testuser', password='testpass')
        self.assertFalse(Vote.objects.get(user=self.user).has_voted)
        response = self.client.get(reverse('poll-home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_POST(self):
        self.client.login(username='testuser', password='testpass')
        self.assertFalse(Vote.objects.get(user=self.user).has_voted)
        form = {'sub': 'red'}
        response = self.client.post(reverse('poll-home'), form)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/results/', status_code=302, target_status_code=200)
        self.assertTrue(Vote.objects.get(user=self.user).has_voted)
        self.assertTrue(Vote.objects.get(user=self.user).choice)

    def test_home_view_auth_voted(self):
        self.client.login(username='testuser', password='testpass')
        vote = Vote.objects.get(user=self.user)
        vote.has_voted = True
        vote.save()
        self.assertTrue(Vote.objects.get(user=self.user).has_voted)
        response = self.client.get(reverse('poll-home'))
        self.assertRedirects(response, '/?next=/home/', status_code=302, target_status_code=200)


class RegisterViewTestCase(TestCase):
    def test_register_view(self):
        form = {
            'username': 'testuser2',
            'password1': 'testpass2',
            'password2': 'testpass2'
        }
        response = self.client.post(reverse('register'), form)
        user = User.objects.get(username = 'testuser2')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser2').exists())
        self.assertTrue(Vote.objects.filter(user=user).exists())


class ResultsviewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser3', password='testpass3')

    def test_results_view_unath(self):
        response = self.client.get(reverse('results'))
        self.assertRedirects(response, '/login/?next=/results/', status_code=302, target_status_code=200)

    def test_results_view_auth_unvoted(self):
        self.client.login(username='testuser3', password='testpass3')
        self.assertFalse(Vote.objects.get(user=self.user).has_voted)
        response = self.client.get(reverse('results'))
        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, '/home/?next=/results/', status_code=302, target_status_code=200)

    def test_results_view_auth_voted(self):
        self.client.login(username='testuser3', password='testpass3')
        vote = Vote.objects.get(user=self.user)
        vote.has_voted = True
        vote.choice = True
        vote.save()
        response = self.client.get(reverse('results'))
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.context['result'], 100)


