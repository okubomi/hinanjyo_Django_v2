# main_app/urls.py
from django.urls import path
from . import views

app_name = 'main_app' # アプリの名前空間を設定

urlpatterns = [
    # 空のパス（http://127.0.0.1:8000/）にアクセスしたときに
    # views.py の shelter_search_view を実行する
    path('', views.shelter_search_view, name='shelter_search'),
]