from django.urls import re_path
from web.views import customer, payment, account

app_name = "web"
urlpatterns = [

    re_path(r'^customer/list/$', customer.customer_list, name="customer_list"),
    re_path(r'^customer/add/$', customer.customer_add, name="customer_add"),
    re_path(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit, name="customer_edit"),
    re_path(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del, name="customer_del"),
    re_path(r'^customer/import/$', customer.customer_import, name="customer_import"),
    re_path(r'^customer/tpl/$', customer.customer_tpl, name="customer_tpl"),

    re_path(r'^payment/list/$', payment.payment_list, name="payment_list"),
    re_path(r'^payment/add/$', payment.payment_add, name="payment_add"),
    re_path(r'^payment/edit/(?P<pid>\d+)/$', payment.payment_edit, name="payment_edit"),
    re_path(r'^payment/del/(?P<pid>\d+)/$', payment.payment_del, name="payment_del"),
    re_path(r'^login/$', account.login),
]
