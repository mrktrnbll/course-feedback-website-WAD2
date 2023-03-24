from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from course_feedback.models import Course, Review
from course_feedback.forms import RegisterForm, RegisterProfileForm, AddCourse, AddReview


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('course_feedback:index')
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_index_view_with_no_courses(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['courses'], [])

    def test_index_view_with_courses(self):
        course = Course.objects.create(
            name='Test Course',
            code='TST123',
            description='Test course description',
            lecturer=self.user.profile,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['courses'], [repr(course)])

    def test_index_view_add_course(self):
        data = {
            'name': 'New Course',
            'code': 'NEW123',
            'description': 'New course description',
            'picture': '',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        self.assertEqual(Course.objects.count(), 1)
        course = Course.objects.first()
        self.assertEqual(course.name, 'New Course')
        self.assertEqual(course.code, 'NEW123')
        self.assertEqual(course.description, 'New course description')
        self.assertEqual(course.lecturer, self.user.profile)
