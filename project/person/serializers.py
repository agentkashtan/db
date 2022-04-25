from rest_framework import serializers
from .models import Person, PersonToDelete


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'phone', 'image',)


class PersonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'phone', 'image',)


class PersonDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonToDelete
        fields = ('primary_id',)
