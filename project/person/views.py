from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import PersonSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Person, ReadOnlyDB
from rest_framework.generics import get_object_or_404


class UpdateDataViewSet(viewsets.ViewSet):
    @action(methods=['get'], detail=False, permission_classes=[AllowAny], url_path='pull')
    def pull_updates(self, request):
        db = get_object_or_404(ReadOnlyDB, key=request.query_params.get('key', None))
        data = Person.objects.exclude(id__in=db.person.all().values('id'))
        for person in data:
            db.person.add(person)
        db.save()
        return Response(PersonSerializer(data, many=True).data)

    @action(methods=['post'], detail=False, permission_classes=[AllowAny], url_path='push')
    def push_updates(self, request):
        response = list()
        print(request.data.get('data', []))
        for val in request.data.get('data', []):
            try:
                print(val)
                serializer = PersonSerializer(data=val)
                serializer.is_valid(raise_exception=True)
                token = val['local_id']
                person_data = PersonSerializer(serializer.save()).data
                person_data['local_id'] = token
                response.append(person_data)
            except KeyError:
                pass

        return Response(response)
