import django

django.setup()
from django.test import TestCase
from django.contrib.auth.models import User
import json
from rest_framework.test import APITestCase
from django.urls import reverse
from post.models import Post


# Create your tests here.

class PostCreateListTestCase(APITestCase):
    url_create = reverse("post:create")
    url_list = reverse("post:post")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "pikachu"
        self.password = "pika123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        """
            Kullanıcının JWT token ile başarılı bir şekilde login olmasını sağlar ve
            login olduğunu doğrular
        """
        response = self.client.post(self.url_login,
                                    data={"username": self.username,
                                          "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_add_new_post(self):
        """
        Oturum açmış bir kullanıcının yeni bir gönderi ( post ) oluşuturabilmesini test eder.
        Post başarıyla oluşuturulmuşsa 201 Created statusu döner.
        """
        data = {
            "content": "pokemon içerik",
            "title": "pokemon başlık"
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(201, response.status_code)

    def test_add_new_post_unauthorization(self):
        """
        Oturum açmamış bir kullanıcının yeni bir post oluşturma denemesini test eder.
        Yetkisiz erişim denemesi 401 Unauthorized hatası döndürmelidir.
        """
        self.client.credentials()  # oturumu kapat
        data = {
            "content": "pokemon içerik",
            "title": "pokemon başlık"
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(401, response.status_code)

    def test_posts(self):
        """
        Mevcut gönderilerin listelenmesini test eder.
        Önce bir gönderi eklenir ve ardından gönderilerin sayısının veritabanındaki gerçek gönderi
        sayısı ile eşleştiği doğrulanır.
        """
        self.test_add_new_post()
        response = self.client.get(self.url_list)
        self.assertEqual(200, response.status_code)
        self.assertTrue(json.loads(response.content)["count"] == Post.objects.filter(draft=False).count())
