from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate
from django.test import TestCase

from ..models import User, Course, CClass, Schedule, ClassRoom, School
from utils.time import add_timezone


class UserModelTests(TestCase):
    """本包内Model单元测试"""

    def setUp(self):
        pass

    def test_course(self, name='C语言'):
        c = Course.objects.create(name=name)
        self.assertEqual(c.name, name)
        return c

    def test_cclass(self):
        c = self.test_course()
        cclass_a = c.cclass_set.create(name='A班')
        cclass_b = CClass.objects.create(
            name='B班',
            course=c
        )

        self.assertEqual(cclass_a.name, 'A班')
        self.assertEqual(cclass_a.course, cclass_b.course)

    def test_classroom(self, name='某教室'):
        classroom = ClassRoom.objects.create(name=name)
        self.assertTrue(classroom.name, name)
        return classroom

    def test_school(self, name='铁岭小学'):
        school = School.objects.create(name=name)
        self.assertEqual(school.name, name)
        return school

    def test_schedule(self):
        c = self.test_course()
        classroom = self.test_classroom()
        cclass = c.cclass_set.create(name='A班')
        self.assertEqual(c, cclass.course)
        schedule = cclass.schedule_set.create(
            classroom=classroom,
            time_check_in=add_timezone(datetime(year=2018, month=10, day=1, hour=10, minute=10)),
            time_start=add_timezone(datetime(year=2018, month=10, day=1, hour=10, minute=10)),
            time_finish=add_timezone(datetime(year=2018, month=10, day=1, hour=10, minute=10)),
        )
        self.assertEqual(schedule.time_check_in.tzinfo.zone, settings.TIME_ZONE)
        self.assertEqual(schedule.time_check_in.hour, 10)
        self.assertEqual(schedule.classroom, classroom)

    def test_user(self):
        User.objects.create_user(phone_number='13300001111', username='A', password='q123q123')
        u = User.objects.filter(phone_number='13300001111').first()
        self.assertTrue(u.check_password('q123q123'))
        self.assertFalse(u.check_password('q123q1231'))
        self.assertFalse(u.is_superuser)

        u = User.objects.create_superuser(phone_number='13300002222', username='B', password='q123q123')
        self.assertTrue(u.is_superuser)
