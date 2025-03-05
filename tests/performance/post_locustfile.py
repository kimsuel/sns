from locust import HttpUser, task


class LocustUser(HttpUser):
    token = None

    def on_start(self):
        response = self.client.post("/api/user/login",
                                    json={"username": "slkim",
                                          "password": "password"})
        if response.status_code == 200:
            self.token = response.json().get("token").get("access")
        else:
            print("로그인 실패:", response.text)
    @task(1)
    def get_newsfeed(self):
        if not self.token:
            print("토큰 없음, 테스트 중지")
            return
        headers = {
            "Authorization": "Bearer " + self.token
        }
        response = self.client.get("/api/posts/newsfeed", headers=headers)

        if response.status_code == 200:
            print(f"정상 응답: {response.json()}")
        else:
            print(f"API 호출 실패: {response.status_code}, {response.text}")
