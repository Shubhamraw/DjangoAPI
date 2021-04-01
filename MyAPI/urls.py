from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('MyAPI', views.ApprovalsView)
urlpatterns = [
    # path('form/', admin.site.urls),
    path('api/', include(router.urls)),
    path('status/', views.approvereject),
] 