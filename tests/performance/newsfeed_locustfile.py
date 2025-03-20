from locust import HttpUser, task


class LocustUser(HttpUser):

    def get_token(self, username):
        response = self.client.post("/api/user/login",
                                    json={"username": username,
                                          "password": "password"})
        if response.status_code == 200:
            return response.json().get("token").get("access")
        else:
            print(f"로그인 실패: {response.text}, {response.status_code}")

    @task(1)
    def get_newsfeed(self):
        token = self.get_token(username='user_2')
        headers = {
            f"Authorization": f"Bearer {token}"
        }
        response = self.client.get("/api/posts/newsfeed", headers=headers)

        if response.status_code == 200:
            print(f"정상 응답: {response.json()}")
        else:
            print(f"API 호출 실패: {response.status_code}, {response.text}")

    @task(1)
    def post_newsfeed(self):
        token = self.get_token(username='user_1')
        headers = {
            "Authorization": f"Bearer {token}"
        }
        data = {
            'text': 'locust 테스트를 위한 글 작성',
            'images': ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg'],
        }
        response = self.client.post("/api/posts/", headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"정상 응답: {result}")
            post_id = result.get("id")
            data = {
                "urls": [
                    'https://flab-sns-bucket.s3.amazonaws.com/test_url/image_1.jpg',
                    'https://flab-sns-bucket.s3.amazonaws.com/test_url/image_2.jpg',
                    'https://flab-sns-bucket.s3.amazonaws.com/test_url/image_3.jpg',
                    'https://flab-sns-bucket.s3.amazonaws.com/test_url/image_4.jpg',
                    'https://flab-sns-bucket.s3.amazonaws.com/test_url/image_5.jpg',
                ]
            }
            img_response = self.client.post(f"/api/posts/newsfeed/images/{post_id}", headers=headers, data=data)
            if img_response.status_code == 200:
                print(f"정상 응답: {img_response.json()}")
            else:
                print(f"API 호출 실패: {img_response.status_code}, {img_response.text}")
        else:
            print(f"API 호출 실패: {response.status_code}, {response.text}")
