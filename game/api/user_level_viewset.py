from rest_framework import serializers, viewsets

from game.models import UserLevel


class UserLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLevel
        fields = '__all__'


class UserLevelViewset(viewsets.ModelViewSet):
    queryset = UserLevel.objects.all()
    serializer_class = UserLevelSerializer
