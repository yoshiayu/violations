from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ViolationsViewSet, ViolationSelectionViewSet, ResultViewSet, get_violations
from . import views

# REST Framework のルーター設定
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'violations', ViolationsViewSet)
router.register(r'violation-selections', ViolationSelectionViewSet)
router.register(r'results', ResultViewSet)

# URLパターンの設定
urlpatterns = [
    path('api/', include(router.urls)),  # REST API用
    path('', views.index, name='index'),  # トップページ
    path('calculate/', views.calculate, name='calculate'),  # 計算ページ
    path('api/violations/', get_violations, name='get_violations'),
    path('get_violations/', views.get_violations, name='get_violations'),

]
