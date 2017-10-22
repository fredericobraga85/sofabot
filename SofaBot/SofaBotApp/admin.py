from django.contrib import admin

from .models import Question, Exchange, OrderState

admin.site.register(Question)
admin.site.register(Exchange)
admin.site.register(OrderState)