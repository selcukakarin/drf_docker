import json
import django

django.setup()

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase


# Create your tests here.

# 1 - dogru verilerle kayıt işlemi
# 2 - username doğru şifre invalid olabilir
# 3 - kullanıcı adı kullanılmış olabilir.
# 4 - üye girişi yaptıksak register sayfası görünmemeli

class UserRegistrationTestCase(APITestCase):
    url = reverse("account:register")

    def test_user_registration(self):
        """
            dogru verilerle kayıt işlemi
        """
        data = {
            "username": "selcuktest1",
            "email": "selcuktest@gmail.com",
            "password": "deneme1SSS"
        }
        response = self.client.post(self.url, data)
        # 201 created
        self.assertEqual(201, response.status_code)

    def test_user_invalid_password(self):
        """
            invalid password ile kayıt
        """
        data = {
            "username": "gece1234gece",
            "email": "gece1234gece@gmail.com",
            "password": "1"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_unique_name(self):
        """
            benzersiz isim testi
        """
        self.test_user_registration()
        data = {
            "username": "selcuktest1",
            "email": "selcuktest@gmail.com",
            "password": "deneme1SSS"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_user_authenticated_registration(self):
        """
            session ile giriş yapmış kullanıcı sayfayı görememeli
        """
        self.test_user_registration()
        self.client.login(username="selcuktest1", password="deneme1SSS")
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)


class UserLoginTestCase(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "selcuk321321312312"
        self.password = "Microman1903"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_token(self):
        """
            Ben username ve password ile giriş yapacağım ve bana access token geliyor mu bunu
            kontrol edeceğim.
        """
        response = self.client.post(self.url_login, {"username": "selcuk321321312312", "password": "Microman1903"})
        self.assertEqual(200, response.status_code)
        print(json.loads(response.content))
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid(self):
        """
            veritabanında user tablosunda olmayan kullanıcı için giriş işleminin 401 status kodunun
            almasını denedik.
        """
        response = self.client.post(self.url_login, {"username": "selcuk99999", "password": "Microman1903"})
        self.assertEqual(401, response.status_code)

    def test_user_empty_data(self):
        response = self.client.post(self.url_login, {"username": "", "password": ""})
        self.assertEqual(400, response.status_code)


class UserPasswordChangeTestCase(APITestCase):
    url = reverse("account:change-password")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "selcuk7777"
        self.password = "Microman1903"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_with_token(self):
        data = {
            "username": "selcuk7777",
            "password": "Microman1903"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_is_authenticated(self):
        """
            giriş yapmamış tokensız kullanıcı isteği
        """
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_with_valid_information(self):
        """
            doğru bilgilerle düzgün bir şekilde şifresini değiştirme işlemi
        """
        self.test_login_with_token()
        data = {
            "old_password": "Microman1903",
            "new_password": "SelcukAkarin123"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(204, response.status_code)
