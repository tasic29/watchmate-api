from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='example', password='newpassword')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name='Netflix',
                                                           about='something about',
                                                           website='https://netflix.com')

    def test_streamplatform_create(self):
        data = {
            'name': 'Netflix',
            'about': 'info about platform',
            'website': 'https://netflix.com'
        }
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(
            reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='example', password='newpassword')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name='Netflix',
                                                           about='something about',
                                                           website='https://netflix.com')
        self.watchlist = models.WatchList.objects.create(platform=self.stream,
                                                         title='Example',
                                                         storyline='Example story',
                                                         active=True)

    def test_watchlist_create(self):
        data = {
            'platform': self.stream,
            'title': 'Example Movie',
            'storyline': 'Example Stroy',
            'active': True
        }

        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(
            reverse('streamplatform-detail', args=[self.watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'Example')


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='example', password='newpassword')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name='Netflix',
                                                           about='something about',
                                                           website='https://netflix.com')
        self.watchlist = models.WatchList.objects.create(platform=self.stream,
                                                         title='Example Movie',
                                                         storyline='Example story',
                                                         active=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream,
                                                          title='Example Movie',
                                                          storyline='Example story',
                                                          active=True)
        self.review = models.Review.objects.create(review_user=self.user,
                                                   rating=5,
                                                   description='Great Movie',
                                                   watchlist=self.watchlist2,
                                                   active=True)

    # def test_review_create(self):
    #     data = {
    #         'review_user': self.user,
    #         'rating': 5,
    #         'description': 'Great Movie',
    #         'watchlist': self.watchlist,
    #         'active': True
    #     }

    #     response = self.client.post(
    #         reverse('review-create', args=(self.watchlist.id,)), data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     response = self.client.post(
    #         reverse('review-create', args=(self.watchlist.id,)), data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unath(self):
        data = {
            'review_user': self.user,
            'rating': 5,
            'description': 'Great Movie',
            'watchlist': self.watchlist,
            'active': True
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            'review_user': self.user,
            'rating': 4,
            'description': 'Great Movie! - Updated',
            'watchlist': self.watchlist,
            'active': False
        }
        response = self.client.put(
            reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(
            reverse('review-list', args=[self.watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(
            reverse('review-detail', args=[self.review.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get(
            '/watch.reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
