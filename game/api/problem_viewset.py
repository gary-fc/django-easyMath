import json

from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import User
from game.models import Problem, UserLevelArea


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


def builderNumbers(numberOne, numberTwo):
    return str(numberOne) + ',' + str(numberTwo)


def isSuccess(numbers, result, problem):
    return (numbers == problem['fields']['numbers'] and result == problem['fields']['result']) if True else False


class ProblemViewset(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    @action(methods=['GET'], detail=False, url_path='get_problems_by_level',
            permission_classes=[IsAuthenticated])
    def get_problems_by_level(self, request):
        level_id = request.GET.get('level')
        f = open('game/fixtures/problem_data.json')
        problems = json.load(f)
        f.close()
        problems = [problem for problem in problems if problem['fields']['level'] == int(level_id)]
        return Response(problems)

    @action(methods=['POST'], detail=False, url_path='get_success_problems_by_level_and_user',
            permission_classes=[IsAuthenticated])
    def get_success_problems_by_level_and_user(self, request):
        level_id = request.GET.get('level')
        answers = request.data.get('answers')
        answers = sorted(answers, key=lambda d: d['pk'])
        f = open('game/fixtures/problem_data.json')
        problems = json.load(f)
        f.close()
        problems = [problem for problem in problems if problem['fields']['level'] == int(level_id)]

        result = [answers for (problem, answers) in zip(problems, answers) if
                  isSuccess(builderNumbers(answers['numberOne'], answers['numberTwo']), answers['total'],
                            problem)]
        result = sorted(result, key=lambda d: d['pk'])
        area_id = None
        print(answers)
        print(problems)
        print(result)
        if len(result) > 0:

            if result[0]["pk"] < 31:
                area_id = 1
            elif result[0]["pk"] < 61:
                area_id = 2
            elif result[0]["pk"] < 91:
                area_id = 3
            elif result[0]["pk"] < 121:
                area_id = 4
            elif result[0]["pk"] < 151:
                area_id = 5
        print(result)
        if area_id is not None:
            user_level_area = UserLevelArea.objects.filter(user_id=request.user.id, level_id=int(level_id) + 1, area_id=area_id).first()
            enable_new_area = UserLevelArea.objects.filter(user_id=request.user.id, area_id=area_id)
            if area_id == 1 and len(enable_new_area) > 6:
                UserLevelArea.objects.update_or_create(user_id=request.user.id, area_id=3, level_id=21)
            if area_id == 2 and len(enable_new_area) > 6:
                UserLevelArea.objects.update_or_create(user_id=request.user.id, area_id=4, level_id=31)
            mult = UserLevelArea.objects.filter(user_id=request.user.id, area_id=3)
            div = UserLevelArea.objects.filter(user_id=request.user.id, area_id=4)

            if len(mult) > 6 and len(div) > 6:
                UserLevelArea.objects.update_or_create(user_id=request.user.id, area_id=5, level_id=41)

            if user_level_area is None:
                UserLevelArea.objects.create(user_id=request.user.id, level_id=int(level_id) + 1, area_id=area_id).save()
                user = User.objects.filter(id=request.user.id).first()
                user.total_score = user.total_score + len(answers)
                user.score = user.score + len(answers)
                user.save()
                return Response(result)
        return Response(result)
