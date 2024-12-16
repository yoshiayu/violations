from django.shortcuts import render,redirect
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Violations, ViolationSelection, Result
from .serializers import User_serializer, ViolationsSerializer, ViolationSelectionSerializer, ResultSerializer
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"アカウント {username} が作成されました！ログインしてください。")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def index(request):
    violations = Violations.objects.filter(age_group__in=[1, 3])  # デフォルトは成人 + 共通項目
    return render(request, 'violations/index.html', {
        'violations': violations,
        'range': range(1, 6),  # 1から5までの選択肢
    })
def calculate(request):
    if request.method == 'POST':
        age_group = request.POST.get('age_group')
        violation_ids = request.POST.getlist('violations')
        violation_ids = [int(v_id) for v_id in violation_ids if v_id]

        violations = Violations.objects.filter(id__in=violation_ids)
        if not violations:
            return JsonResponse({"error": "違反が選択されていません。"}, status=400)

        total_points = sum(v.points for v in violations)
        total_fine = sum(v.fine_min for v in violations)
        max_punishment = max((v.punishment for v in violations), key=len, default="なし")

        result = {
            "age_group": "成人" if age_group == "adult" else "未成年",
            "violations": [{"name": v.name, "points": v.points, "fine": v.fine_min, "punishment": v.punishment} for v in violations],
            "total_points": total_points,
            "total_fine": total_fine,
            "possible_punishment": max_punishment,
            "license_status": "取消" if total_points >= 15 else "停止" if total_points >= 6 else "影響なし"
        }
        return JsonResponse(result)

@api_view(['GET'])
def get_violations(request):
    age_group = request.GET.get('age_group', 'adult')  # デフォルトは"adult"（成人）
    
    if age_group == 'adult':
        age_group_filter = [1, 3]  # 成人 + 共通
    elif age_group == 'minor':
        age_group_filter = [2, 3]  # 未成年 + 共通
    else:
        return JsonResponse({"error": "Invalid age group"}, status=400)
    
    violations = Violations.objects.filter(age_group__in=age_group_filter)
    return JsonResponse(list(violations.values()), safe=False)

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
    
