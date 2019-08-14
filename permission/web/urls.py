from django.conf.urls import url
from web.views import customer
from web.views import payment
app_name = "web"
urlpatterns = [

    url(r'^customer/list/$', customer.customer_list, name="customer_list"),
    url(r'^customer/add/$', customer.customer_add, name="customer_add"),
    url(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit, name="customer_edit"),
    url(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del, name="customer_del"),
    url(r'^customer/import/$', customer.customer_import, name="customer_import"),
    url(r'^customer/tpl/$', customer.customer_tpl, name="customer_tpl"),

    url(r'^payment/list/$', payment.payment_list, name="payment_list"),
    url(r'^payment/add/$', payment.payment_add, name="payment_add"),
    url(r'^payment/edit/(?P<pid>\d+)/$', payment.payment_edit, name="payment_edit"),
    url(r'^payment/del/(?P<pid>\d+)/$', payment.payment_del, name="payment_del"),

]
