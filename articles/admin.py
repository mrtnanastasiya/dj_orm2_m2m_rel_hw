from django.contrib import admin

from .models import Article, Tag, ArticleTag
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

# инлайн для отношения многие-ко-многим между таблицами Article и Tag
# он позволит удобно редактировать статьи в админке, позволит добавлять к ним теги
# автоматически обновляя таблицу ArticleTag


class ArticleTagInlineFormset(BaseInlineFormSet):
    def clean(self):
        # Создаем счетчик того, сколько основных разделов было указано
        is_main_counter = 0
        # Проходимся по формам и если что обновляем счетчик
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            print(form.cleaned_data)
            # Если в форме было указано, что раздел основной, прибавляем 1
            if form.cleaned_data['is_main'] == True:
                is_main_counter += 1
            # Если счетчик превысил 1, выбрасываем ошибку
            if is_main_counter > 1:
                raise ValidationError('Было указано больше 1 основного раздела')

            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
            # raise ValidationError('Тут всегда ошибка')
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


