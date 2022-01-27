from django.urls import path
from . import views

urlpatterns = [
    path('point/', views.PointPromotionAPI().as_view()),
    path('point-pos/', views.PointPOS().as_view()),
    path('point/<int:pk>', views.Point().as_view()),

    path('voucher/', views.VoucherAPI().as_view()),
    path('voucher/<int:pk>', views.VoucherGET().as_view()),
    path('package/', views.PackageAPI().as_view()),
    path('package-image/<int:pk>', views.PackageImage().as_view()),
    path('package/', views.PackageAPI().as_view()),
    path('package/<int:pk>', views.PackageDetailAPI().as_view()),
    path('package-pos/<int:pk>', views.getPackagePOS().as_view()),
    path('package-by-sale-channel/<int:pk>', views.PackageBySaleChannel().as_view()),
    path('reward/', views.RewardAPI().as_view()),
    path('reward/<int:pk>', views.RewardGET().as_view()),
    path('condition-reward/', views.ConditionRewardAPI().as_view()),
    path('condition-reward/<int:pk>', views.ConditionRewardGET().as_view()),
    path('customer-point/', views.CustomerPointAPI().as_view()),
    path('customer-point/<int:pk>', views.CustomerPointGET().as_view()),
    path('exchange-history/', views.ExchangeHistoryAPI().as_view()),
    path('exchange-history/<int:pk>', views.ExchangeHistoryGET().as_view()),
    path('dbs/', views.DBS().as_view()),
]