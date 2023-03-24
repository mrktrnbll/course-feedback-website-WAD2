from django.db import models
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from course_feedback.models import Course, Review, Profile
from course_feedback.forms import RegisterForm, RegisterProfileForm, AddCourse, AddReview
from django.core.files.uploadedfile import SimpleUploadedFile

image_path = 'course_feedback/test_files/test_image.png'

class TestIndexView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('course_feedback:index')
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, is_lecturer=True)
        self.client.login(username='testuser', password='testpassword')

    def test_index_view_with_no_courses(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['courses'], [])

    def test_index_view_with_courses(self):
        course = Course.objects.create(
            name='Test Course',
            courseID='TST123',
            lecturer=self.user.profile,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['courses'], [repr(course)])

    def test_index_view_add_course(self):
        newPhoto = models.ImageField()
        newPhoto.image = SimpleUploadedFile(name='test_image.png', content=open(image_path, 'rb').read(), content_type='image/png')
        data = {
            'courseID': 'NEW123',
            'name': 'New Course',
            'picture': newPhoto.image,
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.url)
        course = Course.objects.first()
        self.assertEqual(course.name, 'New Course')
        self.assertEqual(course.courseID, 'NEW123')
        self.assertEqual(course.lecturer, self.user.profile)

        self.assertEqual(Course.objects.count(), 1)

class TestShowCourseView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com"
        )
        self.profile = Profile.objects.create(user=self.user, is_lecturer=True)
        self.course = Course.objects.create(
            name='Test Course',
            courseID='TST123',
            lecturer=self.user.profile,
        )
        self.review = Review.objects.create(
            content="This is a test review",
            course=self.course,
            student=self.user.profile
        )
        self.url = reverse("course_feedback:show_course", args=[self.course.slug])

    def test_show_course_view_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "course_feedback/course.html")

    def test_show_course_view_POST(self):
        self.client.login(username="testuser", password="testpass")
        form_data = {
            "content": "This is a new test review"
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.course.review_set.count(), 2)

class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('course_feedback:login')
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.profile = Profile.objects.create(user=self.user, is_lecturer=True)
    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_feedback/login.html')

    def test_valid_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, reverse('course_feedback:index')) # check for redirect
        self.assertTrue(response.wsgi_request.user.is_authenticated) # check for user authentication

    def test_invalid_login(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_feedback/login.html')

class UserLogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('course_feedback:logout')
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.profile = Profile.objects.create(user=self.user, is_lecturer=True)

    def test_user_logout(self):
        self.client.login(username='testuser', password='testpass') # login the user
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('course_feedback:index')) # check for redirect
        self.assertFalse(response.wsgi_request.user.is_authenticated) # check for user logout

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('course_feedback:register')

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_feedback/register.html')

    def test_valid_lecturer_registration(self):
        data = {
            'username': 'testlecturer',
            'password': 'testpass',
            'email': 'testlecturer@example.com',
            'is_lecturer': True
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, reverse('course_feedback:login')) # check for redirect
        self.assertEqual(User.objects.count(), 1) # check if user was created
        user = User.objects.first()
        self.assertEqual(user.username, 'testlecturer')
        self.assertEqual(user.email, 'testlecturer@example.com')
        self.assertTrue(user.check_password('testpass'))
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.is_lecturer, True)

    def test_invalid_registration(self):
        data = {
            'username': '',
            'email': '',
            'password': '',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_feedback/register.html')
        self.assertEqual(User.objects.count(), 0) # check if user was not created

class AccountViewTestCase(TestCase):
    def setUp(self):
        self.student_user = User.objects.create_user(
            username='student',
            password='testpass',
            email='student@example.com',
        )
        self.student_profile = Profile.objects.create(user=self.student_user, is_lecturer=False)
        self.lecturer_user = User.objects.create_user(
            username='lecturer',
            password='testpass',
            email='lecturer@example.com',
        )
        self.lecturer_profile = Profile.objects.create(user=self.lecturer_user, is_lecturer=True)
        self.course1 = Course.objects.create(
            name='Test Course 1',
            courseID='TC1',
            lecturer=self.lecturer_profile,
        )
        self.course2 = Course.objects.create(
            name='Test Course 2',
            courseID='TC2',
            lecturer=self.lecturer_profile,
        )
        self.review1 = Review.objects.create(
            course=self.course1,
            student=self.student_profile,
            content='Test Comment 1',
            upvotes=3,
        )
        self.review2 = Review.objects.create(
            course=self.course2,
            student=self.student_profile,
            content='Test Comment 2',
            upvotes=4,
        )

    def test_account_view_with_student(self):
        self.client.login(username='student', password='testpass')
        response = self.client.get(reverse('course_feedback:account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_feedback/account.html')
        self.assertEqual(len(response.context['reviews']), 2)
        self.assertEqual(len(response.context['createdCourses']), 0)
        self.client.logout()

    def test_account_view_with_lecturer(self):
        self.client.login(username='lecturer', password='testpass')
        response = self.client.get(reverse('course_feedback:account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_feedback/account.html')
        self.assertEqual(len(response.context['reviews']), 0)
        self.assertEqual(len(response.context['createdCourses']), 2)
        self.client.logout()

    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()
        Course.objects.all().delete()
        Review.objects.all().delete()
