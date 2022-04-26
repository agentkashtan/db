from django.db import models


class PersonToDelete(models.Model):
    primary_id = models.IntegerField(null=False, blank=False)


class Person(models.Model):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            for db in self.db.all():
                self.db.remove(db)
        return super(Person, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        PersonToDelete.objects.get_or_create(primary_id=self.id)
        return super(Person, self).delete()


class ReadOnlyDB(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    key = models.CharField(max_length=200, blank=False, null=False, unique=True)
    person = models.ManyToManyField('Person', related_name='db', null=True, blank=True)
    person_to_delete = models.ManyToManyField('PersonToDelete', related_name='db', null=True, blank=True)


class UnconfirmedTransaction(models.Model):
    db = models.ForeignKey('ReadOnlyDB', related_name='transaction', null=False, blank=False, on_delete=models.CASCADE)
    person_to_add = models.ManyToManyField('Person', related_name='transaction_add', null=True, blank=True)
    person_to_delete = models.ManyToManyField('PersonToDelete', related_name='transaction_delete', null=True, blank=True)


