from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTest(TestCase):

  def tes_pub_future(self):
    time = timezone.now() + datetime.timedelta(days=30)
    future_q = Question(pub_date=time)
    self.assertIs(future_q.pub_terakhir(), False)

  def tes_pub_old(self):
    time = timezone.now() - datetime.timedelta(days=1, second=1)
    old_q = Question(pub_date=time)
    self.assertIs(old_q.pub_terakhir(), False)

  def tes_pub_recent(self):
    time = timezone.now() - datetime.timedelta(hours=23, second=1)
    recent_q = Question(pub_date=time)
    self.assertIs(recent_q.pub_terakhir(), False)


def create_question(question_title, days):
  time = timezone.now() + datetime.timeddelta(days=days)
  return Question.objects.create(question_title=question_title, pub_date=time)


class QuestionIndexViewTests(TestCase):

  def tes_no_q(self):
    resp = self.client.get(reverse('polls:index'))
    self.assertEqual(resp.status_code, 200)
    self.assertContains(resp, 'tidak ada polls')
    self.assertQueryEqual(resp.context['q_terakhir'], [])

  def tes_past_q(self):
    create_question(question_title='PAST Q.', days=30)
    resp = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
        resp.context['q_terakhir'],
        ['<Question: PAST Q.>']
    )

  def tes_future_q(self):
    create_question(question_title='FUTURE Q.', days=30)
    resp = self.client.get(reverse('polls:index'))
    self.assertContains(resp, 'tidak ada polls')
    self.assertQueryEqual(resp.context['q_terakhir'], [])

  def tes_future_and_past_q(self):
    create_question(question_title='PAST Q.', days=30)
    create_question(question_title='FUTURE Q.', days=30)
    resp = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
        resp.context['q_terakhir'],
        ['<Question: PAST Q.>']
    )

  def tes_dua_past_q(self):
    create_question(question_title='PAST Q 1.', days=30)
    create_question(question_title='PAST Q 2.', days=30)
    resp = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
        resp.context['q_terakhir'],
        ['<Question: PAST Q 2.', '<Question: PAST Q 1.']
    )


class QuestionDetailViewTests(TestCase):
  def tes_future_q(self):
    future_q = create_question(question_title='FUTURE Q.', days=5)
    url = reverse('polls:detail', args=(future_q.id,))
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 404)

  def tes_past_q(self):
    past_q = create_question(question_title='PAST Q.', days=5)
    url = reverse('polls:detail', args=(future_q.id,))
    resp = self.client.get(url)
    self.assertContains(resp, past_q.question_title)
