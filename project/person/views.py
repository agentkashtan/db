from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import PersonSerializer, PersonUpdateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Person, ReadOnlyDB, UnconfirmedTransaction
from rest_framework.generics import get_object_or_404


class UpdateDataViewSet(viewsets.ViewSet):
    @action(methods=['get'], detail=False, permission_classes=[AllowAny], url_path='pull')
    def pull_updates(self, request):
        db = get_object_or_404(ReadOnlyDB, key=request.query_params.get('key', None))
        data = Person.objects.exclude(id__in=db.person.all().values('id'))
        transaction, created = UnconfirmedTransaction.objects.get_or_create(db=db)
        for person in transaction.person.all():
            transaction.person.remove(person)
        for person in data:
            transaction.person.add(person)
        transaction.save()
        return Response(PersonSerializer(data, many=True).data)

    @action(methods=['post'], detail=False, permission_classes=[AllowAny], url_path='push')
    def push_updates(self, request):
        response = list()
        for val in request.data.get('data', []):
            try:
                token = val['local_id']
                primary_id = val.get('primary_id', None)
                if primary_id is not None and Person.objects.filter(id=primary_id).exists():
                    person = Person.objects.get(id=primary_id)
                    serializer = PersonUpdateSerializer(person, data=val, partial=True)
                    serializer.is_valid(raise_exception=True)
                    person_data = PersonSerializer(serializer.save()).data
                    for db in person.db.all():
                        person.db.remove(db)

                    for transaction in person.transaction.all():
                        transaction.person.remove(person)
                    person.save()
                else:
                    serializer = PersonSerializer(data=val)
                    serializer.is_valid(raise_exception=True)
                    person_data = PersonSerializer(serializer.save()).data
                person_data['local_id'] = token
                response.append(person_data)
            except KeyError:
                pass

        return Response(response)

    @action(methods=['post'], detail=False, permission_classes=[AllowAny], url_path='confirm-pull')
    def confirm_pull(self, request):
        db = get_object_or_404(ReadOnlyDB, key=request.data.get('key', None))
        items = request.data.get('data', [])
        transaction = get_object_or_404(UnconfirmedTransaction, db=db)
        for person_id in items:

            if transaction.person.filter(id=person_id).exists():
                try:
                    person = Person.objects.get(id=person_id)
                    db.person.add(person)
                except Person.DoesNotExist:
                    pass
        db.save()
        transaction.delete()
        return Response(status=200)
