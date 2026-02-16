"""
URL configuration for conf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # これが必要
import os
from django.conf import settings

# --- ここから関数定義 ---


def service_worker(request):
    # ファイルの絶対パスを作成
    # settings.BASE_DIR は manage.py がある場所。
    # その下の 'templates' フォルダの中の 'service-worker.js' を指定。
    path = os.path.join(settings.BASE_DIR, 'templates', 'service-worker.js')

    try:
        with open(path, 'rb') as f:
            # 確実に 'application/javascript' ラベルを付けて返す
            return HttpResponse(f.read(), content_type="application/javascript")
    except FileNotFoundError:
        # ファイルがない場合はエラーを出す（原因特定のため）
        return HttpResponse(f"Error: {path} にファイルが見つかりません", status=404)
# --- ここまで関数定義 ---


urlpatterns = [
    path("admin/", admin.site.urls),
    # main_app の urls.py を読み込む設定を追加
    path('', include('main_app.urls')),
    # --- service-worker.js の設定（ここを修正） ---
    # 登録命令。これで http://127.0.0.1:8000/service-worker.js が有効になります
    path('service-worker.js', service_worker),



]
