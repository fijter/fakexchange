from django.contrib import admin
from django.urls import path
from . import views
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('dashboard/', user_views.DashboardView.as_view(), name='dashboard'),
    path('deposit/', views.DepositView.as_view(), name='deposit'),
    path('deposit/<symbol>/', views.DepositAddressView.as_view(), name='deposit-address'),
    path('withdraw/', views.WithdrawView.as_view(), name='withdraw'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('', views.HomepageView.as_view(), name='homepage'),
]

