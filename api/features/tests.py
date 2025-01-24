from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.features.models import Post, Follow
from api.user.models import User


class PosTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user_1 = User.objects.create_user(
            username="test",
            email="test@test.com",
            password="password"
        )
        cls.user_2 = User.objects.create_user(
            username="test2",
            email="test2@test.com",
            password="password"
        )
        cls.url = f'/api/posts'

        for i in range(5):
            Post.objects.create(
                user=cls.user_2,
                text=f'test {i+1}'
            )

        Follow.objects.create(
            follower=cls.user_1,
            followee=cls.user_2
        )

    def setUp(self):
        self.newsfeed_data = {
            'text': 'newsfeed test',
            'images': [
                'image1.jpeg',
                'image2.jpeg',
                'image3.png',
                'image4.jpg',
                'video.MOV'
            ]
        }

        # 로그인
        login_data = {
            'username': 'test',
            'password': 'password'
        }

        login_response = self.client.post('/api/user/login', login_data, format='json')
        self.assertEqual(login_response.status_code, 200)

        access_token = login_response.data['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.client.defaults['HTTP_CONTENT_TYPE'] = 'application/json'

    def test_create_post(self):
        response = self.client.post(
            self.url,
            data=self.newsfeed_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post_id = response.data.get('id')
        urls = response.data.get('urls')
        self.assertIsNotNone(urls, "Presigned URL 리스트가 응답에 포함되어 있지 않습니다.")
        self.assertIsNotNone(post_id, "post_id가 응답에 포함되어 있지 않습니다.")

        required_params = ['X-Amz-Algorithm', 'X-Amz-Credential', 'X-Amz-Signature']

        for idx, url in enumerate(urls):
            with self.subTest(url=url):
                # 1. URL 형식 확인
                self.assertTrue(url.startswith('https://'), f"{url}이 유효하지 않습니다.")

                # 2. 필수 쿼리 매개변수 확인
                for param in required_params:
                    self.assertIn(param, url, f"Presigned URL[{idx}]에 {param} 쿼리 매개변수가 없습니다.")

    def test_get_newsfeed(self):
        url = f'{self.url}/newsfeed'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data.get('results')), 5)
