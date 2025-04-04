import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sns.settings")
django.setup()

from django.contrib.auth.hashers import make_password

from api.features.follow.models import Follow
from api.features.post.models import Post
from api.user.models import User


class MockData:
    def __init__(self):
        self.create_user()
        self.create_follow()
        self.create_newsfeeds()

    @staticmethod
    def create_user():
        users = [
            User(username=f"user_{i}",
                 email=f"user_{i}@example.com",
                 password=make_password("password"))
            for i in range(1, 10001)
        ]
        User.objects.bulk_create(users)

    @staticmethod
    def create_follow():
        users_exclude_user_1 = User.objects.exclude(username="user_1")
        users_exclude_user_2 = User.objects.exclude(username="user_2")
        users_exclude_user_3 = User.objects.exclude(username="user_3")
        user_1 = User.objects.get(username="user_1")
        user_2 = User.objects.get(username="user_2")
        user_3 = User.objects.get(username="user_3")

        for user in users_exclude_user_1:
            instance, created = Follow.objects.get_or_create(follower=user_1,
                                                             followee=user)
            if created:
                print(f"follower 데이터 : {instance}")

        for user in users_exclude_user_2:
            instance, created = Follow.objects.get_or_create(follower=user,
                                                             followee=user_2)
            if created:
                print(f"followee 데이터 : {instance}")

        count = 0
        for user in users_exclude_user_3:
            if count > 500:
                break

            instance, created = Follow.objects.get_or_create(follower=user_3,
                                                             followee=user)
            if created:
                print(f"follower 데이터 : {instance}")
                count += 1

        count = 0
        for user in users_exclude_user_3:
            if count > 500:
                break

            instance, created = Follow.objects.get_or_create(follower=user,
                                                             followee=user_3)

            if created:
                print(f"followee 데이터 : {instance}")
                count += 1

    @staticmethod
    def create_newsfeeds():
        users = User.objects.all()
        for user in users:
            for i in range(20):
                instance = Post.objects.create(user=user, text=f'테스트용 글 작성_{i}')
                for j in range(3):
                    instance.images.create(post=instance,
                                           url=f'https://flab-sns-bucket.s3.amazonaws.com/test_url/image_{j + 1}.jpg')
                print(f'user: {user.username}, post 생성 : {instance}')

MockData()
