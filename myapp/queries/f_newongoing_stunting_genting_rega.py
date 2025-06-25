import psycopg2
import pandas as pd
from psycopg2 import sql, extras
from datetime import datetime, timedelta
from pandas.tseries.offsets import MonthEnd

schema_map = {
    9: "verval_babel",
    16: "verval_banten",
    7: "verval_bengkulu",
    28: "verval_gorontalo",
    21: "verval_kalteng",
    23: "verval_kaltim",
    36: "verval_kalut",
    10: "verval_kepri",
    8: "verval_lampung",
    30: "verval_maluku",
    31: "verval_malut",
    33: "verval_pabar",
    40: "verval_pabardaya",
    32: "verval_papua",
    29: "verval_sulbar",
    26: "verval_sulsel",
    25: "verval_sulteng",
    27: "verval_sultra",
    6: "verval_sumsel",
    2: "verval_sumut"
}

async def calculate_v_tanggal(v_tahun, v_bulan):
    v_tahun = int(v_tahun)
    v_bulan = int(v_bulan)
    
    input_date_str = f"{v_tahun}{v_bulan:02d}"  
    current_date_str = datetime.now().strftime("%Y%m")

    if input_date_str == current_date_str:
        v_tanggal = datetime.now()
    else:
        if v_bulan == 12:
            next_month = datetime(v_tahun + 1, 1, 1)
        else:
            next_month = datetime(v_tahun, v_bulan + 1, 1)
        v_tanggal = next_month - timedelta(days=1)
    return v_tanggal


async def stunting_genting_rega(params):
    conn = psycopg2.connect(
        dbname="volt_verval2024",
        user="dev_siga",
        password="devsiga11s",
        host="103.225.242.119",
        port="5435"
    )

    cursor = conn.cursor(cursor_factory=extras.DictCursor)
    
    # if 'v_id_provinsi' in params and 'id_provinsi' not in params:
    #     params['id_provinsi'] = params['v_id_provinsi']

    try:
        v_id_propinsi_raw = params.get("v_id_propinsi")
        print("Raw v_id_propinsi:", v_id_propinsi_raw)
        v_id_propinsi = int(v_id_propinsi_raw) if v_id_propinsi_raw else None
    except (ValueError, TypeError):
         v_id_propinsi = None
    # v_id_propinsi = int(params.get("v_id_propinsi")) if params.get("v_id_propinsi") else None
    schema = schema_map.get(v_id_propinsi)
    print("Schema resolved:", schema)
    
    if not schema:
        raise ValueError(f"Schema tidak ditemukan untuk id_provinsi = {v_id_propinsi}")

    # v_tahun = params['v_tahun']
    # v_bulan = params['v_bulan']
    
    v_tahun = int(params.get("v_tahun")) if params.get("v_tahun") else None
    v_bulan = int(params.get("v_bulan")) if params.get("v_bulan") else None

    if v_tahun is None or v_bulan is None:
        v_tanggal = datetime(2024, 5, 31)
    else:
        v_tanggal = (pd.Timestamp(year=v_tahun, month=v_bulan, day=1) + MonthEnd(1)).to_pydatetime()

    v_tanggal = await calculate_v_tanggal(v_tahun, v_bulan)
    params['v_tanggal'] = v_tanggal.strftime("%Y-%m-%d %H:%M:%S")


    v_bulan = params.get('v_bulan')
    v_tahun = params.get('v_tahun')
    v_nik = params.get('v_nik')
    v_nama = params.get('v_nama')
    v_id_propinsi = params.get('v_id_propinsi')
    v_id_kabupaten = params.get('v_id_kabupaten')
    v_id_kecamatan = params.get('v_id_kecamatan')
    v_id_kelurahan = params.get('v_id_kelurahan')
    v_id_rw = params.get('v_id_rw')
    v_id_rt = params.get('v_id_rt')
    v_balita = params.get('v_balita')
    v_baduta = params.get('v_baduta')
    v_status_hamil = params.get('v_status_hamil')
    v_status_pus = params.get('v_status_pus')
    v_status_verval = params.get('v_status_verval')
    v_status_krs = params.get('v_status_krs')
    v_nik_tidak_wajar = params.get('v_nik_tidak_wajar')
    v_status_keluarga = params.get('v_status_keluarga')
    v_kesejahteraan_prioritas = params.get('v_kesejahteraan_prioritas')
    v_flag_genting = params.get('v_flag_genting')
    v_sasaran_genting = params.get('v_sasaran_genting')
    v_entry_genting = params.get('v_entry_genting')
    v_sudah_diukur = params.get('v_sudah_diukur')
    v_status_pengukuran = params.get('v_status_pengukuran')
    v_offset = params.get('v_offset')
    v_limit = params.get('v_limit')


    query = sql.SQL("""
    select a.kki, a.nik, a.nama, a.status_pus, a.status_hamil, a.kesertaan_kb_modern, a.id_provinsi, a.id_kabupaten, a.id_kecamatan, a.id_kelurahan, a.id_rw, a.id_rt, a.sumber_air_minum, a.memiliki_tempat_bab, a.status_keluarga, a.kesejahteraan_prioritas, a.pendampingan_tpk, a.terlalu_muda, a.terlalu_tua, a.terlalu_dekat, a.terlalu_banyak, a.status_verval, a.tanggal_verval, a.bulan_rekap, a.tahun_rekap, a.nama_istri, a.balita, a.baduta, a.kondisi_fasilitas_bab, a.kondisi_sumber_air_minum, a.pus_hamil, a.resiko_stunting, a.pus_kb_modern, a.pendampingan_tpk_rujukan, a.pendampingan_tpk_bansos, a.pendampingan_tpk_kie, a.pendampingan_tpk_elsimil, a.pendampingan_tpk_eppgbm, a.pendampingan_tpk_baas, a.pendampingan_tpk_pmt, a.pendampingan_tpk_tidak_ada, a.latitude, a.longitude, a.audit_trail, a.status_draft, a.nik_istri, a.usia_kehamilan, a.keterangan, a.foto_rumah, a.foto_jamban, a.tanggal_capture, a.individu_akan_menikah, a.nik_tidak_wajar, a.flag_posyandu, a.sasaran_genting, a.dapat_bansos_genting, a.mitra_genting_bumn_nn1, a.mitra_genting_bumn_nn2, a.mitra_genting_bumn_nn3, a.mitra_genting_bumn_nn4, a.mitra_genting_bumn_nn5, a.ket_mitra_genting_bumn, a.mitra_genting_swasta_nn1, a.mitra_genting_swasta_nn2, a.mitra_genting_swasta_nn3, a.mitra_genting_swasta_nn4, a.mitra_genting_swasta_nn5, a.ket_mitra_genting_swasta, a.mitra_genting_akademisi_nn1, a.mitra_genting_akademisi_nn2, a.mitra_genting_akademisi_nn3, a.mitra_genting_akademisi_nn4, a.mitra_genting_akademisi_nn5, a.ket_mitra_genting_akademisi, a.mitra_genting_lms_nn1, a.mitra_genting_lms_nn2, a.mitra_genting_lms_nn3, a.mitra_genting_lms_nn4, a.mitra_genting_lms_nn5, a.ket_mitra_genting_lms, a.mitra_genting_media_nn1, a.mitra_genting_media_nn2, a.mitra_genting_media_nn3, a.mitra_genting_media_nn4, a.mitra_genting_media_nn5, a.ket_mitra_genting_media, a.mitra_genting_perorangan_nn1, a.mitra_genting_perorangan_nn2, a.mitra_genting_perorangan_nn3, a.mitra_genting_perorangan_nn4, a.mitra_genting_perorangan_nn5, a.ket_mitra_genting_perorangan, a.id_stunting, a.entry_genting, a.sudah_diukur, a.tanggal_kunjungan, a.status_pengukuran, a.sts_paud, a.id_frm, a.no_kk, a.jarak_sam, a.memiliki_aset, a.jns_atap, a.kondisi_atap, a.jns_dinding, a.kondisi_dinding, a.jns_lantai, a.kondisi_lantai, a.sumber_penerangan, a.daya_penerangan, a.jml_orang_tinggal, a.bahan_bakar_masak, a.kepemilikan_bangunan, a.pendampingan_tpk_genting, a.jenis_bantuan, a.ket_mitra_genting_lainnya, a.mitra_genting_lainnya_nn1, a.mitra_genting_lainnya_nn2, a.mitra_genting_lainnya_nn3, a.mitra_genting_lainnya_nn4, a.mitra_genting_lainnya_nn5, a.luas_rumah
	from (
		select distinct a.kki::text AS kki,
	        LEFT(public.voltaccess(a.nik_kk, 'numeric'), 16)::text AS nik,
	        LEFT(public.voltaccess(a.nama_kk, 'alphanumericv2'), 200)::text AS nama,
	        a.status_pus,
	        (case when a.status_hamil = true and ((extract(days from ({v_tanggal} - a.updated_date)) / 7)::int + coalesce(a.usia_kehamilan,0)::int) <= 40 then a.status_hamil else false end)::boolean as status_hamil,
			a.kesertaan_kb_modern::text as kesertaan_kb_modern,
	        a.id_provinsi,
	        a.id_kabupaten,
	        a.id_kecamatan,
	        a.id_kelurahan,
	        a.id_rw,
	        a.id_rt,
			a.sumber_air_minum::varchar as sumber_air_minum,
			a.memiliki_tempat_bab::varchar as memiliki_tempat_bab,
			a.status_keluarga::varchar as status_keluarga,
			a.kesejahteraan_prioritas::varchar as kesejahteraan_prioritas,
			a.pendampingan_tpk::varchar as pendampingan_tpk,
			a.terlalu_muda,
			a.terlalu_tua,
			a.terlalu_dekat,
			a.terlalu_banyak,
	        a.status_verval,
	        a.tanggal_verval,
	        a.bulan_rekap,
	        a.tahun_rekap,
	        LEFT(public.voltaccess(a.nama_istri, 'alphanumericv2'), 200)::text as nama_istri,
	        coalesce(dtl.balita,2) as balita,
	        coalesce(dtl.baduta,2) as baduta,
	        a.kondisi_fasilitas_bab,
	        a.kondisi_sumber_air_minum,
	        a.pus_hamil,
			a.resiko_stunting,
			a.pus_kb_modern,
			a.pendampingan_tpk_rujukan,
			a.pendampingan_tpk_bansos,
			a.pendampingan_tpk_kie,
			a.pendampingan_tpk_elsimil,
			a.pendampingan_tpk_eppgbm,
			a.pendampingan_tpk_baas,
			a.pendampingan_tpk_pmt,
			a.pendampingan_tpk_tidak_ada,
			a.latitude,
			a.longitude,
			a.audit_trail,
			a.status_draft,
			LEFT(public.voltaccess(a.nik_istri, 'numeric'), 16)::text as nik_istri,
			a.usia_kehamilan,
			a.keterangan,
			a.foto_rumah,
			a.foto_jamban,
			a.tanggal_capture,
			a.individu_akan_menikah,
			a.nik_tidak_wajar,
			a.flag_posyandu,
			coalesce(b.sasaran_genting,
	            (case
		            when ((to_char(age({v_tanggal}, a.tanggal_lahir_anak_terakhir), 'YYYY'::text)::int < 5
		            		or (case when a.status_hamil = true and ((extract(days from ({v_tanggal} - a.updated_date)) / 7)::int + coalesce(a.usia_kehamilan,0)::int) <= 40 then a.status_hamil else false end)::boolean = true)
		            	and a.kesejahteraan_prioritas in (1,2,3)
		            	and (a.resiko_stunting = 1
		            		or (a.resiko_stunting is null
		            			and a.status_pus = 1
		            			and (a.kondisi_fasilitas_bab = 2 or a.kondisi_sumber_air_minum = 2)
		            			and (a.terlalu_banyak = 1 or a.terlalu_dekat = 1 or a.terlalu_muda = 1 or a.terlalu_tua = 1)
		            			and a.kesertaan_kb_modern in (0,9))
		            		or (a.resiko_stunting is null
		            			and a.status_pus = 2
		            			and (a.kondisi_fasilitas_bab = 2 or a.kondisi_sumber_air_minum = 2))
		            		)
		            	)
		            then 1
		            when ((to_char(age({v_tanggal}, a.tanggal_lahir_anak_terakhir), 'YYYY'::text)::int < 5
		            		or (case when a.status_hamil = true and ((extract(days from ({v_tanggal} - a.updated_date)) / 7)::int + coalesce(a.usia_kehamilan,0)::int) <= 40 then a.status_hamil else false end)::boolean = true)
		            	and a.kesejahteraan_prioritas in (1,2,3)
		            	and (a.resiko_stunting = 2
		            		or (a.resiko_stunting is null
		            			and a.status_pus = 1
		            			and (a.kondisi_fasilitas_bab = 1 or a.kondisi_sumber_air_minum = 1)
		            			and (a.terlalu_banyak = 2 or a.terlalu_dekat = 2 or a.terlalu_muda = 2 or a.terlalu_tua = 2)
		            			and a.kesertaan_kb_modern not in (0,9))
		            		or (a.resiko_stunting is null
		            			and a.status_pus = 2
		            			and (a.kondisi_fasilitas_bab = 1 or a.kondisi_sumber_air_minum = 1))
		            		)
		            	)
		            then 2
		            when ((to_char(age({v_tanggal}, a.tanggal_lahir_anak_terakhir), 'YYYY'::text)::int < 5
		            		or (case when a.status_hamil = true and ((extract(days from ({v_tanggal} - a.updated_date)) / 7)::int + coalesce(a.usia_kehamilan,0)::int) <= 40 then a.status_hamil else false end)::boolean = true)
		            	and (a.kesejahteraan_prioritas not in (1,2,3) or a.kesejahteraan_prioritas is null)
		            	and (a.resiko_stunting = 1
		            		or (a.resiko_stunting is null
		            			and a.status_pus = 1
		            			and (a.kondisi_fasilitas_bab = 2 or a.kondisi_sumber_air_minum = 2)
		            			and (a.terlalu_banyak = 1 or a.terlalu_dekat = 1 or a.terlalu_muda = 1 or a.terlalu_tua = 1)
		            			and a.kesertaan_kb_modern in (0,9))
		            		or (a.resiko_stunting is null
		            			and a.status_pus = 2
		            			and (a.kondisi_fasilitas_bab = 2 or a.kondisi_sumber_air_minum = 2))
		            		)
		            	)
		            then 3
		            when (to_char(age({v_tanggal}, a.tanggal_lahir_anak_terakhir), 'YYYY'::text)::int < 5
		            		or (case when a.status_hamil = true and ((extract(days from ({v_tanggal} - a.updated_date)) / 7)::int + coalesce(a.usia_kehamilan,0)::int) <= 40 then a.status_hamil else false end)::boolean = true)
		            	and dtl.individu_baru = 1
		            then 4
	            end)::int) as sasaran_genting,
			b.dapat_bansos_genting,
			b.mitra_genting_bumn_nn1,
			b.mitra_genting_bumn_nn2,
			b.mitra_genting_bumn_nn3,
			b.mitra_genting_bumn_nn4,
			b.mitra_genting_bumn_nn5,
			b.ket_mitra_genting_bumn,
			b.mitra_genting_swasta_nn1,
			b.mitra_genting_swasta_nn2,
			b.mitra_genting_swasta_nn3,
			b.mitra_genting_swasta_nn4,
			b.mitra_genting_swasta_nn5,
			b.ket_mitra_genting_swasta,
			b.mitra_genting_akademisi_nn1,
			b.mitra_genting_akademisi_nn2,
			b.mitra_genting_akademisi_nn3,
			b.mitra_genting_akademisi_nn4,
			b.mitra_genting_akademisi_nn5,
			b.ket_mitra_genting_akademisi,
			b.mitra_genting_lms_nn1,
			b.mitra_genting_lms_nn2,
			b.mitra_genting_lms_nn3,
			b.mitra_genting_lms_nn4,
			b.mitra_genting_lms_nn5,
			b.ket_mitra_genting_lms,
			b.mitra_genting_media_nn1,
			b.mitra_genting_media_nn2,
			b.mitra_genting_media_nn3,
			b.mitra_genting_media_nn4,
			b.mitra_genting_media_nn5,
			b.ket_mitra_genting_media,
			b.mitra_genting_perorangan_nn1,
			b.mitra_genting_perorangan_nn2,
			b.mitra_genting_perorangan_nn3,
			b.mitra_genting_perorangan_nn4,
			b.mitra_genting_perorangan_nn5,
			b.ket_mitra_genting_perorangan,
			b.id_stunting,
			(case when b.dapat_bansos_genting = 1 then 1 when b.dapat_bansos_genting = 2 then 0 end)::int as entry_genting,
			a.sudah_diukur,
			a.tanggal_kunjungan,
			a.status_pengukuran,
			a.tanggal_lahir_anak_terakhir,
			dtl.sts_paud,
			a.id_frm,
			a.no_kk,
			a.jarak_sam,
			a.memiliki_aset,
			a.jns_atap,
			a.kondisi_atap,
			a.jns_dinding,
			a.kondisi_dinding,
			a.jns_lantai,
			a.kondisi_lantai,
			a.sumber_penerangan,
			a.daya_penerangan,
			a.jml_orang_tinggal,
			a.bahan_bakar_masak,
			a.kepemilikan_bangunan,
			a.pendampingan_tpk_genting,
			b.jenis_bantuan,
			b.ket_mitra_genting_lainnya,
			b.mitra_genting_lainnya_nn1,
			b.mitra_genting_lainnya_nn2,
			b.mitra_genting_lainnya_nn3,
			b.mitra_genting_lainnya_nn4,
			b.mitra_genting_lainnya_nn5,
			a.luas_rumah
	    from {schema}.stunting_head a
	    left join (select * from {schema}.stunting_genting b
		    where b.jenis_bantuan = 1
		    and b.id_provinsi = {v_id_propinsi}
		    and b.id_kabupaten = {v_id_kabupaten}
		    and b.id_kecamatan = {v_id_kecamatan}
		    and b.id_kelurahan = {v_id_kelurahan}
		    and b.id_rw = coalesce({v_id_rw}, b.id_rw)
			and (({v_id_rt} is not null and b.id_rt::int in (select unnest(string_to_array({v_id_rt}, ','))::int))
			or ({v_id_rt} is null and b.id_rt::text = coalesce({v_id_rt}::text, b.id_rt::text)))
	        and b.tahun_genting = {v_tahun} and b.bulan_genting = {v_bulan}
		) b on a.id_stunting = b.id_stunting
	    left join (select b.id_stunting,
				max(case when to_char(age({v_tanggal}, b.tanggal_lahir), 'YYYY')::integer < 2 then 1 end) as baduta,
				max(case when to_char(age({v_tanggal}, b.tanggal_lahir), 'YYYY')::integer between 2 and 4 then 1 end) as balita,
				max(case when b.individu_baru = true then 1 end)::int as individu_baru,
				b.sts_paud
	    	from {schema}.stunting_dtl b
	    	where b.id_provinsi = {v_id_propinsi}
		    and b.id_kabupaten = {v_id_kabupaten}
		    and b.id_kecamatan = {v_id_kecamatan}
		    and b.id_kelurahan = {v_id_kelurahan}
		    and b.id_rw = coalesce({v_id_rw}, b.id_rw)
			and (({v_id_rt} is not null and b.id_rt::int in (select unnest(string_to_array({v_id_rt}, ','))::int))
			or ({v_id_rt} is null and b.id_rt::text = coalesce({v_id_rt}::text, b.id_rt::text)))
			group by b.id_stunting, b.sts_paud
		) dtl on a.id_stunting = dtl.id_stunting
	    where a.id_provinsi = {v_id_propinsi}
	    and a.id_kabupaten = {v_id_kabupaten}
	    and a.id_kecamatan = {v_id_kecamatan}
	    and a.id_kelurahan = {v_id_kelurahan}
	    and a.id_rw = coalesce({v_id_rw}, a.id_rw)
		and (({v_id_rt} is not null and a.id_rt::int in (select unnest(string_to_array({v_id_rt}, ','))::int))
		or ({v_id_rt} is null and a.id_rt::text = coalesce({v_id_rt}::text, a.id_rt::text)))
		and coalesce(a.status_keluarga::int,1) in (1,6)
	) a
    where a.sasaran_genting in (1,2,3,4)
    and (a.nik like '%'||coalesce({v_nik}, a.nik)||'%'
    	or a.nik_istri like '%'||coalesce({v_nik}, a.nik_istri)||'%')
    and (a.nama like '%'||coalesce({v_nama}, a.nama)||'%'
    	or a.nama_istri like '%'||coalesce({v_nama}, a.nama_istri)||'%')
    and (a.tahun_rekap::text || lpad(a.bulan_rekap::text,2,'0'))::int <= ({v_tahun}::text || lpad({v_bulan}::text,2,'0'))::int
	and coalesce(a.status_pus::text, '-') = coalesce({v_status_pus}::text, coalesce(a.status_pus::text, '-'))
	and coalesce(a.status_hamil::text, 'false') = coalesce({v_status_hamil}::text, coalesce(a.status_hamil::text, 'false'))
	and coalesce(a.baduta::text, '-') = coalesce({v_baduta}::text, coalesce(a.baduta::text, '-'))
	and coalesce(a.balita::text, '-') = coalesce({v_balita}::text, coalesce(a.balita::text, '-'))
	and coalesce(a.status_verval::text, '-') = coalesce({v_status_verval}::text, coalesce(a.status_verval::text, '-'))
	and coalesce(a.resiko_stunting::text, '-') = coalesce({v_status_krs}::text, coalesce(a.resiko_stunting::text, '-'))
	and coalesce(a.nik_tidak_wajar::text, '-') = coalesce({v_nik_tidak_wajar}::text, coalesce(a.nik_tidak_wajar::text, '-'))
	and (({v_status_keluarga} is not null and a.status_keluarga::int in (select unnest(string_to_array({v_status_keluarga}, ','))::int))
	or ({v_status_keluarga} is null and coalesce(a.status_keluarga::text, '-') = coalesce({v_status_keluarga}::text, coalesce(a.status_keluarga::text, '-'))))
	and (({v_kesejahteraan_prioritas} is not null and a.kesejahteraan_prioritas::int in (select unnest(string_to_array({v_kesejahteraan_prioritas}, ','))::int))
	or ({v_kesejahteraan_prioritas} is null and coalesce(a.kesejahteraan_prioritas::text, '-') = coalesce({v_kesejahteraan_prioritas}::text, coalesce(a.kesejahteraan_prioritas::text, '-'))))
	and coalesce((case when (to_char(age({v_tanggal}, a.tanggal_lahir_anak_terakhir), 'YYYY'::text)::int < 5 or a.status_hamil = true) and a.sasaran_genting is not null then 1 else 2 end)::text, '-') = coalesce({v_flag_genting}::text, coalesce((case when (to_char(age({v_tanggal}, a.tanggal_lahir_anak_terakhir), 'YYYY'::text)::int < 5 or a.status_hamil = true) and a.sasaran_genting is not null then 1 else 2 end)::text, '-'))
	and (({v_sasaran_genting} is not null and a.sasaran_genting::int in (select unnest(string_to_array({v_sasaran_genting}, ','))::int))
	or ({v_sasaran_genting} is null and coalesce(a.sasaran_genting::text, '-') = coalesce({v_sasaran_genting}::text, coalesce(a.sasaran_genting::text, '-'))))
	and coalesce(a.entry_genting::text, '-') = coalesce({v_entry_genting}::text, coalesce(a.entry_genting::text, '-'))
	and coalesce(a.sudah_diukur::text, '-') = coalesce({v_sudah_diukur}::text, coalesce(a.sudah_diukur::text, '-'))
	and coalesce(a.status_pengukuran::text, '-') = coalesce({v_status_pengukuran}::text, coalesce(a.status_pengukuran::text, '-'))
	order by kki
	offset {v_offset}
	limit {v_limit}
    """).format(
        schema=sql.Identifier(schema),
		v_tanggal=sql.Literal(params['v_tanggal']),
		v_bulan=sql.Literal(params['v_bulan']),
		v_tahun=sql.Literal(params['v_tahun']),
		v_nik=sql.Literal(params['v_nik']),
		v_nama=sql.Literal(params['v_nama']),
		v_id_propinsi=sql.Literal(params['v_id_propinsi']),
		v_id_kabupaten=sql.Literal(params['v_id_kabupaten']),
		v_id_kecamatan=sql.Literal(params['v_id_kecamatan']),
		v_id_kelurahan=sql.Literal(params['v_id_kelurahan']),
		v_id_rw=sql.Literal(params['v_id_rw']),
		v_id_rt=sql.Literal(params['v_id_rt']),
		v_balita=sql.Literal(params['v_balita']),
		v_baduta=sql.Literal(params['v_baduta']),
		v_status_hamil=sql.Literal(params['v_status_hamil']),
		v_status_pus=sql.Literal(params['v_status_pus']),
		v_status_verval=sql.Literal(params['v_status_verval']),
		v_status_krs=sql.Literal(params['v_status_krs']),
		v_nik_tidak_wajar=sql.Literal(params['v_nik_tidak_wajar']),
		v_status_keluarga=sql.Literal(params['v_status_keluarga']),
		v_kesejahteraan_prioritas=sql.Literal(params['v_kesejahteraan_prioritas']),
		v_flag_genting=sql.Literal(params['v_flag_genting']),
		v_sasaran_genting=sql.Literal(params['v_sasaran_genting']),
		v_entry_genting=sql.Literal(params['v_entry_genting']),
		v_sudah_diukur=sql.Literal(params['v_sudah_diukur']),
		v_status_pengukuran=sql.Literal(params['v_status_pengukuran']),
		v_offset=sql.Literal(params['v_offset']),
    	v_limit=sql.Literal(params['v_limit'])
	)

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results