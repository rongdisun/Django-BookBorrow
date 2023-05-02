import uuid
from pathlib import Path

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):

    def create_superuser(self, userid, username, password, **kwargs):
        kwargs['is_superuser'] = True
        user = self.model(userid=userid,
                          username=username,
                          **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    userid = models.CharField(verbose_name="账号", max_length=20, primary_key=True)
    username = models.CharField(verbose_name="用户名", max_length=20, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    # 如果使用username登录则改成username即可
    USERNAME_FIELD = "userid"

    REQUIRED_FIELDS = ["username", "is_staff"]


def user_avatar_path(instance, avatar_name):
    ext = avatar_name.split('.')[-1]
    avatar_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return Path("avatar", avatar_name)


class UserProfile(models.Model):
    sex_choice = (
        (0, "男"),
        (1, "女")
    )
    user = models.OneToOneField(to=User, verbose_name="用户", on_delete=models.CASCADE, related_name="user_profile")
    avatar = models.FileField(verbose_name="头像", upload_to=user_avatar_path)
    sex = models.SmallIntegerField(verbose_name="性别", choices=sex_choice)
    address = models.CharField(verbose_name="住址", max_length=20)
    email = models.EmailField(verbose_name="邮箱", max_length=30)
    telephone = models.CharField(verbose_name="手机号", max_length=11)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name



