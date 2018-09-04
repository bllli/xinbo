from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

from model_utils.models import TimeStampedModel


class School(models.Model):
    name = models.CharField('学校名称', max_length=128)

    class Meta:
        verbose_name = '学校'
        verbose_name_plural = verbose_name


class ClassRoom(models.Model):
    name = models.CharField('教室名称', max_length=128)

    class Meta:
        verbose_name = '教室'
        verbose_name_plural = verbose_name


class Course(models.Model):
    name = models.CharField('班级名称', max_length=128)

    class Meta:
        verbose_name = '新博课程'
        verbose_name_plural = verbose_name


class CClass(TimeStampedModel):
    name = models.CharField('新博班级', max_length=128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='所属课程')

    class Meta:
        verbose_name = '新博班级'
        verbose_name_plural = verbose_name


class Schedule(TimeStampedModel):
    time_check_in = models.DateTimeField('签到开始时间')
    time_start = models.DateTimeField('课程开始时间')
    time_finish = models.DateTimeField('课程结束时间')
    cclass = models.ForeignKey(CClass, on_delete=models.CASCADE, verbose_name='所属班级')
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, verbose_name='占用教室')

    class Meta:
        verbose_name = '课次'
        verbose_name_plural = verbose_name


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone number')

        user = self.model(
            username=username,
            phone_number=phone_number,
            # email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            phone_number,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """用户模型定义"""
    phone_number = models.CharField(
        '手机号',
        max_length=16,
        unique=True,
        help_text='用户的手机号，11位数字不含区号',
        db_index=True,
    )

    username = models.CharField(
        '姓名',
        max_length=32,
        db_index=True,
    )

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        verbose_name='所属学校',
        null=True, blank=True,
    )

    email = None  # 不要邮箱

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'phone_number'

    objects = UserManager()  # 使用自定义的用户管理器

    class Meta(AbstractUser.Meta):
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ('id',)

    def __str__(self):
        return f'{self.username}'
