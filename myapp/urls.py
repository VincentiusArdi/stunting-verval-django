from django.urls import path
from .views import ong_stunting_v3_bali, ong_stunting_v3_diy, ong_stunting_v3_jateng, ong_stunting_dtl_bali, f_newrekap_stunting_vmp8, f_newrekap_stunting_dtl_vmp8, ong_stunting_dtl_regc

urlpatterns = [
    path('stunting-baliv3', ong_stunting_v3_bali, name='stunting_baliv3'),
    path('stunting-diy3', ong_stunting_v3_diy, name='stunting_diy3'),
    path('stunting-jateng3', ong_stunting_v3_jateng, name='stunting_jateng3'),
    path('stunting-dtl-bali', ong_stunting_dtl_bali, name='stunting_dtl_bali'),
    path('newrekap-stunting-vmp8', f_newrekap_stunting_vmp8, name='newrekap_stunting_vmp8'),
    path('newrekap-stunting-dtl-vmp8', f_newrekap_stunting_dtl_vmp8, name='newrekap_stunting_dtl_vmp8'),
    path('stunting-dtl-regc', ong_stunting_dtl_regc, name='stunting_dtl_regc'),
]