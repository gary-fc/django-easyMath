import json

from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from game.models import Area, UserLevelArea


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = '__all__'


class AreaViewset(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer



    @action(methods=['GET'], detail=False, url_path='get_area_by_id_pg')
    def get_area_by_id_pg(self, request):
        area_id = request.GET.get('area')
        f = open('game/fixtures/area_data.json')
        areas = json.load(f)
        f.close()
        area = [area for area in areas if area['pk'] == int(area_id)]
        return Response({'levels': area})

    @action(methods=['GET'], detail=False, url_path='get_areas_enable_by_user', permission_classes=[IsAuthenticated])
    def get_areas_enable_by_user(self, request):
        areas_by_user = [area['area_id'] for area in UserLevelArea.objects.filter(user_id=request.user.id).values('area_id')]
        f = open('game/fixtures/area_data.json')
        areas = json.load(f)
        f.close()
        areas = [area for area in areas if area['pk'] in areas_by_user]
        return Response({'areas': areas})