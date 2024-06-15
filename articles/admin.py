from django.contrib import admin

from .models import Article, Tag, ArticleTag
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

class ArticleTagInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_counter = 0
        for form in self.forms:
            print(form.cleaned_data)
            if form.cleaned_data['is_main'] == True:
                is_main_counter += 1
            if is_main_counter > 1:
                raise ValidationError('Было указано больше 1 основного раздела')

        return super().clean()  # вызываем базовый код переопределяемого метода

class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    formset = ArticleTagInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at', 'image']
    inlines = [ArticleTagInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


