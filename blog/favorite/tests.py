import json
import django

django.setup()
from favorite.models import Favorite
from post.models import Post
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase


# Create your tests here.

class FavoriteCreateListTestCase(APITestCase):
    url = reverse("favorite:list-create")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "selcuk5655"
        self.password = "Microman1903"
        self.post = Post.objects.create(title="Başlık 1111", content="İçerik 11111")
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
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

    def test_add_favorite(self):
        """
            Kullanıcının bir gönderiyi favorilere ekleyip eklemediğini test eder.
        """
        data = {
            "content": "içerik güzelll",
            "user": self.user.id,
            "post": self.post.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_favs(self):
        """
            Kullanıcının favori gönderilerini listeleyip listelemediğini test eder.
        """
        self.test_add_favorite()
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)) ==
                        Favorite.objects.filter(user=self.user).count())


class FavoriteUpdateDeleteTest(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "selcuk111111"
        self.password = "Microman1903"
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.user2 = User.objects.create_user(username="selcuk2",
                                              password=self.password)
        self.post = Post.objects.create(title="Başlık", content="İçerik")
        self.favorite = Favorite.objects.create(content="içeriği çok güzel olan bir post",
                                                post=self.post,
                                                user=self.user)
        self.url = reverse("favorite:rud",
                           kwargs={"pk": self.favorite.pk})
        self.test_jwt_authentication("selcuk111111")

    def test_jwt_authentication(self, username="selcuk111111"):
        """
            Kullanıcının JWT token ile başarılı bir şekilde login olmasını sağlar ve
            login olduğunu doğrular
        """
        response = self.client.post(self.url_login,
                                    data={"username": username,
                                          "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_fav_delete(self):
        """
            Kullanıcının kendi favori gönderisini silip silemediğini test eder
        """
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)

    def test_fav_delete_different_user(self):
        """
            Farklı bir kullanıcının başka bir kullanıcıya ait favori gönderiyi silmeye çalışması
            durumunda yetkisizlik (403) hatası alıp almadığını test eder.
        """
        self.test_jwt_authentication("selcuk2")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_fav_update(self):
        """
            Kullanıcının kendi favorisini günceleyip güncelleyemediğini test eder.
        """
        data = {
            "content": "içerik güzelll 999999",
            "post": self.post.id,
            "user": self.user.id
        }
        response = self.client.put(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(Favorite.objects.get(id=self.favorite.id).content == data["content"])

    def test_fav_update_different_user(self):
        """
            Farklı bir kullanıcının başka bir kullanıcıya ait favori gönderiyi güncelleyip
            güncelleyemediğini (yetkisizlik - 403) test eder
        """
        self.test_jwt_authentication("selcuk2")
        data = {
            "content": "içerik güzelll 6666666",
            "post": self.post.id,
            "user": self.user2.id
        }
        response = self.client.put(self.url, data)
        self.assertTrue(403, response.status_code)

    def test_unauthorized(self):
        """
            Giriş yapmamış kullanıcının favorinin detayını göremediğini test ediyoruz.
        """
        self.client.credentials()  # Bu şekilde oturum sonlandırılmış olur.
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
