from django.contrib import admin
from .models import Person, ReadOnlyDB, UnconfirmedTransaction, PersonToDelete
from django.dispatch import receiver
from django.db.models.signals import pre_delete


class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ('first_name', 'last_name', 'phone',)
    fields = ('first_name', 'last_name', 'phone', 'image',)

    @receiver(pre_delete)
    def delete_repo(sender, instance, **kwargs):
        if sender == Person:
            PersonToDelete.objects.get_or_create(primary_id=instance.id)


class ReadOnlyDBAdmin(admin.ModelAdmin):
    model = ReadOnlyDB
    list_display = ('key', 'title',)
    fields = ('key', 'title', 'person', 'person_to_delete',)


class UnconfirmedTransactionAdmin(admin.ModelAdmin):
    model = UnconfirmedTransaction
    list_display = ('id',)
    fields = ('db', 'person_to_add', 'person_to_delete',)


class PersonToDeleteAdmin(admin.ModelAdmin):
    model = PersonToDelete
    list_display = ('primary_id',)
    fields = ('primary_id',)


admin.site.register(PersonToDelete, PersonToDeleteAdmin)
admin.site.register(UnconfirmedTransaction, UnconfirmedTransactionAdmin)
admin.site.register(ReadOnlyDB, ReadOnlyDBAdmin)
admin.site.register(Person, PersonAdmin)

