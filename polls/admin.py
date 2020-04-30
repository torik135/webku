from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 3

  fieldsets = [
      ('Pilihan', {'fields': ['choice_text']}),
  ]


class QuestionAdmin(admin.ModelAdmin):
  fieldsets = [
      ('Question',
       {'fields': ['question_title', 'question_text']}),
      ('Info tanggal',
       {'fields': ['pub_date']}),
  ]
  inlines = [ChoiceInline]
  list_display = (
      'question_title',
      'question_text',
      'pub_date',
      'pub_terakhir',
  )
  list_filter = ['pub_date']
  search_fields = ['question_title']


admin.site.register(Question, QuestionAdmin)
