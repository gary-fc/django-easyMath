from django.urls import re_path, include
from rest_framework import routers

from game.api import LevelViewset, AreaViewset, ProblemViewset

router = routers.DefaultRouter()
router.register(r'level', LevelViewset)
router.register(r'area', AreaViewset)
router.register(r'problem', ProblemViewset)

urlpatterns = [
    re_path(r'^', include(router.urls)),
]