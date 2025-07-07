import time
from django.forms.models import model_to_dict
from myapp.models import DataStunting
from myapp.queries.f_newongoing_stunting_v3_rega import stunting_v3_rega
from myapp.queries.f_newongoing_stunting_v3_regb import stunting_v3_regb
from myapp.queries.f_newongoing_stunting_v3_regc import stunting_v3_regc
from myapp.queries.f_newongoing_stunting_v3_regd import stunting_v3_regd
from myapp.queries.f_newongoing_stunting_ringkasan_v3_rega import stunting_ringkasan_v3_rega
from myapp.queries.f_newongoing_stunting_ringkasan_v3_regb import stunting_ringkasan_v3_regb
from myapp.queries.f_newongoing_stunting_ringkasan_v3_regc import stunting_ringkasan_v3_regc
from myapp.queries.f_newongoing_stunting_ringkasan_v3_regd import stunting_ringkasan_v3_regd
from myapp.queries.f_newongoing_stunting_genting_rega import stunting_genting_rega
from myapp.queries.f_newongoing_stunting_genting_regb import stunting_genting_regb
from myapp.queries.f_newongoing_stunting_genting_regc import stunting_genting_regc
from myapp.queries.f_newongoing_stunting_genting_regd import stunting_genting_regd
from myapp.queries.f_newongoing_stunting_genting_ringkasan_rega import stunting_genting_ringkasan_rega
from myapp.queries.f_newongoing_stunting_genting_ringkasan_regb import stunting_genting_ringkasan_regb
from myapp.queries.f_newongoing_stunting_genting_ringkasan_regc import stunting_genting_ringkasan_regc
from myapp.queries.f_newongoing_stunting_genting_ringkasan_regd import stunting_genting_ringkasan_regd
from myapp.queries.f_newrekap_stunting import newrekap_stunting_vmp8
from myapp.queries.f_newrekap_stunting_ringkasan import newrekap_stunting_ringkasan_vmp8
from myapp.queries.f_newrekap_stunting_vmp11 import newrekap_stunting_vmp11
from myapp.queries.f_newrekap_stunting_ringkasan_vmp11 import newrekap_stunting_ringkasan_vmp11
from myapp.utils.voltage_decrypt import voltageDecrypt



class StuntingService:
    @staticmethod
    async def get_stunting_data(params):
        try:
            v_id_provinsi = int(params.get("v_id_propinsi"))
            page = int(params.get("page", 1))
            record_per_page = 20

            ls_data = []
            ls_ongoing = []
            ls_rekap = []

            total_record = 0
            te_ongoing = 0
            te_sasaran = 0
            te_ringkasan_ongoing = 0
            te_ringkasan_sasaran = 0

            lower = (page - 1) * record_per_page
            upper = lower + record_per_page

            params["v_offset"] = lower
            params["v_limit"] = record_per_page

            nama = params.get("v_nama")
            if nama:
                nama = nama.upper()

            statusKeluarga = params.get("v_status_keluarga")


             # Panggil query berdasarkan id_provinsi
            if v_id_provinsi in {11, 13, 14, 17}:
                dsRekapOnGo =  stunting_v3_regc
                dsTotalRekapOnGo =  stunting_ringkasan_v3_regc
                dsRekapOnGoGenting =  stunting_genting_regc
                dsTotalRekapOnGoGenting =  stunting_genting_ringkasan_regc
            elif v_id_provinsi in {12, 18}:
                dsRekapOnGo = stunting_v3_regb
                dsTotalRekapOnGo =  stunting_ringkasan_v3_regb
                dsRekapOnGoGenting =  stunting_genting_regb
                dsTotalRekapOnGoGenting =  stunting_genting_ringkasan_regb
            elif v_id_provinsi in {9, 16, 7, 28, 21, 23, 36, 10, 8, 30, 31, 33, 40, 32, 29, 26, 25, 27, 6, 2}:
                dsRekapOnGo =  stunting_v3_rega
                dsTotalRekapOnGo =  stunting_ringkasan_v3_rega
                dsRekapOnGoGenting =  stunting_genting_rega
                dsTotalRekapOnGoGenting =  stunting_genting_ringkasan_rega
            elif v_id_provinsi in {1, 5, 15, 20, 22, 19, 39, 37, 38, 4, 24, 3}:
                dsRekapOnGo = stunting_v3_regd
                dsTotalRekapOnGo =  stunting_ringkasan_v3_regd
                dsRekapOnGoGenting =  stunting_genting_regd
                dsTotalRekapOnGoGenting =  stunting_genting_ringkasan_regd
            else:
                return {"error": f"Schema on going tidak ditemukan untuk id_provinsi = {v_id_provinsi}"}, 400

            # sc data sasaran berdasarkan id_provinsi
            if v_id_provinsi in {12, 18, 11, 13, 14, 17}:
                dsRekapSasaran = newrekap_stunting_vmp8
                dsTotalRekapSasaran = newrekap_stunting_ringkasan_vmp8
            elif v_id_provinsi in {9, 16, 7, 28, 21, 23, 36, 10, 8, 30, 31, 33, 40, 32, 29, 26, 25, 27, 6, 2, 1, 5, 15, 20, 22, 19, 39, 37, 38, 4, 24, 3}:
                dsRekapSasaran = newrekap_stunting_vmp11
                dsTotalRekapSasaran = newrekap_stunting_ringkasan_vmp11

            # Tentukan scData
            status_verval = params.get("statusVerval")
            sasaran_genting = params.get("sasaranGenting")
            sc_data = 3
            if status_verval is not None:
                sc_data = 1 if status_verval == 'true' else 2
            if sasaran_genting:
                sc_data = 1


            # Logic Retrieving data
            if statusKeluarga is not None and sc_data == 1:
                startRecord = time.time()
                
                if params.get("v_flag_genting") is not None and params.get("v_flag_genting") == 1:
                    total_record_on_going = await dsTotalRekapOnGoGenting(params)
                elif params.get("v_flag_genting") is None:
                    total_record_on_going = await dsTotalRekapOnGo(params)

                te_ringkasan_ongoing = (time.time() - startRecord) * 1000
                count_record_on_going = total_record_on_going[0]['jlh_row'] if total_record_on_going else 0
                total_record += count_record_on_going
                print("elapse time function ringkasan on going: %sms",te_ringkasan_ongoing)
            
                print("request data from on going only")
                startRekap = time.time()
                
                if params.get("v_flag_genting") is not None and params.get("v_flag_genting") == 1:
                    ls_ongoing = await dsRekapOnGoGenting(params)
                elif params.get("v_flag_genting") is None:
                    ls_ongoing = await dsRekapOnGo(params)
                
                te_ongoing = (time.time() - startRekap) * 1000
                print("elapse time function rekap on going : %sms", te_ongoing)
            elif sc_data == 2:
                params["status_verval"] = None
                startRecordSasaran = time.time()
                total_record_sasaran = await dsTotalRekapSasaran(params)
                te_ringkasan_sasaran = (time.time() - startRecordSasaran) * 1000
                count_record_sasaran = total_record_sasaran[0]['jlh_row'] if total_record_sasaran else 0
                total_record += count_record_sasaran
                print("elapse time function ringkasan sasaran: %sms",te_ringkasan_sasaran)

                print("request data from sasaran only")
                startRekapSasaran = time.time()
                ls_rekap = await dsRekapSasaran(params)
                te_rekap_sasaran = (time.time() - startRekapSasaran) * 1000
                print("elapse time function rekap sasaran : %sms", te_rekap_sasaran)
            else :
                startRecord = time.time()
                
                if params.get("v_flag_genting") is not None and params.get("v_flag_genting") == 1:
                    total_record_on_going = await dsTotalRekapOnGoGenting(params)
                elif params.get("v_flag_genting") is None:
                    total_record_on_going = await dsTotalRekapOnGo(params)

                te_ringkasan_ongoing = (time.time() - startRecord) * 1000
                print("elapse time function ringkasan on going: %sms",te_ringkasan_ongoing)

                startRecordSasaran = time.time()
                total_record_sasaran = await dsTotalRekapSasaran(params)
                te_ringkasan_sasaran = (time.time() - startRecordSasaran) * 1000
                print("elapse time function ringkasan sasaran: %sms",te_ringkasan_sasaran)

                count_record_sasaran = total_record_sasaran[0]['jlh_row'] if total_record_sasaran else 0
                count_record_on_going = total_record_on_going[0]['jlh_row'] if total_record_on_going else 0

                total_record += count_record_on_going + count_record_sasaran

                if lower < count_record_on_going and upper <= count_record_on_going:
                    print("request data from on going only")
                    startRekap = time.time()
                    
                    if params.get("v_flag_genting") is not None and params.get("v_flag_genting") == 1:
                        ls_ongoing = await dsRekapOnGoGenting(params)
                    elif params.get("v_flag_genting") is None:
                        ls_ongoing = await dsRekapOnGo(params)
                    
                    te_ongoing = (time.time() - startRekap) * 1000
                    print("elapse time function rekap on going : %sms", te_ongoing)
                elif lower > count_record_on_going and lower >= count_record_on_going:
                    print("request data from sasaran only")

                    lowerSasaran = lower - count_record_on_going

                    params["v_offset"] = lowerSasaran

                    startRekapSasaran = time.time()
                    ls_rekap = await dsRekapSasaran(params)
                    te_rekap_sasaran = (time.time() - startRekapSasaran) * 1000
                    print("elapse time function rekap sasaran : %sms", te_rekap_sasaran)
                elif lower <= count_record_on_going and upper > count_record_on_going:
                    print("request data from sasaran and on going")
                    
                    offsetOnGoing = lower
                    limitOnGoing = record_per_page

                    params["v_offset"] = offsetOnGoing
                    params["v_limit"] = limitOnGoing

                    print("v_offset : %s , v_limit : %s", params.get("v_offset"), params.get("v_limit"))

                    if params.get("v_flag_genting") is not None and params.get("v_flag_genting") == 1:
                        ls_ongoing = await dsRekapOnGoGenting(params)
                    elif params.get("v_flag_genting") is None:
                        ls_ongoing = await dsRekapOnGo(params)
                    
                    te_ongoing = (time.time() - startRekap) * 1000
                    print("elapse time function rekap on going : %sms", te_ongoing)

                    lowerSasaran = 0
                    upperSasaran = page * record_per_page
            
                    params["v_offset"] = lowerSasaran
                    params["v_limit"] = upperSasaran

                    startRekapSasaran = time.time()
                    ls_rekap = await dsRekapSasaran(params)
                    te_rekap_sasaran = (time.time() - startRekapSasaran) * 1000
                    print("elapse time function rekap sasaran : %sms", te_rekap_sasaran)
            
            if ls_ongoing:
                onGoing = [dict(row) for row in ls_ongoing]
                for row in onGoing:
                    nik =  voltageDecrypt(v_id_provinsi=row.get("id_provinsi"), chipertext=row.get("nik"),method="numeric")
                    nikIstri =  voltageDecrypt(v_id_provinsi=row.get("id_provinsi"), chipertext=row.get("nik_istri"),method="numeric")
                    nama =  voltageDecrypt(v_id_provinsi=row.get("id_provinsi"), chipertext=row.get("nama"),method="alphanumericv2")
                    namaIstri =  voltageDecrypt(v_id_provinsi=row.get("id_provinsi"), chipertext=row.get("nama_istri"),method="alphanumericv2")
                    print("nik :", nik)
                    print("nama :", nama)
                    print("nik istri :", nikIstri)
                    print("nama istri :", namaIstri)

                    row["flag"] = "progress"
                    row["nik"] = nik or ""
                    row["nama"] = nama or ""
                    row["nik_istri"] = nikIstri or ""
                    row["nama_istri"] = namaIstri or ""
                    ls_data.append(row)

            if ls_rekap:
                rekap = [dict(row) for row in ls_rekap]
                for rowSasaran in rekap:
                    rowSasaran["flag"] = "sasaran"
                    ls_data.append(rowSasaran)

            # Konversi hasil
            data = [DataStunting(**row) for row in ls_data]
            data_dicts = [model_to_dict(obj) for obj in data]
            return {
                "data": data_dicts,
                "page": page,
                "recordPerPage": record_per_page,
                "totalRecord": total_record,
                "elapseTimeFunctionOngoing": te_ongoing,
                "elapseTimeFunctionSasaran": te_sasaran,
                "elapseTimeFunctionOngoingRingkasan": te_ringkasan_ongoing,
                "elapseTimeFunctionSasaranRingkasan": te_ringkasan_sasaran
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 400