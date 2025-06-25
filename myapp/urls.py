from django.urls import path
from .views import f_newrekap_stunting_vmp8, f_newrekap_stunting_dtl_vmp8, ong_stunting_dtl_regc, ong_stunting_v3_regc, ong_stunting_genting_allreg, ong_stunting_genting_ringkasan_allreg, f_newrekap_stunting_ringkasan_all, ong_stunting_ringkasan_v3_allreg

urlpatterns = [
    path('newrekap-stunting', f_newrekap_stunting_vmp8, name='newrekap_stunting'),
    path('newrekap-stunting-dtl', f_newrekap_stunting_dtl_vmp8, name='newrekap_stunting_dtl'),
    path('newrekap-stunting-ringkasan', f_newrekap_stunting_ringkasan_all, name='newrekap_stunting_ringkasan'),
    path('stunting-dtl', ong_stunting_dtl_regc, name='stunting_dtl'),
    path('stunting-v3', ong_stunting_v3_regc, name='stunting_v3'),
    path('stunting-genting', ong_stunting_genting_allreg, name='stunting_genting_allreg'),
    path('stunting-genting-ringkasan', ong_stunting_genting_ringkasan_allreg, name='stunting_genting_ringkasan_allreg'),
    path('stunting-ringkasan', ong_stunting_ringkasan_v3_allreg, name='stunting_ringkasan_v3_allreg'),
]