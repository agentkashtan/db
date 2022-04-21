from django.contrib import admin
from .models import Person, ReadOnlyDB, UnconfirmedTransaction


class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ('first_name', 'last_name', 'phone',)
    fields = ('first_name', 'last_name', 'phone', 'image',)


class ReadOnlyDBAdmin(admin.ModelAdmin):
    model = ReadOnlyDB
    list_display = ('key', 'title',)
    fields = ('key', 'title', 'person',)


class UnconfirmedTransactionAdmin(admin.ModelAdmin):
    model = UnconfirmedTransaction
    list_display = ('id',)
    fields = ('db', 'person',)


admin.site.register(UnconfirmedTransaction, UnconfirmedTransactionAdmin)
admin.site.register(ReadOnlyDB, ReadOnlyDBAdmin)
admin.site.register(Person, PersonAdmin)

