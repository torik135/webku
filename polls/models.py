import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_title = models.CharField(max_length=200)
    question_text = models.TextField()
    pub_date = models.DateTimeField('tgl_pub')

    def __str__(self):
        return self.question_title

    def pub_terakhir(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    pub_terakhir.admin_order_field = 'pub_date'
    pub_terakhir.boolean = True
    pub_terakhir.short_description = 'pub terakhir ?.'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
