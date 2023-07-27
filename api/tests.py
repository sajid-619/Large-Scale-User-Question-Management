import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from faker import Faker
from .models import User, Question, FavoriteQuestion, ReadQuestion

class QuestionManagementTests(TestCase):
    def setUp(self):
        # Create test data for users and questions using Faker library
        fake = Faker()

        # Create 10 million users
        for _ in range(10000000):
            User.objects.create(
                idname=fake.unique.name(),
                display_name=fake.name(),
                email=fake.unique.email(),
                phone=fake.unique.phone_number()
            )

        # Create 1 million questions
        for _ in range(1000000):
            Question.objects.create(
                question=fake.sentence(),
                option1=fake.word(),
                option2=fake.word(),
                option3=fake.word(),
                option4=fake.word(),
                option5=fake.word(),
                answer=fake.random_int(min=1, max=5),
                explain=fake.paragraph()
            )

        # Convert the querysets to lists
        users = list(User.objects.all())
        questions = list(Question.objects.all())

        # Create some favorite and read questions for users
        for user in users:
            favorite_questions = fake.random_elements(elements=questions, length=5, unique=True)
            for question in favorite_questions:
                FavoriteQuestion.objects.create(user_id=user, question_id=question)

            read_questions = fake.random_elements(elements=questions, length=5, unique=True)
            for question in read_questions:
                ReadQuestion.objects.create(user_id=user, question_id=question)

    def test_count_favorite_read_questions(self):
        # Write test cases to check if the count_favorite_read_questions API works as expected
        user_id = 1  # Assuming there is a user with ID 1
        response = self.client.get(reverse('count_favorite_read_questions', kwargs={'user_id': user_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse the JSON response
        data = json.loads(response.content)

        # Check if the 'favorite_count' and 'read_count' keys exist in the response data
        self.assertIn('favorite_count', data)
        self.assertIn('read_count', data)

    def test_filter_questions(self):
    # Write test cases to check if the filter_questions API works as expected
        # Test 'read' status
        response = self.client.get(reverse('filter_questions', kwargs={'status': 'read'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse the JSON response
        data = json.loads(response.content)

        # Print the response data to debug
        print(data)

        # Check if the 'results' key exists in the response data (Paginated response)
        self.assertIn('results', data)

        # Access the 'questions' key from the paginated 'results'
        questions = data['results']

        # Now you can assert your specific test conditions based on the 'questions' list
        # In this case, let's check if the questions list is not empty
        self.assertTrue(len(questions) > 0, f"No questions found for 'read' status. Response data: {data}")

        # Test 'unread' status
        response = self.client.get(reverse('filter_questions', kwargs={'status': 'unread'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        questions = data['results']

        # Print the response data to debug
        print("Unread Status Response:")
        print(data)

        # Now you can assert your specific test conditions based on the 'questions' list
        # In this case, let's check if the questions list is not empty
        print(f"Number of questions for 'unread' status: {len(questions)}")
        self.assertTrue(len(questions) > 0)

        # Test 'favorite' status
        response = self.client.get(reverse('filter_questions', kwargs={'status': 'favorite'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        questions = data['results']

        # Print the response data to debug
        print("Favorite Status Response:")
        print(data)

        # Now you can assert your specific test conditions based on the 'questions' list
        # In this case, let's check if the questions list is not empty
        print(f"Number of questions for 'favorite' status: {len(questions)}")
        self.assertTrue(len(questions) > 0)

        # Test 'unfavorite' status
        response = self.client.get(reverse('filter_questions', kwargs={'status': 'unfavorite'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        questions = data['results']

        # Print the response data to debug
        print("Unfavorite Status Response:")
        print(data)

        # Now you can assert your specific test conditions based on the 'questions' list
        # In this case, let's check if the questions list is not empty
        print(f"Number of questions for 'unfavorite' status: {len(questions)}")
        self.assertTrue(len(questions) > 0)

        # Check if the questions in the response have the correct status ('unread')
        for question in questions:
            self.assertTrue('question' in question)
            self.assertTrue('option1' in question)
            self.assertTrue('option2' in question)
            # Add similar assertions for other fields in the question model

            # Assert that the question has the correct status ('unread')
            self.assertIn('status', question)
            self.assertEqual(question['status'], 'unread')


