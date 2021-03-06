from django.urls import path

from .views import SingleInvoiceView, InvoicesView

urlpatterns = [
    path('', InvoicesView.as_view(), name='create'),
    path('<str:identifier>', SingleInvoiceView.as_view(),
         name='retrieve/update'),
]
