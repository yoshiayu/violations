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
        age_group = request.POST.get('age_group')
        violation_ids = request.POST.getlist('violations')  # 違反リストを取得

        if not age_group or not violation_ids:
            return Response({"error": "年齢区分または違反内容が選択されていません。"}, status=400)

        # 違反の最大数を5つに制限
        if len(violation_ids) > 5:
            return Response({"error": "違反は最大5つまで選択できます。"}, status=400)

        # データベースから違反情報を取得
        violations = Violations.objects.filter(id__in=violation_ids)
        if not violations.exists():
            return Response({"error": "指定された違反が存在しません。"}, status=404)

        # 合計罰金と点数を計算
        total_fine = sum(violation.fine_min for violation in violations)
        total_points = sum(violation.points for violation in violations)

        # 最も厳しい刑罰を特定
        possible_punishment = max(
            (violation.punishment for violation in violations), key=len, default="なし"
        )

        # 各違反内容をリスト化
        violations_details = [
            {
                "name": violation.name,
                "points": violation.points,
                "fine": violation.fine_min,
                "punishment": violation.punishment
            }
            for violation in violations
        ]

        # 結果を構築
        result = {
            "age_group": "成人" if age_group == "adult" else "未成年",
            "violations": violations_details,
            "total_fine": total_fine,
            "total_points": total_points,
            "possible_punishment": possible_punishment
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
    
