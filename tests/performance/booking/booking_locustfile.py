import random

from locust import HttpUser, task


class LocustBookingUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None

    def get_token(self, username):
        response = self.client.post("/api/user/login",
                                    json={"username": username,
                                          "password": "password"})
        if response.status_code == 200:
            return response.json().get("token").get("access")
        else:
            print(f"로그인 실패: {response.text}, {response.status_code}")

    def get_event(self, headers):
        response = self.client.get("/api/events", headers=headers)
        if response.status_code == 200:
            result = response.json().get('results', [])
            if result:
                return result[3]
            return None
        else:
            print(f"이벤트 GET 실패: {response.text}, {response.status_code}")

    def get_tickets(self, event_id, headers):
        response = self.client.get(f"/api/events/{event_id}", headers=headers)
        if response.status_code == 200:
            result = response.json().get('tickets', [])
            if result:
                return result
            return None
        else:
            print(f"Ticket API 호출 실패: {response.status_code}, {response.text}")

    @task(1)
    def post_booking(self):
        user_id = random.randint(1, 10000)  # 랜덤 사용자 ID 생성
        token = self.get_token(username=f"user_{user_id}")

        headers = {
            "Authorization": f"Bearer {token}"
        }

        event = self.get_event(headers=headers)
        if event:
            event_id = event.get("id")

            tickets = self.get_tickets(event_id=event_id, headers=headers)

            if tickets:
                random_num = random.randint(1, 10)
                num = min(random_num, len(tickets))
                selected_tickets = random.sample(tickets, num)
                ticket_ids = [ticket["id"] for ticket in selected_tickets]

                # 티켓 예약 API 호출
                data = {
                    "tickets": ticket_ids,
                    "payment": "credit_card",
                }

                response = self.client.post("/api/bookings/", headers=headers, json=data)
                if response.status_code == 201:
                    print(f"정상 응답: {response.json()}")
                else:
                    print(f"API 호출 실패: {response.status_code}, {response.text}")
