app_name = ""

from django.urls import path
from .views import *

vendor_urlpatterns = [
    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('vendors/New', VendorCreateView.as_view(), name='vendor_create'),
    path('vendor/<int:pk>/', VendorDetailView.as_view(), name='vendor_detail'),
    path('vendor/update/<int:pk>/', VendorUpdateView.as_view(), name='vendor_update'),
]


loan_urlpatterns = [
    path('loans/', LoanListView.as_view(), name='loan_list'),
    path('loan/create/', create_loan, name='create_loan'),
    path('loan/<int:pk>/', LoanDetailView.as_view(), name='loan_detail'),
]

payment_urlpatterns = [
    path('payments/<int:loan_id>/make_payment/', make_payment, name='make_payment'),
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payment/<int:loan_id>/make/', make_payment, name='make_payment'),
    path('payment/detail/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
]

product_urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
]

Supplier_urlpatterns = [
        path('supplier/create/', SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('supplier/<int:pk>/', SupplierDetailView.as_view(), name='supplier_detail'),

]

loan_repayment_schedule_urlpatterns = [
    # path('loan_repayment_schedule/create/', LoanRepaymentScheduleCreateView.as_view(), name='loan_repayment_schedule_create'),
    path('loan_repayment_schedules/', LoanRepaymentScheduleListView.as_view(), name='loan_repayment_schedule_list'),
    path('loan_repayment_schedule/<int:pk>/', LoanRepaymentScheduleDetailView.as_view(), name='loan_repayment_schedule_detail'),





    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

urlpatterns = vendor_urlpatterns + loan_urlpatterns + payment_urlpatterns + product_urlpatterns + Supplier_urlpatterns+loan_repayment_schedule_urlpatterns


from django.urls import path
from .views import admin_dashboard

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
] + urlpatterns


from django.urls import path
from .views import vendor_dashboard

urlpatterns = [
    path('vendor/dashboard/', vendor_dashboard, name='vendor_dashboard'),
] + urlpatterns

