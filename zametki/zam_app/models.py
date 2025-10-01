from django.db import models

class Note(models.Model): #Делаем модель для БД заметок
    title_n = models.CharField(max_length=200, verbose_name='Заголовок')
    content_n = models.TextField(verbose_name='Содержание')
