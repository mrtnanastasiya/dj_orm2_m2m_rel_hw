from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name

class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    # поле tags будет перечислять все записи из таблицы Tag,
    # связанные с какой-то статьей, а тоо как они связаны будет задано в таблице ArticleTag
    tags = models.ManyToManyField(Tag, through='ArticleTag')
    # Если мы хотим получить не список тегов для какой-то статьи,
    # а более обширные сведения из таблицы ArticleTag, например,
    # свойство is_main (является ли этот тег основным для статьи),
    # то мы должны использовать не article.tags, а article.articletag_set.all()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

# Вместо того, чтобы позволить джанго придумать и создать кросс-таблицу
# мы прописали ее вручную
class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    is_main = models.BooleanField(verbose_name='Основной раздел?')

    class Meta:
        verbose_name = 'Раздел для статьи'
        verbose_name_plural = 'Разделы для статьи'