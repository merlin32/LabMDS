from django.test import TestCase, Client
from .models import Category, Course


class CourseViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Mathematics')
        self.course = Course.objects.create(
            title='Linear Algebra',
            instructor='Georgescu Ana',
            year=2026,
            semester='fall',
            category=self.category,
        )

    def test_list_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Linear Algebra')

    def test_detail_view(self):
        response = self.client.get(f'/{self.course.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Georgescu Ana')

    def test_detail_404(self):
        response = self.client.get('/9999/')
        self.assertEqual(response.status_code, 404)

    def test_create_requires_login(self):
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 302)

    def test_api(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data[0]['title'], 'Linear Algebra')
