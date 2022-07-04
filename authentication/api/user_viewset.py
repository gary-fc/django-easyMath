from django.contrib.auth.hashers import make_password
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import User
from game.models import UserLevelArea


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'school', 'score')


def enable_area_and_basic_level(user) -> bool:
    try:
        UserLevelArea(user_id=user['id'], area_id=1, level_id=1).save()
        UserLevelArea(user_id=user['id'], area_id=2, level_id=11).save()
        return True
    except:
        User.objects.get(id=user['id']).delete()
        return False


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) \
            if enable_area_and_basic_level(serializer.data) \
            else Response('error', status=status.HTTP_409_CONFLICT, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserCustomSerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UserCustomSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='get_score' , permission_classes=[IsAuthenticated])
    def get_score(self, request):
        user = User.objects.filter(id=request.user.id).first()
        return Response({'score': user.score, 'total_score': user.total_score})
