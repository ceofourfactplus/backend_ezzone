from django.urls import path
from . import views

urlpatterns = [
    path('raw-material/', views.RawMaterialListAPIView().as_view()),
    path('raw-material/<int:pk>', views.GetRM().as_view()),
    path('edit-rm/<int:pk>', views.EditRM().as_view()),
    path('rm-img/<int:pk>', views.UpdateRmImg().as_view()),
    path('price-raw-material/', views.PriceRawMaterialAPIView().as_view()),
    path('pickup-raw-material/', views.PickupPriceRM().as_view()),
    path('rm-po/notice', views.PONotice.as_view()),
    path('rm-update/', views.RMAPIView().as_view()),
    path('pickup/', views.PickupAPIView.as_view()),
    path('get-nearly-sold-out/', views.PONotice.as_view()),
    path('get_unit/<int:pk>', views.UnitDetailAPIView.as_view()),
    # path('edit/', views.RMAPIView().as_view()),
    path('category/', views.CategoryAPIView.as_view()),
    path('category/<int:pk>', views.RMCategoryDetailAPIView.as_view()),
    path('receipt/', views.ReceiptRawMaterial.as_view()),
    path('receipt-detail/', views.ReceiptRawMaterialDetail.as_view()),
    path('unit/', views.UnitListAPIView.as_view()),
    path('unit/<int:pk>', views.UnitDetailAPIView.as_view()),
    path('query_category/<int:pk>', views.FilCategoryRaw.as_view()),
    path('supplier/', views.SupplierListAPIView.as_view()),
    path('supplier/<int:pk>', views.SupplierDetailAPIView.as_view()),
    path('po/cal-add',views.CalPO.as_view()),                
    path('po/',views.POList.as_view()),
    path('po/update/',views.POList.as_view()),
    path('po/calc/',views.CalcPOAvg.as_view()),
    path('check-phone-number/<str:phone_number>',views.CheckPhoneNumber.as_view()),
    path('check-phone-number/<str:phone_number>/<int:pk>', views.CheckPhoneNumberEdit.as_view())
]