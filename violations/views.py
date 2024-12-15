from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Violations, ViolationSelection, Result
from .serializers import User_serializer, ViolationsSerializer, ViolationSelectionSerializer, ResultSerializer

def index(request):
    violations = Violations.objects.all()
    return render(request, 'violations/index.html', {'violations': violations})

@api_view(['POST'])
def calculate(request):
    try:
        # POSTリクエストのデータを取得
        age_group = request.data.get('age_group')
        violation_ids = request.data.getlist('violations')

        if not age_group or not violation_ids:
            return Response({"error": "年齢区分または違反内容が選択されていません。"}, status=400)

        # データベースから違反情報を取得
        violations = Violations.objects.filter(id__in=violation_ids)
        if not violations.exists():
            return Response({"error": "指定された違反が存在しません。"}, status=404)

        # 合計罰金と点数の計算
        total_fine = sum(violation.fine_min for violation in violations)
        total_points = sum(violation.points for violation in violations)

        # 結果の作成
        result = {
            "age_group": age_group,
            "violations": [
                {
                    "name": violation.name,
                    "points": violation.points,
                    "fine": violation.fine_min
                }
                for violation in violations
            ],
            "total_fine": total_fine,
            "total_points": total_points
        }

        return Response(result, status=200)

    except Exception as e:
        return Response({"error": f"サーバーエラーが発生しました: {str(e)}"}, status=500)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = User_serializer

class ViolationsViewSet(viewsets.ModelViewSet):
    queryset = Violations.objects.all()
    serializer_class = ViolationsSerializer

class ViolationSelectionViewSet(viewsets.ModelViewSet):
    queryset = ViolationSelection.objects.all()
    serializer_class = ViolationSelectionSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    
