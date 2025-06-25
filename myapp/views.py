from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
import json
from .f_newrekap_stunting import newrekap_stunting_vmp8
from .f_newrekap_stunting_vmp11 import newrekap_stunting_vmp11
from .f_newrekap_stunting_dtl import newrekap_stunting_dtl_vmp8
from .f_newrekap_stunting_dtl_vmp11 import newrekap_stunting_dtl_vmp11
from .f_newrekap_stunting_ringkasan import newrekap_stunting_ringkasan_vmp8
from .f_newrekap_stunting_ringkasan_vmp11 import newrekap_stunting_ringkasan_vmp11
from .f_newongoing_stunting_dtl_regc import stunting_dtl_regc
from .f_newongoing_stunting_dtl_regb import stunting_dtl_regb
from .f_newongoing_stunting_dtl_rega import stunting_dtl_rega
from .f_newongoing_stunting_dtl_regd import stunting_dtl_regd
from .f_newongoing_stunting_v3_regc import stunting_v3_regc
from .f_newongoing_stunting_v3_rega import stunting_v3_rega
from .f_newongoing_stunting_v3_regb import stunting_v3_regb
from .f_newongoing_stunting_v3_regd import stunting_v3_regd
from .f_newongoing_stunting_genting_regb import stunting_genting_regb
from .f_newongoing_stunting_genting_rega import stunting_genting_rega
from .f_newongoing_stunting_genting_regc import stunting_genting_regc
from .f_newongoing_stunting_genting_regd import stunting_genting_regd
from .f_newongoing_stunting_genting_ringkasan_regb import stunting_genting_ringkasan_regb
from .f_newongoing_stunting_genting_ringkasan_rega import stunting_genting_ringkasan_rega
from .f_newongoing_stunting_genting_ringkasan_regc import stunting_genting_ringkasan_regc
from .f_newongoing_stunting_genting_ringkasan_regd import stunting_genting_ringkasan_regd
from .f_newongoing_stunting_ringkasan_v3_rega import stunting_ringkasan_v3_rega
from .f_newongoing_stunting_ringkasan_v3_regb import stunting_ringkasan_v3_regb
from .f_newongoing_stunting_ringkasan_v3_regc import stunting_ringkasan_v3_regc
from .f_newongoing_stunting_ringkasan_v3_regd import stunting_ringkasan_v3_regd

@extend_schema(
    methods=['GET'],
    parameters=[
        OpenApiParameter(name='v_bulan', required=True, type=int),
        OpenApiParameter(name='v_tahun', required=True, type=int),
        OpenApiParameter(name='v_nik', required=False, type=str),
        OpenApiParameter(name='v_nama', required=False, type=str),
        OpenApiParameter(name='v_id_propinsi', required=True, type=int),
        OpenApiParameter(name='v_id_kabupaten', required=True, type=int),
        OpenApiParameter(name='v_id_kecamatan', required=True, type=int),
        OpenApiParameter(name='v_id_kelurahan', required=True, type=int),
        OpenApiParameter(name='v_id_rw', required=False, type=int),
        OpenApiParameter(name='v_id_rt', required=False, type=str),
        OpenApiParameter(name='v_balita', required=False, type=int),
        OpenApiParameter(name='v_baduta', required=False, type=int),
        OpenApiParameter(name='v_status_hamil', required=False, type=bool),
        OpenApiParameter(name='v_status_pus', required=False, type=int),
        OpenApiParameter(name='v_status_verval', required=False, type=bool),
        OpenApiParameter(name='v_status_krs', required=False, type=int),
        OpenApiParameter(name='v_nik_tidak_wajar', required=False, type=bool),
        OpenApiParameter(name='v_status_keluarga', required=False, type=str),
        OpenApiParameter(name='v_kesejahteraan_prioritas', required=False, type=str),
        OpenApiParameter(name='v_flag_genting', required=False, type=int),
        OpenApiParameter(name='v_sudah_diukur', required=False, type=bool),
        OpenApiParameter(name='v_status_pengukuran', required=False, type=bool),
        OpenApiParameter(name='v_offset', required=False, type=int),
        OpenApiParameter(name='v_limit', required=False, type=int),
    ],
    responses={200: dict},
)
@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def f_newrekap_stunting_vmp8(request):
    if request.method == 'GET':
        params = {
            'v_bulan': request.GET.get('v_bulan', None),
            'v_tahun': request.GET.get('v_tahun', None),
            'v_nik': request.GET.get('v_nik', None),
            'v_nama': request.GET.get('v_nama', None),
            'v_id_propinsi': request.GET.get('v_id_propinsi', None),
            'v_id_kabupaten': request.GET.get('v_id_kabupaten', None),
            'v_id_kecamatan': request.GET.get('v_id_kecamatan', None),
            'v_id_kelurahan': request.GET.get('v_id_kelurahan', None),
            'v_id_rw': request.GET.get('v_id_rw', None),
            'v_id_rt': request.GET.get('v_id_rt', None),
            'v_balita': request.GET.get('v_balita', None),
            'v_baduta': request.GET.get('v_baduta', None),
            'v_status_hamil': request.GET.get('v_status_hamil', None),
            'v_status_pus': request.GET.get('v_status_pus', None),
            'v_status_verval': request.GET.get('v_status_verval', None),
            'v_status_krs': request.GET.get('v_status_krs', None),
            'v_nik_tidak_wajar': request.GET.get('v_nik_tidak_wajar', None),
            'v_status_keluarga': request.GET.get('v_status_keluarga', None),
            'v_kesejahteraan_prioritas': request.GET.get('v_kesejahteraan_prioritas', None),
            'v_flag_genting': request.GET.get('v_flag_genting', None),
            'v_sudah_diukur': request.GET.get('v_sudah_diukur', None),
            'v_status_pengukuran': request.GET.get('v_status_pengukuran', None),
            'v_offset': request.GET.get('v_offset', None),
            'v_limit': request.GET.get('v_limit', None),
        }

        try:
            if params['v_id_propinsi'] is not None:
                params['v_id_propinsi'] = int(params['v_id_propinsi'])

            if params['v_id_propinsi'] in {12, 18, 11, 13, 14, 17}:
                    results = await newrekap_stunting_vmp8(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {9, 16, 7, 28, 21, 23, 36, 10, 8, 30, 31, 33, 40, 32, 29, 26, 25, 27, 6, 2, 1, 5, 15, 20, 22, 19, 39, 37, 38, 4, 24, 3}:
                    results = await newrekap_stunting_vmp11(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            else:
                return JsonResponse({"error": f"Provinsi tidak ditemukan untuk id_provinsi = {params['v_id_propinsi']}"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

@extend_schema(
    methods=['GET'],
    parameters=[
        OpenApiParameter(name='v_id_provinsi', required=True, type=int),
        OpenApiParameter(name='v_nomor_keluarga', required=True, type=str),
        OpenApiParameter(name='v_nik_tidak_wajar', required=False, type=bool),
    ],
    responses={200: dict},
)
@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def f_newrekap_stunting_dtl_vmp8(request):
    if request.method == 'GET':
        params = {
            'v_id_provinsi': request.GET.get('v_id_provinsi', None),
            'v_nomor_keluarga': request.GET.get('v_nomor_keluarga', None),
            'v_nik_tidak_wajar': request.GET.get('v_nik_tidak_wajar', None),
        }

        try:
            if params['v_id_provinsi'] is not None:
                params['v_id_provinsi'] = int(params['v_id_provinsi'])
            
            if params['v_id_provinsi'] in {12, 18, 11, 13, 14, 17}:
                    results = await newrekap_stunting_dtl_vmp8(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_provinsi'] in {9, 16, 7, 28, 21, 23, 36, 10, 8, 30, 31, 33, 40, 32, 29, 26, 25, 27, 6, 2, 1, 5, 15, 20, 22, 19, 39, 37, 38, 4, 24, 3}:
                    results = await newrekap_stunting_dtl_vmp11(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            else:
                return JsonResponse({"error": f"Provinsi tidak ditemukan untuk id_provinsi = {params['v_id_propinsi']}"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

@extend_schema(
    methods=['GET'],
    parameters=[
        OpenApiParameter(name='v_bulan', required=True, type=int),
        OpenApiParameter(name='v_tahun', required=True, type=int),
        OpenApiParameter(name='v_nik', required=False, type=str),
        OpenApiParameter(name='v_nama', required=False, type=str),
        OpenApiParameter(name='v_id_propinsi', required=True, type=int),
        OpenApiParameter(name='v_id_kabupaten', required=True, type=int),
        OpenApiParameter(name='v_id_kecamatan', required=True, type=int),
        OpenApiParameter(name='v_id_kelurahan', required=True, type=int),
        OpenApiParameter(name='v_id_rw', required=False, type=int),
        OpenApiParameter(name='v_id_rt', required=False, type=str),
        OpenApiParameter(name='v_balita', required=False, type=int),
        OpenApiParameter(name='v_baduta', required=False, type=int),
        OpenApiParameter(name='v_status_hamil', required=False, type=bool),
        OpenApiParameter(name='v_status_pus', required=False, type=int),
        OpenApiParameter(name='v_status_verval', required=False, type=bool),
        OpenApiParameter(name='v_status_krs', required=False, type=int),
        OpenApiParameter(name='v_nik_tidak_wajar', required=False, type=bool),
        OpenApiParameter(name='v_status_keluarga', required=False, type=str),
        OpenApiParameter(name='v_kesejahteraan_prioritas', required=False, type=str),
        OpenApiParameter(name='v_flag_genting', required=False, type=int),
        OpenApiParameter(name='v_sudah_diukur', required=False, type=bool),
        OpenApiParameter(name='v_status_pengukuran', required=False, type=bool),
    ],
    responses={200: dict},
)
@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def f_newrekap_stunting_ringkasan_all(request):
    if request.method == 'GET':
        params = {
            'v_bulan': request.GET.get('v_bulan', None),
            'v_tahun': request.GET.get('v_tahun', None),
            'v_nik': request.GET.get('v_nik', None),
            'v_nama': request.GET.get('v_nama', None),
            'v_id_propinsi': request.GET.get('v_id_propinsi', None),
            'v_id_kabupaten': request.GET.get('v_id_kabupaten', None),
            'v_id_kecamatan': request.GET.get('v_id_kecamatan', None),
            'v_id_kelurahan': request.GET.get('v_id_kelurahan', None),
            'v_id_rw': request.GET.get('v_id_rw', None),
            'v_id_rt': request.GET.get('v_id_rt', None),
            'v_balita': request.GET.get('v_balita', None),
            'v_baduta': request.GET.get('v_baduta', None),
            'v_status_hamil': request.GET.get('v_status_hamil', None),
            'v_status_pus': request.GET.get('v_status_pus', None),
            'v_status_verval': request.GET.get('v_status_verval', None),
            'v_status_krs': request.GET.get('v_status_krs', None),
            'v_nik_tidak_wajar': request.GET.get('v_nik_tidak_wajar', None),
            'v_status_keluarga': request.GET.get('v_status_keluarga', None),
            'v_kesejahteraan_prioritas': request.GET.get('v_kesejahteraan_prioritas', None),
            'v_flag_genting': request.GET.get('v_flag_genting', None),
            'v_sudah_diukur': request.GET.get('v_sudah_diukur', None),
            'v_status_pengukuran': request.GET.get('v_status_pengukuran', None),
        }

        try:
            if params['v_id_propinsi'] is not None:
                params['v_id_propinsi'] = int(params['v_id_propinsi'])

            if params['v_id_propinsi'] in {12, 18, 11, 13, 14, 17}:
                    results = await newrekap_stunting_ringkasan_vmp8(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {9, 16, 7, 28, 21, 23, 36, 10, 8, 30, 31, 33, 40, 32, 29, 26, 25, 27, 6, 2, 1, 5, 15, 20, 22, 19, 39, 37, 38, 4, 24, 3}:
                    results = await newrekap_stunting_ringkasan_vmp11(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            else:
                return JsonResponse({"error": f"Provinsi tidak ditemukan untuk id_provinsi = {params['v_id_propinsi']}"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

@extend_schema(
    methods=['GET'],
    parameters=[
        OpenApiParameter(name='v_id_provinsi', required=True, type=int),
        OpenApiParameter(name='v_bulan', required=True, type=int),
        OpenApiParameter(name='v_tahun', required=True, type=int),
        OpenApiParameter(name='v_nomor_keluarga', required=True, type=str),
        OpenApiParameter(name='v_nik_tidak_wajar', required=False, type=str),
    ],
    responses={200: dict},
)
@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def ong_stunting_dtl_regc(request):
        
        params = {
            'v_id_provinsi': request.GET.get('v_id_provinsi', None),
            'v_bulan': request.GET.get('v_bulan', None),
            'v_tahun': request.GET.get('v_tahun', None),
            'v_nomor_keluarga': request.GET.get('v_nomor_keluarga', None),
            'v_nik_tidak_wajar': request.GET.get('v_nik_tidak_wajar', None),
        }

        try:
            if params['v_tahun'] is not None:
                params['v_tahun'] = int(params['v_tahun'])
            if params['v_bulan'] is not None:
                params['v_bulan'] = int(params['v_bulan'])
            if params['v_id_provinsi'] is not None:
                params['v_id_provinsi'] = int(params['v_id_provinsi'])

            if params['v_id_provinsi'] in {11, 13, 14, 17}:
                    results = await stunting_dtl_regc(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_provinsi'] in {12, 18}:
                    results = await stunting_dtl_regb(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_provinsi'] in {9, 16, 7, 28, 21, 23, 36, 10, 8, 30, 31, 33, 40, 32, 29, 26, 25, 27, 6, 2}:
                    results = await stunting_dtl_rega(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_provinsi'] in {1, 5, 15, 20, 22, 19, 39, 37, 38, 4, 24, 3}:
                    results = await stunting_dtl_regd(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            else:
                return JsonResponse({"error": f"Schema tidak ditemukan untuk id_provinsi = {params['v_id_provinsi']}"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

@extend_schema(
    methods=['GET'],
    parameters=[
        OpenApiParameter(name='v_bulan', required=True, type=int),
        OpenApiParameter(name='v_tahun', required=True, type=int),
        OpenApiParameter(name='v_nik', required=False, type=str),
        OpenApiParameter(name='v_nama', required=False, type=str),
        OpenApiParameter(name='v_id_propinsi', required=True, type=int),
        OpenApiParameter(name='v_id_kabupaten', required=True, type=int),
        OpenApiParameter(name='v_id_kecamatan', required=True, type=int),
        OpenApiParameter(name='v_id_kelurahan', required=True, type=int),
        OpenApiParameter(name='v_id_rw', required=False, type=int),
        OpenApiParameter(name='v_id_rt', required=False, type=str),
        OpenApiParameter(name='v_balita', required=False, type=int),
        OpenApiParameter(name='v_baduta', required=False, type=int),
        OpenApiParameter(name='v_status_hamil', required=False, type=bool),
        OpenApiParameter(name='v_status_pus', required=False, type=int),
        OpenApiParameter(name='v_status_verval', required=False, type=bool),
        OpenApiParameter(name='v_status_krs', required=False, type=int),
        OpenApiParameter(name='v_nik_tidak_wajar', required=False, type=bool),
        OpenApiParameter(name='v_status_keluarga', required=False, type=str),
        OpenApiParameter(name='v_kesejahteraan_prioritas', required=False, type=str),
        OpenApiParameter(name='v_flag_genting', required=False, type=int),
        OpenApiParameter(name='v_sasaran_genting', required=False, type=str),
        OpenApiParameter(name='v_sudah_diukur', required=False, type=bool),
        OpenApiParameter(name='v_status_pengukuran', required=False, type=bool),
        OpenApiParameter(name='verval_ya', required=False, type=int),
        OpenApiParameter(name='v_offset', required=False, type=int),
        OpenApiParameter(name='v_limit', required=False, type=int),
    ],
    responses={200: dict},
)
@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def ong_stunting_v3_regc(request):
    if request.method == 'GET':
        params = {
            'v_bulan': request.GET.get('v_bulan', None),
            'v_tahun': request.GET.get('v_tahun', None),
            'v_nik': request.GET.get('v_nik', None),
            'v_nama': request.GET.get('v_nama', None),
            'v_id_propinsi': request.GET.get('v_id_propinsi', None),
            'v_id_kabupaten': request.GET.get('v_id_kabupaten', None),
            'v_id_kecamatan': request.GET.get('v_id_kecamatan', None),
            'v_id_kelurahan': request.GET.get('v_id_kelurahan', None),
            'v_id_rw': request.GET.get('v_id_rw', None),
            'v_id_rt': request.GET.get('v_id_rt', None),
            'v_balita': request.GET.get('v_balita', None),
            'v_baduta': request.GET.get('v_baduta', None),
            'v_status_hamil': request.GET.get('v_status_hamil', None),
            'v_status_pus': request.GET.get('v_status_pus', None),
            'v_status_verval': request.GET.get('v_status_verval', None),
            'v_status_krs': request.GET.get('v_status_krs', None),
            'v_nik_tidak_wajar': request.GET.get('v_nik_tidak_wajar', None),
            'v_status_keluarga': request.GET.get('v_status_keluarga', None),
            'v_kesejahteraan_prioritas': request.GET.get('v_kesejahteraan_prioritas', None),
            'v_flag_genting': request.GET.get('v_flag_genting', None),
            'v_sasaran_genting': request.GET.get('v_sasaran_genting', None),
            'v_sudah_diukur': request.GET.get('v_sudah_diukur', None),
            'v_status_pengukuran': request.GET.get('v_status_pengukuran', None),
            'verval_ya': request.GET.get('verval_ya', None),
            'v_offset': request.GET.get('v_offset', None),
            'v_limit': request.GET.get('v_limit', None),
        }
        # params['id_provinsi'] = params['v_id_propinsi']

        try:
            if params['v_id_propinsi'] is not None:
                params['v_id_propinsi'] = int(params['v_id_propinsi'])

            if params['v_id_propinsi'] in {11, 13, 14, 17}:
                    results = await stunting_v3_regc(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {9, 16, 7, 28, 21, 23, 36, 10, 8, 30, 31, 33, 40, 32, 29, 26, 25, 27, 6, 2}:
                    results = await stunting_v3_rega(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {12, 18}:
                    results = await stunting_v3_regb(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {1, 5, 15, 20, 22, 19, 39, 37, 38, 4, 24, 3}:
                    results = await stunting_v3_regd(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            else:
                return JsonResponse({"error": f"Schema tidak ditemukan untuk id_provinsi = {params['v_id_propinsi']}"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

@extend_schema(
    methods=['GET'],
    parameters=[
        OpenApiParameter(name='v_bulan', required=True, type=int),
        OpenApiParameter(name='v_tahun', required=True, type=int),
        OpenApiParameter(name='v_nik', required=False, type=str),
        OpenApiParameter(name='v_nama', required=False, type=str),
        OpenApiParameter(name='v_id_propinsi', required=True, type=int),
        OpenApiParameter(name='v_id_kabupaten', required=True, type=int),
        OpenApiParameter(name='v_id_kecamatan', required=True, type=int),
        OpenApiParameter(name='v_id_kelurahan', required=True, type=int),
        OpenApiParameter(name='v_id_rw', required=False, type=int),
        OpenApiParameter(name='v_id_rt', required=False, type=str),
        OpenApiParameter(name='v_balita', required=False, type=int),
        OpenApiParameter(name='v_baduta', required=False, type=int),
        OpenApiParameter(name='v_status_hamil', required=False, type=bool),
        OpenApiParameter(name='v_status_pus', required=False, type=int),
        OpenApiParameter(name='v_status_verval', required=False, type=bool),
        OpenApiParameter(name='v_status_krs', required=False, type=int),
        OpenApiParameter(name='v_nik_tidak_wajar', required=False, type=bool),
        OpenApiParameter(name='v_status_keluarga', required=False, type=str),
        OpenApiParameter(name='v_kesejahteraan_prioritas', required=False, type=str),
        OpenApiParameter(name='v_flag_genting', required=False, type=int),
        OpenApiParameter(name='v_sasaran_genting', required=False, type=str),
        OpenApiParameter(name='v_entry_genting', required=False, type=int),
        OpenApiParameter(name='v_sudah_diukur', required=False, type=bool),
        OpenApiParameter(name='v_status_pengukuran', required=False, type=bool),
        OpenApiParameter(name='v_offset', required=False, type=int),
        OpenApiParameter(name='v_limit', required=False, type=int),
    ],
    responses={200: dict},
)
@api_view(['GET'])        
@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def ong_stunting_genting_allreg(request):
    if request.method == 'GET':
        params = {
            'v_bulan': request.GET.get('v_bulan', None),
            'v_tahun': request.GET.get('v_tahun', None),
            'v_nik': request.GET.get('v_nik', None),
            'v_nama': request.GET.get('v_nama', None),
            'v_id_propinsi': request.GET.get('v_id_propinsi', None),
            'v_id_kabupaten': request.GET.get('v_id_kabupaten', None),
            'v_id_kecamatan': request.GET.get('v_id_kecamatan', None),
            'v_id_kelurahan': request.GET.get('v_id_kelurahan', None),
            'v_id_rw': request.GET.get('v_id_rw', None),
            'v_id_rt': request.GET.get('v_id_rt', None),
            'v_balita': request.GET.get('v_balita', None),
            'v_baduta': request.GET.get('v_baduta', None),
            'v_status_hamil': request.GET.get('v_status_hamil', None),
            'v_status_pus': request.GET.get('v_status_pus', None),
            'v_status_verval': request.GET.get('v_status_verval', None),
            'v_status_krs': request.GET.get('v_status_krs', None),
            'v_nik_tidak_wajar': request.GET.get('v_nik_tidak_wajar', None),
            'v_status_keluarga': request.GET.get('v_status_keluarga', None),
            'v_kesejahteraan_prioritas': request.GET.get('v_kesejahteraan_prioritas', None),
            'v_flag_genting': request.GET.get('v_flag_genting', None),
            'v_sasaran_genting': request.GET.get('v_sasaran_genting', None),
            'v_entry_genting': request.GET.get('v_entry_genting', None),
            'v_sudah_diukur': request.GET.get('v_sudah_diukur', None),
            'v_status_pengukuran': request.GET.get('v_status_pengukuran', None),
            'v_offset': request.GET.get('v_offset', None),
            'v_limit': request.GET.get('v_limit', None),
        }
        # params['id_provinsi'] = params['v_id_propinsi']

        try:
            if params['v_id_propinsi'] is not None:
                params['v_id_propinsi'] = int(params['v_id_propinsi'])

            if params['v_id_propinsi'] in {11, 13, 14, 17}:
                    results = await stunting_genting_regc(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {9, 16, 7, 28, 21, 23, 36, 10, 8, 30, 31, 33, 40, 32, 29, 26, 25, 27, 6, 2}:
                    results = await stunting_genting_rega(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {12, 18}:
                    results = await stunting_genting_regb(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {1, 5, 15, 20, 22, 19, 39, 37, 38, 4, 24, 3}:
                    results = await stunting_genting_regd(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            else:
                return JsonResponse({"error": f"Schema tidak ditemukan untuk id_provinsi = {params['v_id_propinsi']}"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        
@extend_schema(
    methods=['GET'],
    parameters=[
        OpenApiParameter(name='v_bulan', required=True, type=int),
        OpenApiParameter(name='v_tahun', required=True, type=int),
        OpenApiParameter(name='v_nik', required=False, type=str),
        OpenApiParameter(name='v_nama', required=False, type=str),
        OpenApiParameter(name='v_id_propinsi', required=True, type=int),
        OpenApiParameter(name='v_id_kabupaten', required=True, type=int),
        OpenApiParameter(name='v_id_kecamatan', required=True, type=int),
        OpenApiParameter(name='v_id_kelurahan', required=True, type=int),
        OpenApiParameter(name='v_id_rw', required=False, type=int),
        OpenApiParameter(name='v_id_rt', required=False, type=str),
        OpenApiParameter(name='v_balita', required=False, type=int),
        OpenApiParameter(name='v_baduta', required=False, type=int),
        OpenApiParameter(name='v_status_hamil', required=False, type=bool),
        OpenApiParameter(name='v_status_pus', required=False, type=int),
        OpenApiParameter(name='v_status_verval', required=False, type=bool),
        OpenApiParameter(name='v_status_krs', required=False, type=int),
        OpenApiParameter(name='v_nik_tidak_wajar', required=False, type=bool),
        OpenApiParameter(name='v_status_keluarga', required=False, type=str),
        OpenApiParameter(name='v_kesejahteraan_prioritas', required=False, type=str),
        OpenApiParameter(name='v_flag_genting', required=False, type=int),
        OpenApiParameter(name='v_sasaran_genting', required=False, type=str),
        OpenApiParameter(name='v_entry_genting', required=False, type=int),
        OpenApiParameter(name='v_sudah_diukur', required=False, type=bool),
        OpenApiParameter(name='v_status_pengukuran', required=False, type=bool),
    ],
    responses={200: dict},
)
@api_view(['GET'])        
@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def ong_stunting_genting_ringkasan_allreg(request):
    if request.method == 'GET':
        params = {
            'v_bulan': request.GET.get('v_bulan', None),
            'v_tahun': request.GET.get('v_tahun', None),
            'v_nik': request.GET.get('v_nik', None),
            'v_nama': request.GET.get('v_nama', None),
            'v_id_propinsi': request.GET.get('v_id_propinsi', None),
            'v_id_kabupaten': request.GET.get('v_id_kabupaten', None),
            'v_id_kecamatan': request.GET.get('v_id_kecamatan', None),
            'v_id_kelurahan': request.GET.get('v_id_kelurahan', None),
            'v_id_rw': request.GET.get('v_id_rw', None),
            'v_id_rt': request.GET.get('v_id_rt', None),
            'v_balita': request.GET.get('v_balita', None),
            'v_baduta': request.GET.get('v_baduta', None),
            'v_status_hamil': request.GET.get('v_status_hamil', None),
            'v_status_pus': request.GET.get('v_status_pus', None),
            'v_status_verval': request.GET.get('v_status_verval', None),
            'v_status_krs': request.GET.get('v_status_krs', None),
            'v_nik_tidak_wajar': request.GET.get('v_nik_tidak_wajar', None),
            'v_status_keluarga': request.GET.get('v_status_keluarga', None),
            'v_kesejahteraan_prioritas': request.GET.get('v_kesejahteraan_prioritas', None),
            'v_flag_genting': request.GET.get('v_flag_genting', None),
            'v_sasaran_genting': request.GET.get('v_sasaran_genting', None),
            'v_entry_genting': request.GET.get('v_entry_genting', None),
            'v_sudah_diukur': request.GET.get('v_sudah_diukur', None),
            'v_status_pengukuran': request.GET.get('v_status_pengukuran', None),
        }
        # params['id_provinsi'] = params['v_id_propinsi']

        try:
            if params['v_tahun'] is not None:
                params['v_tahun'] = int(params['v_tahun'])
            if params['v_bulan'] is not None:
                params['v_bulan'] = int(params['v_bulan'])
            if params['v_id_propinsi'] is not None:
                params['v_id_propinsi'] = int(params['v_id_propinsi'])

            if params['v_id_propinsi'] in {11, 13, 14, 17}:
                    results = await stunting_genting_ringkasan_regc(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {9, 16, 7, 28, 21, 23, 36, 10, 8, 30, 31, 33, 40, 32, 29, 26, 25, 27, 6, 2}:
                    results = await stunting_genting_ringkasan_rega(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {12, 18}:
                    results = await stunting_genting_ringkasan_regb(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {1, 5, 15, 20, 22, 19, 39, 37, 38, 4, 24, 3}:
                    results = await stunting_genting_ringkasan_regd(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            else:
                return JsonResponse({"error": f"Schema tidak ditemukan untuk id_provinsi = {params['v_id_propinsi']}"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        
@extend_schema(
    methods=['GET'],
    parameters=[
        OpenApiParameter(name='v_bulan', required=True, type=int),
        OpenApiParameter(name='v_tahun', required=True, type=int),
        OpenApiParameter(name='v_nik', required=False, type=str),
        OpenApiParameter(name='v_nama', required=False, type=str),
        OpenApiParameter(name='v_id_propinsi', required=True, type=int),
        OpenApiParameter(name='v_id_kabupaten', required=True, type=int),
        OpenApiParameter(name='v_id_kecamatan', required=True, type=int),
        OpenApiParameter(name='v_id_kelurahan', required=True, type=int),
        OpenApiParameter(name='v_id_rw', required=False, type=int),
        OpenApiParameter(name='v_id_rt', required=False, type=str),
        OpenApiParameter(name='v_balita', required=False, type=int),
        OpenApiParameter(name='v_baduta', required=False, type=int),
        OpenApiParameter(name='v_status_hamil', required=False, type=bool),
        OpenApiParameter(name='v_status_pus', required=False, type=int),
        OpenApiParameter(name='v_status_verval', required=False, type=bool),
        OpenApiParameter(name='v_status_krs', required=False, type=int),
        OpenApiParameter(name='v_nik_tidak_wajar', required=False, type=bool),
        OpenApiParameter(name='v_status_keluarga', required=False, type=str),
        OpenApiParameter(name='v_kesejahteraan_prioritas', required=False, type=str),
        OpenApiParameter(name='v_flag_genting', required=False, type=int),
        OpenApiParameter(name='v_sasaran_genting', required=False, type=str),
        OpenApiParameter(name='v_sudah_diukur', required=False, type=bool),
        OpenApiParameter(name='v_status_pengukuran', required=False, type=bool),
        OpenApiParameter(name='verval_ya', required=False, type=int),
    ],
    responses={200: dict},
)
@api_view(['GET'])        
@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def ong_stunting_ringkasan_v3_allreg(request):
    if request.method == 'GET':
        params = {
            'v_bulan': request.GET.get('v_bulan', None),
            'v_tahun': request.GET.get('v_tahun', None),
            'v_nik': request.GET.get('v_nik', None),
            'v_nama': request.GET.get('v_nama', None),
            'v_id_propinsi': request.GET.get('v_id_propinsi', None),
            'v_id_kabupaten': request.GET.get('v_id_kabupaten', None),
            'v_id_kecamatan': request.GET.get('v_id_kecamatan', None),
            'v_id_kelurahan': request.GET.get('v_id_kelurahan', None),
            'v_id_rw': request.GET.get('v_id_rw', None),
            'v_id_rt': request.GET.get('v_id_rt', None),
            'v_balita': request.GET.get('v_balita', None),
            'v_baduta': request.GET.get('v_baduta', None),
            'v_status_hamil': request.GET.get('v_status_hamil', None),
            'v_status_pus': request.GET.get('v_status_pus', None),
            'v_status_verval': request.GET.get('v_status_verval', None),
            'v_status_krs': request.GET.get('v_status_krs', None),
            'v_nik_tidak_wajar': request.GET.get('v_nik_tidak_wajar', None),
            'v_status_keluarga': request.GET.get('v_status_keluarga', None),
            'v_kesejahteraan_prioritas': request.GET.get('v_kesejahteraan_prioritas', None),
            'v_flag_genting': request.GET.get('v_flag_genting', None),
            'v_sasaran_genting': request.GET.get('v_sasaran_genting', None),
            'v_sudah_diukur': request.GET.get('v_sudah_diukur', None),
            'v_status_pengukuran': request.GET.get('v_status_pengukuran', None),
            'verval_ya': request.GET.get('verval_ya', None),
        }
        # params['id_provinsi'] = params['v_id_propinsi']

        try:
            if params['v_tahun'] is not None:
                params['v_tahun'] = int(params['v_tahun'])
            if params['v_bulan'] is not None:
                params['v_bulan'] = int(params['v_bulan'])
            if params['v_id_propinsi'] is not None:
                params['v_id_propinsi'] = int(params['v_id_propinsi'])

            if params['v_id_propinsi'] in {11, 13, 14, 17}:
                    results = await stunting_ringkasan_v3_regc(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {9, 16, 7, 28, 21, 23, 36, 10, 8, 30, 31, 33, 40, 32, 29, 26, 25, 27, 6, 2}:
                    results = await stunting_ringkasan_v3_rega(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {12, 18}:
                    results = await stunting_ringkasan_v3_regb(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            if params['v_id_propinsi'] in {1, 5, 15, 20, 22, 19, 39, 37, 38, 4, 24, 3}:
                    results = await stunting_ringkasan_v3_regd(params)
                    data = [dict(row) for row in results]
                    return JsonResponse({"data": data}, safe=False)
            else:
                return JsonResponse({"error": f"Schema tidak ditemukan untuk id_provinsi = {params['v_id_propinsi']}"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)