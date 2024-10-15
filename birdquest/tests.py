from birdquest.models import BirdsFound, UsersBirdCollection
from django.test import TestCase
from django.urls import reverse
from unittest.mock import MagicMock, patch
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

import io

class SubmitBirdTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        self.uploaded_image = InMemoryUploadedFile(
            io.BytesIO(b"fake_image_data"),
            'image',
            'test_image.jpg',
            'image/jpeg',
            len(b"fake_image_data"),
            None
        )

    @patch('birdquest.views.BirdsFound.objects.get_or_create')
    @patch('birdquest.views.UsersBirdCollection.objects.get_or_create')
    def test_submit_bird(self, mock_collection_get_or_create, mock_bird_get_or_create):
        mock_bird = MagicMock()
        mock_bird.bird_name = "029.American_Crow"
        mock_bird.found_count = 1
        mock_bird_get_or_create.return_value = (mock_bird, True)

        mock_collection = MagicMock()
        mock_collection.total_birds_found = 1
        mock_collection_get_or_create.return_value = (mock_collection, True)

        response = self.client.post(reverse('submit_bird'), {
            'bird_name': '029.American_Crow',
            'image': self.uploaded_image
        })

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'status': 'success', 'bird_name': '029.American_Crow', 'found_count': 1}
        )
class LeaderboardIntegrationTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')

        UsersBirdCollection.objects.create(user=self.user1, total_birds_found=5)
        UsersBirdCollection.objects.create(user=self.user2, total_birds_found=10)

    def test_leaderboard_data_display(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1')
        self.assertContains(response, '5')
        self.assertContains(response, 'user2')
        self.assertContains(response, '10')