import django

django.setup()
import json
from comment.models import Comment
from post.models import Post
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase


# Create your tests here.

class CommentCreateTestCase(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.url = reverse("comment:create")
        self.url_list = reverse("comment:list")
        self.username = "selcuk000"
        self.password = "Microman1903"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.post = Post.objects.create(title="deneme", content="içerik")
        self.parent_comment = Comment.objects.create(content="yeni yorum 1", user=self.user,
                                                     post=self.post)
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

    def test_create_comment(self):
        """
            Kullanıcının bir posta yorum yapıp yapamayacığını test eder.
        """
        data = {
            "content": "içerik güzelll 4444",
            "user": self.user.id,
            "post": self.post.id,
            "parent": ""
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_create_child_comment(self):
        """
            Kullanıcının mevcut bir yoruma yanıt olarak alt bir yorum (child comment) ekleyip
            ekleyemediğini test eder
        """
        data = {
            "content": "yeni yorum 1111",
            "user": self.user.id,
            "post": self.post.id,
            "parent": self.parent_comment.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_comment_list(self):
        """
            Belirli bir gönderiye (posta) ait tüm yorumların listelenip listelenmediğini test eder.
        """
        self.test_create_comment()
        response = self.client.get(self.url_list, {"q": self.post.id})
        self.assertTrue(response.data["count"] == Comment.objects.filter(post=self.post).count())


class CommentUpdateDeleteTestCase(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "selcuk000"
        self.password = "Microman1903"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="selcuk12345", password=self.password)
        self.post = Post.objects.create(title="deneme", content="içerik")
        self.comment = Comment.objects.create(content="içerik1", user=self.user, post=self.post)
        self.url = reverse("comment:update", kwargs={'pk': self.comment.pk})
        self.url_delete = reverse("comment:delete", kwargs={'pk': self.comment.pk})
        self.test_jwt_authentication()

    def test_jwt_authentication(self, username="selcuk000", password="Microman1903"):
        """
            Kullanıcının JWT token ile başarılı bir şekilde login olmasını sağlar ve
            login olduğunu doğrular
        """
        response = self.client.post(self.url_login,
                                    data={"username": username,
                                          "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_delete_comment(self):
        """
        Kullanıcının kendi yorumunu başarılı bir şekilde silip
        silemediğini test eder. Silme işlemi başarılı olduğunda
        yorum veritabanından tamamen kaldırılır.
        """
        response = self.client.delete(self.url_delete)
        self.assertEqual(204, response.status_code)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_delete_other_user(self):
        """
        Bir kullanıcının başka bir kullanıcıya ait yorumu silip silemediğini test eder.
        Başarısız olursa (403 - Forbidden) hatası döner ve yorum silinmez.
        """
        self.test_jwt_authentication("selcuk12345")
        response = self.client.delete(self.url_delete)
        self.assertEqual(403, response.status_code)
        self.assertTrue(Comment.objects.get(pk=self.comment.pk))

    def test_update_comment(self):
        """
        Kullanıcının kendi yorumunu başarılı bir şekilde güncelleyip güncelleyemediğini test eder.
        Güncelleme işlemi başarılı olduğunda, yorumun içeriği değişir.
        """
        response = self.client.put(self.url, data={"content": "Elma kivi nane"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(Comment.objects.get(pk=self.comment.id).content, "Elma kivi nane")

    def test_update_comment_other_user(self):
        """
        Bir kullanıcının başka bir kullanıcıya ait yorumu güncelleyip güncelleyemeyeciğini test eder.
        Başarısız olursa 403 ( Forbidden ) hatası döner ve yorumun içeriği değişmez.
        """
        self.test_jwt_authentication("selcuk12345")
        response = self.client.put(self.url, data={"content": "Elma kivi nane"})
        self.assertEqual(403, response.status_code)
        self.assertNotEqual(Comment.objects.get(pk=self.comment.id), "Elma kivi nane")

    def test_unathorization(self):
        """
        Oturum açmamış bir kullanıcının yorum güncelleme URL'ine erişip erişemeyeceğini test eder.
        Yetkisiz erişim denemesi 401 Unauthorized hatası döndürür
        """
        self.client.credentials()  # oturumu kapatıyor.
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
