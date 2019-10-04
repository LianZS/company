from django.db import models
from django.contrib.auth.models import User


# # Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    idcard = models.BigIntegerField(db_column="idcard", verbose_name="身份证")
    photo = models.ImageField(upload_to="user", null=True)  # 头像
