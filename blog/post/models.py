from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=120)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    created_date = models.DateTimeField(editable=False)
    modified_date = models.DateTimeField()
    slug = models.SlugField(unique=True, max_length=150, editable=False)
    image = models.ImageField(upload_to='post/', null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                    related_name='modified_by')

    def get_slug(self):
        # Cay Bardagı Seti
        # cay_bardagi_seti
        # site_adresi/cay-bardagi-seti
        # site_adresi/cay-bardagi-seti-1
        # site_adresi/cay-bardagi-seti-2
        # site_adresi/cay-bardagi-seti-3
        slug = slugify(self.title.replace("ı", "i"))
        unique = slug
        number = 1

        while Post.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        self.modified_date = timezone.now()
        self.slug = self.get_slug()
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]
