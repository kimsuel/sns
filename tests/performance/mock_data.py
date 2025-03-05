import requests

host = "http://localhost:8002"


class MockData:
    def __init__(self):
        # self.sign_up()
        self.follow()

    @staticmethod
    def sign_up():
        for i in range(6418, 10001):
            url = f'{host}/api/user/signup'
            data = {
                'username': f'user_{i}',
                'email': f'user_{i}@test.com',
                'password': 'password'
            }

            response = requests.post(url, json=data)

            if response.status_code == 201:
                print(f"데이터 : {data}")
            else:
                print(f"응답 오류 : {response.status_code}")

    @staticmethod
    def get_token(username: str):
        url = f'{host}/api/user/login'
        response = requests.post(url,
                                 json={"username": username,
                                       "password": "password"})
        if response.status_code == 200:
            return response.json().get("token").get("access")
        else:
            print("로그인 실패:", response.text)

    def follow(self):
        follower_token = self.get_token('user_1')
        url = f'{host}/api/follows/'
        for i in range(2, 10001):
            data_follower = {
                'follower_name': 'user_1',
                'followee_name': f'user_{i}',
            }
            response = requests.post(url, json=data_follower,
                                     headers={'Authorization': f'Bearer {follower_token}'})

            if response.status_code == 201:
                print(f"follower 데이터 : {data_follower}")
            else:
                print(f"follower 응답 오류 : {response.status_code}")

            data_followee = {
                'follower_name': f'user_{i + 1}',
                'followee_name': f'user_2',
            }
            followee_token = self.get_token(f'user_{i + 1}')

            response = requests.post(url, json=data_followee,
                                     headers={'Authorization': f'Bearer {followee_token}'})

            if response.status_code == 201:
                print(f"followee 데이터 : {data_followee}")
            else:
                print(f"followee 응답 오류 : {response.status_code}")


MockData()
