from django.urls import reverse
from django.db import models


class List(models.Model):
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('view_list', args=[self.pk])


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE, related_name='items')
    objects = models.Manager()
