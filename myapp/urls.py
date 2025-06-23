from django.urls import path
from .views import f_newrekap_stunting_vmp8, f_newrekap_stunting_dtl_vmp8, ong_stunting_dtl_regc, ong_stunting_v3_regc

urlpatterns = [
    path('newrekap-stunting', f_newrekap_stunting_vmp8, name='newrekap_stunting'),
    path('newrekap-stunting-dtl', f_newrekap_stunting_dtl_vmp8, name='newrekap_stunting_dtl'),
    path('stunting-dtl', ong_stunting_dtl_regc, name='stunting_dtl'),
    path('stunting-v3', ong_stunting_v3_regc, name='stunting_v3'),
]