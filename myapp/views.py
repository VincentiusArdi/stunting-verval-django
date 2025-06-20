from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
import json
from .f_newongoing_stunting_v2_bali import stunting_v3_bali
from .f_newongoing_stunting_v3_diy import stunting_v3_diy
from .f_newongoing_stunting_v3_jateng import stunting_v3_jateng
from .f_newongoing_stunting_dtl_bali import stunting_dtl_bali
from .f_newrekap_stunting import newrekap_stunting_vmp8
from .f_newrekap_stunting_dtl import newrekap_stunting_dtl_vmp8
from .f_newongoing_stunting_dtl_regc import stunting_dtl_regc
from .f_newongoing_stunting_dtl_regb import stunting_dtl_regb

@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def ong_stunting_v3_bali(request):
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

        try:
            data = await stunting_v3_bali(params)
            return JsonResponse({"data": data}, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def ong_stunting_v3_diy(request):
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

        try:
            data = await stunting_v3_diy(params)
            return JsonResponse({"data": data}, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def ong_stunting_v3_jateng(request):
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

        try:
            data = await stunting_v3_jateng(params)
            return JsonResponse({"data": data}, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def ong_stunting_dtl_bali(request):
    if request.method == 'GET':
        params = {
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

            data = await stunting_dtl_bali(params)
            return JsonResponse({"data": data}, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

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
            data = await newrekap_stunting_vmp8(params)
            return JsonResponse({"data": data}, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def f_newrekap_stunting_dtl_vmp8(request):
    if request.method == 'GET':
        params = {
            'v_nomor_keluarga': request.GET.get('v_nomor_keluarga', None),
            'v_nik_tidak_wajar': request.GET.get('v_nik_tidak_wajar', None),
        }

        try:
            data = await newrekap_stunting_dtl_vmp8(params)
            return JsonResponse({"data": data}, safe=False)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@permission_classes([AllowAny])
@csrf_exempt
@async_to_sync
async def ong_stunting_dtl_regc(request):
    if request.method == 'GET':
        params = {
            'id_provinsi': request.GET.get('id_provinsi', None),
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
            if params['id_provinsi'] is not None:
                params['id_provinsi'] = int(params['id_provinsi'])

            if params['id_provinsi'] in {11, 13, 14, 17}:
                    data = await stunting_dtl_regc(params)
                    return JsonResponse({"data": data}, safe=False)
            if params['id_provinsi'] in {12, 18}:
                    data = await stunting_dtl_regb(params)
                    return JsonResponse({"data": data}, safe=False)
            else:
                return JsonResponse({"error": f"Schema tidak ditemukan untuk id_provinsi = {params['id_provinsi']}"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)