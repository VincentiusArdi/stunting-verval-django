from myapp.queries import (
    f_newongoing_stunting_dtl_rega, f_newongoing_stunting_dtl_regb, f_newongoing_stunting_dtl_regc, 
    f_newrekap_stunting_vmp11, f_newongoing_stunting_genting_regd, f_newongoing_stunting_genting_regc,
    f_newongoing_stunting_dtl_regd, f_newongoing_stunting_genting_rega, f_newongoing_stunting_genting_regb,
    f_newongoing_stunting_genting_ringkasan_rega, f_newongoing_stunting_genting_ringkasan_regb, f_newongoing_stunting_genting_ringkasan_regc,
    f_newongoing_stunting_genting_ringkasan_regd, f_newongoing_stunting_v3_rega, f_newongoing_stunting_v3_regb, f_newongoing_stunting_v3_regc,
    f_newongoing_stunting_v3_regd, f_newrekap_stunting, f_newrekap_stunting_dtl, f_newrekap_stunting_dtl_vmp11, f_newrekap_stunting_ringkasan, 
    f_newrekap_stunting_ringkasan_vmp11)

from myapp.queries.f_newongoing_stunting_v3_rega import stunting_v3_rega
from myapp.queries.f_newongoing_stunting_v3_regb import stunting_v3_regb
from myapp.queries.f_newongoing_stunting_v3_regc import stunting_v3_regc
from myapp.queries.f_newongoing_stunting_v3_regd import stunting_v3_regd


class StuntingService:
    @staticmethod
    async def get_stunting_data(params):
        try:
            v_id_provinsi = int(params.get("v_id_propinsi"))
            page = int(params.get("page", 1))
            record_per_page = 10

            ls_data = []
            ls_ongoing = []
            ls_rekap = []

            total_record = 0
            te_ongoing = te_sasaran = te_ringkasan_ongoing = te_ringkasan_sasaran = 0

            lower = (page - 1) * record_per_page
            upper = lower + record_per_page

            # Tentukan scData
            status_verval = params.get("statusVerval")
            sasaran_genting = params.get("sasaranGenting")
            sc_data = 3
            if status_verval is not None:
                sc_data = 1 if status_verval == 'true' else 2
            if sasaran_genting:
                sc_data = 1


            # Panggil query berdasarkan id_provinsi
            if v_id_provinsi in {11, 13, 14, 17}:
                results = await stunting_v3_regc(params)
            elif v_id_provinsi in {12, 18}:
                results = await stunting_v3_regb(params)
            elif v_id_provinsi in {9, 16, 7, 28, 21, 23, 36, 10, 8, 30, 31, 33, 40, 32, 29, 26, 25, 27, 6, 2}:
                results = await stunting_v3_rega(params)
            elif v_id_provinsi in {1, 5, 15, 20, 22, 19, 39, 37, 38, 4, 24, 3}:
                results = await stunting_v3_regd(params)
            else:
                return {"error": f"Schema tidak ditemukan untuk id_provinsi = {v_id_provinsi}"}, 400

            # Konversi hasil
            data = [dict(row) for row in results]
            return {"data": data}, 200
        except ValueError as e:
            return {"error": str(e)}, 400