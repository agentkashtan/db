from rest_framework import serializers
from .models import Person, PersonToDelete
import os
import base64


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'phone',)


class PersonListSerializer(serializers.ModelSerializer):
    image_file = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'phone', 'image_file',)

    def get_image_file(self, obj):
        script_dir = os.path.dirname(__file__)[:-6]
        with open(os.path.join(script_dir, str(obj.image)), "rb") as f:
            im_bytes = f.read()
        return base64.b64encode(im_bytes).decode("utf8")


class PersonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'phone', 'image',)


class PersonDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonToDelete
        fields = ('primary_id',)
