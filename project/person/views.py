from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import PersonSerializer, PersonUpdateSerializer, PersonDeleteSerializer, PersonListSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Person, ReadOnlyDB, UnconfirmedTransaction, PersonToDelete
from rest_framework.generics import get_object_or_404
from django.db.models import Q
import base64
from PIL import Image
import io
from io import BytesIO
from django.core.files import File
import json


class UpdateDataViewSet(viewsets.ViewSet):
    @action(methods=['get'], detail=False, permission_classes=[AllowAny], url_path='pull')
    def pull_updates(self, request):
        db = get_object_or_404(ReadOnlyDB, key=request.query_params.get('key', None))
        data_to_add = Person.objects.exclude(id__in=db.person.all().values('id'))

        data_to_delete = PersonToDelete.objects.exclude(Q(primary_id__in=db.person_to_delete.all().values('id')) & ~Q(primary_id__in=db.person.all().values('id')))

        transaction, created = UnconfirmedTransaction.objects.get_or_create(db=db)
        for person in transaction.person_to_add.all():
            transaction.person_to_add.remove(person)
        for person in transaction.person_to_delete.all():
            transaction.person_to_delete.remove(person)

        for person in data_to_add:
            transaction.person_to_add.add(person)

        for person in data_to_delete:
            transaction.person_to_delete.add(person)

        transaction.save()

        data = PersonListSerializer(data_to_add, many=True).data
        return HttpResponse(json.dumps({"add": data,
                            "delete": PersonDeleteSerializer(data_to_delete, many=True).data}))

    @action(methods=['post'], detail=False, permission_classes=[AllowAny], url_path='push')
    def push_updates(self, request):
        response = list()
        for val in request.data.get('data', []):
            try:
                token = val['local_id']
                primary_id = val.get('primary_id', None)
                from django.core.files.base import ContentFile

                if primary_id is not None and Person.objects.filter(id=primary_id).exists():
                    person = Person.objects.get(id=primary_id)
                    serializer = PersonUpdateSerializer(person, data=val, partial=True)
                    serializer.is_valid(raise_exception=True)
                    person = serializer.save()

                    for db in person.db.all():
                        person.db.remove(db)

                    for transaction in person.transaction.all():
                        transaction.person.remove(person)
                    person.save()
                else:
                    serializer = PersonSerializer(data=val)
                    serializer.is_valid(raise_exception=True)
                    person = serializer.save()

                image = Image.open(io.BytesIO(base64.b64decode(val['image'].encode('utf-8'))))
                blob = BytesIO()
                image.save(blob, image.format.lower())
                person.image.save(f'{person.first_name}_{person.last_name}.{image.format.lower()}', File(blob),
                                  save=True)

                person_data = PersonSerializer(person).data
                person_data['local_id'] = token
                response.append(person_data)
            except:
                pass

        return Response(response)

    @action(methods=['post'], detail=False, permission_classes=[AllowAny], url_path='confirm-pull')
    def confirm_pull(self, request):
        db = get_object_or_404(ReadOnlyDB, key=request.data.get('key', None))
        added_items = request.data.get('data_added', [])
        deleted_items = request.data.get('data_deleted', [])

        transaction = get_object_or_404(UnconfirmedTransaction, db=db)
        for person_id in added_items:
            if transaction.person_to_add.filter(id=person_id).exists():
                try:
                    person = Person.objects.get(id=person_id)
                    db.person.add(person)
                except Person.DoesNotExist:
                    pass

        for person_id in deleted_items:
            if transaction.person_to_delete.filter(primary_id=person_id).exists():
                try:
                    person = PersonToDelete.objects.get(primary_id=person_id)
                    db.person_to_delete.add(person)
                except PersonToDelete.DoesNotExist:
                    pass
        db.save()
        transaction.delete()
        return Response(status=200)
