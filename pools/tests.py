from django.http import response
from django.test import TestCase, testcases
from django.urls.base import reverse
from django.utils import timezone
import datetime
from .models import Question

# Create your tests here.


def create_question(question_text, days):
    """ Function to create question with any number of days"""
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    return question

class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_date(self):
        future_time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=future_time)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_old_date(self):
        old_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=old_time)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_date(self):
        recent_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=recent_time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """ If no question exists, display a message """
        response = self.client.get(reverse('pools_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No pools available')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """ Question in the past, display it on the index page """
        question = create_question(question_test='This question is in the past', days=-1)
        response = self.client.get(reverse('pools_index'))
        self.assertQuerySetEqual(response.context['lastest_question_list'], [question])

    def test_future_question(self):
        """ If future question exists, don't display a message """
        question = create_question(question_test='This question is in the future', days=1)
        response = self.client.get(reverse('pools_index'))
        self.assertQuerySetEqual(response.context['lastest_question_list'], [])

    def test_future_and_past_question(self):
        """ If both future and past questions exist, display only past question"""
        question = create_question(question_test='This question is in the past', days=-1)
        create_question(question_text='This is a future question')
        response = self.client.get(reverse('pools_index'))
        self.assertQuerySetEqual(response.context['lastest_question_list'], [question])

    def test_two_past_questions(self):
        """ If two past questions exists, display them all on the index page """
        question1 = create_question(question_test='This first question is in the past', days=-1)
        question2 = create_question(question_test='This second question is in the past', days=-1)
        response = self.client.get(reverse('pools_index'))
        self.assertQuerySetEqual(response.context['lastest_question_list'], [question1, question2])
        

class QuestionDetailViewTests(TestCase):
    def test_past_question(self):
        """ If past question, display it."""
        past_question = create_question(question_text='Past question', days=-2)
        url = reverse('pools_detai', args=past_question.id)
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        """If future question, assert 404"""
        future_question = create_question(question_text='Future question', days=2)
        url = reverse('pools_detail', args=future_question.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)