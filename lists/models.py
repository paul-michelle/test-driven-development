from django.db import models


class List(models.Model):
    objects = models.Manager()


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE, related_name='items')
    objects = models.Manager()
