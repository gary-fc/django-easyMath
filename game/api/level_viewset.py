import json

from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from game.models import Level, UserLevelArea


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializers = LevelSerializer

    @action(methods=['GET'], detail=False, url_path='get_levels_by_area')
    def get_area_by_id_pg(self, request):
        area_id = request.GET.get('area')
        f = open('game/fixtures/level_data.json')
        levels = json.load(f)
        f.close()
        levels = [level for level in levels if level['fields']['area'] == int(area_id)]
        return Response({'levels': levels})

    @action(methods=['GET'], detail=False, url_path='get_levels_enable_by_user_and_area', permission_classes=[IsAuthenticated])
    def get_levels_enable_by_user_and_area(self, request):
        area = request.GET.get('area')
        levels_by_user = [level['level_id'] for level in
                          UserLevelArea.objects.filter(user_id=request.user.id, area_id=area).values('level_id')]
        f = open('game/fixtures/level_data.json')
        levels = json.load(f)
        f.close()
        test = UserLevelArea.objects.filter(user_id=request.user.id, area_id=area).values('level_id')
        print(test)
        print(levels_by_user)
        levels = [level for level in levels if level['pk'] in levels_by_user]
        return Response({'levels': levels})
