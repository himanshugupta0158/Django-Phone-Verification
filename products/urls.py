from django.urls import path
from .views import (ProductAPIView , CustomerRecordAPIView)


urlpatterns = [
        path("", ProductAPIView.as_view(), name="products"),
        path('<int:id>/',ProductAPIView.as_view()),
        path("puchase_record/", CustomerRecordAPIView.as_view(), name="puchase_record"),
]
