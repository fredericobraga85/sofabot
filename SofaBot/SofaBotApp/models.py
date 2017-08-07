from django.db import models
from django.utils.encoding import python_2_unicode_compatible

import datetime

from django.utils import timezone

@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

@python_2_unicode_compatible
class Exchange(models.Model):
    currency_pair = models.CharField(max_length=20)
    initial_btc = models.FloatField(default=0)
    isActive    = models.BooleanField(default=False)

    def __str__(self):
        return self.currency_pair



@python_2_unicode_compatible
class OrderState(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    statusCode = models.IntegerField(default=0)
    perGain = models.FloatField(default=0)
    actual_price = models.FloatField(default=0)
    buy_value = models.FloatField(default=0)
    sell_value = models.FloatField(default=0)
    current_btc = models.FloatField(default=0)
    current_coin = models.FloatField(default=0)
    piggy       = models.FloatField(default=0)
    state_date = models.DateTimeField('date state')

    def __str__(self):
        return str(self.statusCode)
