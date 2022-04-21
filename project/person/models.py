from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)


class ReadOnlyDB(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    key = models.CharField(max_length=200, blank=False, null=False, unique=True)
    person = models.ManyToManyField('Person', related_name='db', null=True, blank=True)


class UnconfirmedTransaction(models.Model):
    db = models.ForeignKey('ReadOnlyDB', related_name='transaction', null=False, blank=False, on_delete=models.CASCADE)
    person = models.ManyToManyField('Person', related_name='transaction', null=True, blank=True)
