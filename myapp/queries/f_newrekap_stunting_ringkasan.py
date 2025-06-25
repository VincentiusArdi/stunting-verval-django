import psycopg2
import pandas as pd
from psycopg2 import sql, extras
from datetime import datetime, timedelta
from pandas.tseries.offsets import MonthEnd

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


async def newrekap_stunting_ringkasan_vmp8(params):
    conn = psycopg2.connect(
        dbname="BKKBN",
        user="dev_siga",
        password="devsiga11s",
        host="103.225.242.241",
        port="5500"
    )

    cursor = conn.cursor(cursor_factory=extras.DictCursor)

    # v_tahun = params['v_tahun']
    # v_bulan = params['v_bulan']
    
    v_tahun = int(params.get("v_tahun")) if params.get("v_tahun") else None
    v_bulan = int(params.get("v_bulan")) if params.get("v_bulan") else None

    if v_tahun is None or v_bulan is None:
        v_tanggal = datetime(2024, 5, 31)
    else:
        v_tanggal = (pd.Timestamp(year=v_tahun, month=v_bulan, day=1) + MonthEnd(1)).to_pydatetime()

    v_tanggal = await calculate_v_tanggal(v_tahun, v_bulan)
    params['v_tanggal'] = v_tanggal


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
    v_sudah_diukur = params.get('v_sudah_diukur')
    v_status_pengukuran = params.get('v_status_pengukuran')


    query = sql.SQL("""
	select count(*)::int as jlh_row from (
		select distinct pk.kki::text as kki,
            pk.nik::text as nik,
            pk.nama::text as nama,
			COALESCE(COALESCE(pk.status_pus, pk.status_pus_manual), 2)::int as status_pus,
            (case when pk.status_hamil = true and ((EXTRACT(days FROM ({v_tanggal} - pk.updated_date)) / 7)::int + coalesce(pk.usia_kehamilan,0)::int) <= 40 then pk.status_hamil else false end)::boolean as status_hamil,
			pk.status_keluarga::varchar,
			pk.kesejahteraan_prioritas::varchar as kesejahteraan_prioritas,
            null::boolean as status_verval,
            (case when to_char(age({v_tanggal}, pk.balita), 'YYYY'::text)::integer between 2 and 4 then 1 else 2 end)::int as balita,
            (case when to_char(age({v_tanggal}, pk.baduta), 'YYYY'::text)::integer < 2 then 1 else 2 end)::int as baduta,
			(case when to_char(age({v_tanggal}, pk.baduta_balita), 'YYYY'::text)::integer < 5
				or COALESCE(COALESCE(pk.status_pus, pk.status_pus_manual), 2) = 1
            	or ((case when pk.status_hamil = true and ((EXTRACT(days FROM ({v_tanggal} - pk.updated_date)) / 7)::int + coalesce(pk.usia_kehamilan,0)::int) <= 40 then pk.status_hamil else false end)::boolean = true and COALESCE(COALESCE(pk.status_pus, pk.status_pus_manual), 2) = 1)
            then 1 else 2 end)::int as sasaran_krs,
            pk.nik_tidak_wajar,
            pk.sudah_diukur,
            pk.status_pengukuran,
--            case when to_char(age({v_tanggal}, pk.baduta_balita), 'YYYY'::text)::integer < 5 then 1 else 2 end as flag_genting,
            (case
	            when (to_char(age({v_tanggal}, pk.baduta_balita), 'YYYY'::text)::integer < 5
	            	and pk.kesejahteraan_prioritas in (1,2,3)
	            	and (pk.resiko_stunting = 1
	            		or (pk.resiko_stunting is null
	            			and COALESCE(COALESCE(pk.status_pus, pk.status_pus_manual), 2)::int = 1
	            			and (pk.kondisi_fasilitas_bab = 2 or pk.kondisi_sumber_air_minum = 2)
	            			and (pk.terlalu_banyak = 1 or pk.terlalu_dekat = 1 or pk.terlalu_muda = 1 or pk.terlalu_tua = 1)
	            			and COALESCE(pk.siga_metode_kontrasepsi, pk.metode_kontrasepsi) in ('BUKAN PESERTA KB', 'TRADISIONAL'))
	            		or (pk.resiko_stunting is null
	            			and COALESCE(COALESCE(pk.status_pus, pk.status_pus_manual), 2)::int = 2
	            			and (pk.kondisi_fasilitas_bab = 2 or pk.kondisi_sumber_air_minum = 2))
	            		)
	            	)
	            then 1
	            when (to_char(age({v_tanggal}, pk.baduta_balita), 'YYYY'::text)::integer < 5
	            	and pk.kesejahteraan_prioritas in (1,2,3)
	            	and (pk.resiko_stunting = 2
	            		or (pk.resiko_stunting is null
	            			and COALESCE(COALESCE(pk.status_pus, pk.status_pus_manual), 2)::int = 1
	            			and (pk.kondisi_fasilitas_bab = 1 or pk.kondisi_sumber_air_minum = 1)
	            			and (pk.terlalu_banyak = 2 or pk.terlalu_dekat = 2 or pk.terlalu_muda = 2 or pk.terlalu_tua = 2)
	            			and COALESCE(pk.siga_metode_kontrasepsi, pk.metode_kontrasepsi) not in ('BUKAN PESERTA KB', 'TRADISIONAL'))
	            		or (pk.resiko_stunting is null
	            			and COALESCE(COALESCE(pk.status_pus, pk.status_pus_manual), 2)::int = 2
	            			and (pk.kondisi_fasilitas_bab = 1 or pk.kondisi_sumber_air_minum = 1))
	            		)
	            	)
	            then 2
	            when (to_char(age({v_tanggal}, pk.baduta_balita), 'YYYY'::text)::integer < 5
	            	and (pk.kesejahteraan_prioritas not in (1,2,3) or pk.kesejahteraan_prioritas is null)
	            	and (pk.resiko_stunting = 1
	            		or (pk.resiko_stunting is null
	            			and COALESCE(COALESCE(pk.status_pus, pk.status_pus_manual), 2)::int = 1
	            			and (pk.kondisi_fasilitas_bab = 2 or pk.kondisi_sumber_air_minum = 2)
	            			and (pk.terlalu_banyak = 1 or pk.terlalu_dekat = 1 or pk.terlalu_muda = 1 or pk.terlalu_tua = 1)
	            			and COALESCE(pk.siga_metode_kontrasepsi, pk.metode_kontrasepsi) in ('BUKAN PESERTA KB', 'TRADISIONAL'))
	            		or (pk.resiko_stunting is null
	            			and COALESCE(COALESCE(pk.status_pus, pk.status_pus_manual), 2)::int = 2
	            			and (pk.kondisi_fasilitas_bab = 2 or pk.kondisi_sumber_air_minum = 2))
	            		)
	            	)
	            then 3
            end)::int as sasaran_genting,
            pk.sudah_diverval,
            pk.flag_genting
           FROM 
             (select a.kki
				,a.nik
				,a.nama
				,case when to_char(age({v_tanggal}, ibrl.tgl_lahir_istri), 'YYYY'::text)::int between 10 AND 49 then 1 else null end as status_pus
				,case when to_char(age({v_tanggal}, ibrl.tgl_lahir_manual), 'YYYY'::text)::int between 10 AND 49 THEN 1 else null end as status_pus_manual
				,a.status_hamil
				,a.usia_kehamilan
				,a.created_date
				,a.siga_ada_suami
				,a.updated_date
				,a.siga_created_date
				,ibrl.baduta_balita
				,case when a.status_keluarga = 6 and (a.created_date < '2025-06-16' or a.updated_date < '2025-06-16') then 1 else a.status_keluarga end as status_keluarga
				,a.kesejahteraan_prioritas
				,ibrl.baduta
				,ibrl.balita
				,case when ibrl.nik_tidak_wajar = 1 then true else false end as nik_tidak_wajar
				,lead(a.kki) over (partition by a.kki, a.hubungan_dengan_kk order by a.updated_date, a.created_date) as flag
				,a.sudah_diverval
				,case when a.metode_kontrasepsi = '0' then 'BUKAN PESERTA KB'
					when a.metode_kontrasepsi = '1' then 'MOW'
					when a.metode_kontrasepsi = '2' then 'MOP'
					when a.metode_kontrasepsi = '3' then 'IUD'
					when a.metode_kontrasepsi = '4' then 'IMPLANT'
					when a.metode_kontrasepsi = '5' then 'SUNTIKAN'
					when a.metode_kontrasepsi = '6' then 'PIL'
					when a.metode_kontrasepsi = '7' then 'KONDOM'
					when a.metode_kontrasepsi = '8' then 'MAL'
					when a.metode_kontrasepsi = '9' then 'TRADISIONAL'
					when a.metode_kontrasepsi = '99' then 'TIDAK BERLAKU'
				end as metode_kontrasepsi
				,case when a.siga_metode_kontrasepsi = '0' then 'BUKAN PESERTA KB'
					when a.siga_metode_kontrasepsi = '1' then 'MOW'
					when a.siga_metode_kontrasepsi = '2' then 'MOP'
					when a.siga_metode_kontrasepsi = '3' then 'IUD'
					when a.siga_metode_kontrasepsi = '4' then 'IMPLANT'
					when a.siga_metode_kontrasepsi = '5' then 'SUNTIKAN'
					when a.siga_metode_kontrasepsi = '6' then 'PIL'
					when a.siga_metode_kontrasepsi = '7' then 'KONDOM'
				end as siga_metode_kontrasepsi
				,a.resiko_stunting
				,(case when (a.memiliki_tempat_bab in (1,2) or a.memiliki_tempat_bab is null) then 1 when a.memiliki_tempat_bab in (3,4) then 2 end) as kondisi_fasilitas_bab
				,(case when (a.sumber_air_minum in (1,2,3,4,6) or a.sumber_air_minum is null) then 1 when a.sumber_air_minum in (5,7,8,9,10) then 2 end) as kondisi_sumber_air_minum
				,a.sudah_diukur
				,a.status_pengukuran
				,(case
					when to_char(age(date({v_tanggal}), ibrl.tgl_lahir_istri), 'YYYY'::text)::integer < 20 --between 15 and 19
						and coalesce(coalesce((case when to_char(age({v_tanggal}, ibrl.tgl_lahir_istri), 'YYYY'::text)::int between 10 AND 49 then 1 else null end), (case when to_char(age({v_tanggal}, ibrl.tgl_lahir_manual), 'YYYY'::text)::int between 10 AND 49 THEN 1 else null end)), 2) = 1
					then 1
						when to_char(age(date({v_tanggal}), ibrl.tgl_lahir_istri), 'YYYY'::text)::integer < 20
						and (case when a.status_hamil = true and ((extract(days from ({v_tanggal} - a.updated_date)) / 7)::int + coalesce(a.usia_kehamilan,0)::int) <= 40 then a.status_hamil else false end)::bool = true
					then 1
						when to_char(age(date({v_tanggal}), ibrl.tgl_lahir_istri), 'YYYY'::text)::integer >= 20
						and coalesce(coalesce((case when to_char(age({v_tanggal}, ibrl.tgl_lahir_istri), 'YYYY'::text)::int between 10 AND 49 then 1 else null end), (case when to_char(age({v_tanggal}, ibrl.tgl_lahir_manual), 'YYYY'::text)::int between 10 AND 49 THEN 1 else null end)), 2) = 1
					then 2
						when to_char(age(date({v_tanggal}), ibrl.tgl_lahir_istri), 'YYYY'::text)::integer >= 20
						and (case when a.status_hamil = true and ((extract(days from ({v_tanggal} - a.updated_date)) / 7)::int + coalesce(a.usia_kehamilan,0)::int) <= 40 then a.status_hamil else false end)::bool = true
					then 2
					else 3
				end)::int as terlalu_muda
				,(case
					when to_char(age(date({v_tanggal}), ibrl.tgl_lahir_istri), 'YYYY'::text)::integer between 35 and 40
						and coalesce(coalesce((case when to_char(age({v_tanggal}, ibrl.tgl_lahir_istri), 'YYYY'::text)::int between 10 AND 49 then 1 else null end), (case when to_char(age({v_tanggal}, ibrl.tgl_lahir_manual), 'YYYY'::text)::int between 10 AND 49 THEN 1 else null end)), 2) = 1
					then 1
						when to_char(age(date({v_tanggal}), ibrl.tgl_lahir_istri), 'YYYY'::text)::integer >= 35
						and (case when a.status_hamil = true and ((extract(days from ({v_tanggal} - a.updated_date)) / 7)::int + coalesce(a.usia_kehamilan,0)::int) <= 40 then a.status_hamil else false end)::bool = true
					then 1
						when (to_char(age(date({v_tanggal}), ibrl.tgl_lahir_istri), 'YYYY'::text)::integer < 35 or to_char(age(date({v_tanggal}), ibrl.tgl_lahir_istri), 'YYYY'::text)::integer > 40)
						and coalesce(coalesce((case when to_char(age({v_tanggal}, ibrl.tgl_lahir_istri), 'YYYY'::text)::int between 10 AND 49 then 1 else null end), (case when to_char(age({v_tanggal}, ibrl.tgl_lahir_manual), 'YYYY'::text)::int between 10 AND 49 THEN 1 else null end)), 2) = 1
					then 2
						when to_char(age(date({v_tanggal}), ibrl.tgl_lahir_istri), 'YYYY'::text)::integer < 35
						and (case when a.status_hamil = true and ((extract(days from ({v_tanggal} - a.updated_date)) / 7)::int + coalesce(a.usia_kehamilan,0)::int) <= 40 then a.status_hamil else false end)::bool = true
					then 2
					else 3
				end)::int as terlalu_tua
				,(case
					when ibrl.anak_2terakhir - ibrl.anak_terakhir < 2
					and coalesce(coalesce((case when to_char(age({v_tanggal}, ibrl.tgl_lahir_istri), 'YYYY'::text)::int between 10 AND 49 then 1 else null end), (case when to_char(age({v_tanggal}, ibrl.tgl_lahir_manual), 'YYYY'::text)::int between 10 AND 49 THEN 1 else null end)), 2) = 1
				then 1
					when ibrl.anak_2terakhir - ibrl.anak_terakhir >= 2
					and coalesce(coalesce((case when to_char(age({v_tanggal}, ibrl.tgl_lahir_istri), 'YYYY'::text)::int between 10 AND 49 then 1 else null end), (case when to_char(age({v_tanggal}, ibrl.tgl_lahir_manual), 'YYYY'::text)::int between 10 AND 49 THEN 1 else null end)), 2) = 1
				then 2
				else 3 end)::int as terlalu_dekat
				,(case
					when ibrl.jlh_anak >= 3
					and coalesce(coalesce((case when to_char(age({v_tanggal}, ibrl.tgl_lahir_istri), 'YYYY'::text)::int between 10 AND 49 then 1 else null end), (case when to_char(age({v_tanggal}, ibrl.tgl_lahir_manual), 'YYYY'::text)::int between 10 AND 49 THEN 1 else null end)), 2) = 1
				then 1
					when ibrl.jlh_anak < 3
					and coalesce(coalesce((case when to_char(age({v_tanggal}, ibrl.tgl_lahir_istri), 'YYYY'::text)::int between 10 AND 49 then 1 else null end), (case when to_char(age({v_tanggal}, ibrl.tgl_lahir_manual), 'YYYY'::text)::int between 10 AND 49 THEN 1 else null end)), 2) = 1
				then 2
				else 3 end)::int terlalu_banyak
				,a.flag_genting
            from (select x.*, y.nik, y.nama, y.hubungan_dengan_kk, y.tanggal_lahir, y.sts_kawin, y.jns_pendidikan, y.id_pekerjaan, y.jenis_kelamin, y.id_mutasi_individu, y.tgl_mutasi_individu, y.kode_ibu_kandung, y.sudah_menikah, y.flag_catin, y.flag_bumil, y.bumil_melahirkan, y.flag_pascasalin, y.flag_baduta
            	from sigabaru.rekap_data_keluarga_head x
            	inner join (select * from sigabaru.rekap_data_keluarga_dtl y
			        where y.id_provinsi = {v_id_propinsi}
					and y.id_kabupaten = {v_id_kabupaten}
					and y.id_kecamatan = {v_id_kecamatan}
					and y.id_kelurahan = coalesce({v_id_kelurahan}, y.id_kelurahan)
					and y.id_rw = coalesce({v_id_rw}, y.id_rw)
					and (({v_id_rt} is not null and y.id_rt::int in (select unnest(string_to_array({v_id_rt}, ','))::int))
					or ({v_id_rt} is null and y.id_rt::text = coalesce({v_id_rt}::text, y.id_rt::text)))
				) y on x.kki = y.kki
	            where x.id_provinsi = {v_id_propinsi}
				and x.id_kabupaten = {v_id_kabupaten}
				and x.id_kecamatan = {v_id_kecamatan}
				and x.id_kelurahan = coalesce({v_id_kelurahan}, x.id_kelurahan)
				and x.id_rw = coalesce({v_id_rw}, x.id_rw)
				and (({v_id_rt} is not null and x.id_rt::int in (select unnest(string_to_array({v_id_rt}, ','))::int))
				or ({v_id_rt} is null and x.id_rt::text = coalesce({v_id_rt}::text, x.id_rt::text)))
				and x.created_date <= '2025-06-04'
			) a
			left join (select bb.kki, sum(anak_terakhir) as anak_terakhir, sum(anak_2terakhir) as anak_2terakhir,
					max(bb.tgl_lahir_istri) as tgl_lahir_istri,
					max(bb.baduta_balita) as baduta_balita,
					max(bb.baduta) as baduta,
					max(bb.balita) as balita,
					count(case when bb.hubungan_dengan_kk = '3' then bb.kki end) as jlh_anak,
					max(bb.nama_istri) as nama_istri,
					max(bb.tgl_lahir_manual) as tgl_lahir_manual,
					max(bb.nik_tidak_wajar) as nik_tidak_wajar
				from (select a.kki, a.hubungan_dengan_kk, a.tanggal_lahir,
						max(case when a.hubungan_dengan_kk = '2' then a.tanggal_lahir end) as tgl_lahir_istri,
						max(case when to_char(age({v_tanggal}, a.tanggal_lahir), 'YYYY')::integer < 5 then a.tanggal_lahir end) as baduta_balita,
						max(case when to_char(age({v_tanggal}, a.tanggal_lahir), 'YYYY')::integer < 2 then a.tanggal_lahir end) as baduta,
						max(case when to_char(age({v_tanggal}, a.tanggal_lahir), 'YYYY')::integer between 2 and 4 then a.tanggal_lahir end) as balita,
						count(case when a.hubungan_dengan_kk = '3' then a.kki end) as jlh_anak,
						max(case when a.hubungan_dengan_kk = '2' then a.nama end) as nama_istri,
						max(coalesce((case when a.siga_ada_suami = 1 and a.kki like '%S%' and a.hubungan_dengan_kk = '2' then a.tanggal_lahir end), (case when a.siga_ada_suami = 1 and a.kki like '%S%' and a.hubungan_dengan_kk = '1' then a.tanggal_lahir end))) as tgl_lahir_manual,
						max(case when a.nik similar to '%[^0-9]%'
							or a.nik like '12345%' or a.nik like '00000%' or a.nik like '%00000' or a.nik like '010101%' or a.nik like '030303%' or a.nik like '090909%' or a.nik like '%66666' or a.nik like '%88888' or a.nik like '%55555' or a.nik like '%11111'
							or ((a.nik like '%99999' or a.nik like '99999%') and a.nik <> '9999999999999999')
							or a.nik in ('0000000000000000','1111111111111111','2222222222222222','3333333333333333','4444444444444444','5555555555555555','6666666666666666','7777777777777777','8888888888888888','1901089999999999')
							or length(a.nik) < 16
						then 1 end) as nik_tidak_wajar,
						case when rank() over (partition by a.kki, (a.hubungan_dengan_kk = '3') order by a.tanggal_lahir desc) = 1 and a.hubungan_dengan_kk = '3' and to_char(age(date({v_tanggal}), a.tanggal_lahir), 'YYYY')::integer < 5 then to_char(age(date({v_tanggal}), a.tanggal_lahir), 'YYYY')::integer end as anak_terakhir,
						case when rank() over (partition by a.kki, (a.hubungan_dengan_kk = '3') order by a.tanggal_lahir desc) = 2 and a.hubungan_dengan_kk = '3' then to_char(age(date({v_tanggal}), a.tanggal_lahir), 'YYYY')::integer end as anak_2terakhir
					from sigabaru.rekap_data_keluarga_dtl a
		            where a.id_provinsi = {v_id_propinsi}
					and a.id_kabupaten = {v_id_kabupaten}
					and a.id_kecamatan = {v_id_kecamatan}
					and a.id_kelurahan = coalesce({v_id_kelurahan}, a.id_kelurahan)
					and a.id_rw = coalesce({v_id_rw}, a.id_rw)
					and (({v_id_rt} is not null and a.id_rt::int in (select unnest(string_to_array({v_id_rt}, ','))::int))
					or ({v_id_rt} is null and a.id_rt::text = coalesce({v_id_rt}::text, a.id_rt::text)))
					group by a.kki, a.hubungan_dengan_kk, a.tanggal_lahir) bb
				group by bb.kki) ibrl
			on a.kki = ibrl.kki
            where ({v_nik} is null
			 	and a.id_provinsi = {v_id_propinsi}
			    and a.id_kabupaten = {v_id_kabupaten}
			    and a.id_kecamatan = {v_id_kecamatan}
			    and a.id_kelurahan = coalesce({v_id_kelurahan}, a.id_kelurahan)
			    and a.id_rw = coalesce({v_id_rw}, a.id_rw)
				and (({v_id_rt} is not null and a.id_rt::int in (select unnest(string_to_array({v_id_rt}, ','))::int))
				or ({v_id_rt} is null and a.id_rt::text = coalesce({v_id_rt}::text, a.id_rt::text)))
			    and upper(a.nama) like '%' || upper(coalesce({v_nama}, a.nama)) || '%'
				and a.hubungan_dengan_kk = '1'
			    )
			    or ({v_nik} is null
			    and upper(a.nama) like '%' || upper(coalesce({v_nama}, 'not found')) || '%'
			 	and a.id_provinsi = {v_id_propinsi}
			    and a.id_kabupaten = {v_id_kabupaten}
			    and a.id_kecamatan = {v_id_kecamatan}
			    and a.id_kelurahan = coalesce({v_id_kelurahan}, a.id_kelurahan)
			    and a.id_rw = coalesce({v_id_rw}, a.id_rw)
				and (({v_id_rt} is not null and a.id_rt::int in (select unnest(string_to_array({v_id_rt}, ','))::int))
				or ({v_id_rt} is null and a.id_rt::text = coalesce({v_id_rt}::text, a.id_rt::text)))
				and a.hubungan_dengan_kk <> '1'
			    )
			    or (a.nik like '%' || coalesce({v_nik}, 'not found') || '%'
			 	and a.id_provinsi = {v_id_propinsi}
			    and a.id_kabupaten = {v_id_kabupaten}
			    and a.id_kecamatan = {v_id_kecamatan}
			    and a.id_kelurahan = coalesce({v_id_kelurahan}, a.id_kelurahan)
			    and a.id_rw = coalesce({v_id_rw}, a.id_rw)
				and (({v_id_rt} is not null and a.id_rt::int in (select unnest(string_to_array({v_id_rt}, ','))::int))
				or ({v_id_rt} is null and a.id_rt::text = coalesce({v_id_rt}::text, a.id_rt::text)))
			    )
			) pk
		where to_char(pk.created_date, 'YYYYMM') <= concat({v_tahun}::varchar, lpad({v_bulan}::varchar,2,'0'))
		and pk.flag is null
		) src
	where src.sudah_diverval is null
	and src.sasaran_krs = coalesce({v_status_krs}, src.sasaran_krs)
	and coalesce((case when (src.baduta = 1 or src.balita = 1 or src.status_hamil = true) and src.sasaran_genting is not null and coalesce(src.status_keluarga::int,1) in (1,6) then 1 else 2 end)::text, '-') = coalesce({v_flag_genting}::text, coalesce((case when (src.baduta = 1 or src.balita = 1 or src.status_hamil = true) and src.sasaran_genting is not null and coalesce(src.status_keluarga::int,1) in (1,6) then 1 else 2 end)::text, '-'))
	and coalesce(src.status_pus::text, '-') = coalesce({v_status_pus}::text, coalesce(src.status_pus::text, '-'))
	and coalesce(src.status_hamil::text, 'false') = coalesce({v_status_hamil}::text, coalesce(src.status_hamil::text, 'false'))
	and coalesce(src.baduta::text, '-') = coalesce({v_baduta}::text, coalesce(src.baduta::text, '-'))
	and coalesce(src.balita::text, '-') = coalesce({v_balita}::text, coalesce(src.balita::text, '-'))
	and coalesce(src.status_keluarga::text, '-') = coalesce({v_status_keluarga}::text, coalesce(src.status_keluarga::text, '-'))
	and coalesce(src.nik_tidak_wajar::text, '-') = coalesce({v_nik_tidak_wajar}::text, coalesce(src.nik_tidak_wajar::text, '-'))
	and (({v_kesejahteraan_prioritas} is not null and src.kesejahteraan_prioritas::int in (select unnest(string_to_array({v_kesejahteraan_prioritas}, ','))::int))
	or ({v_kesejahteraan_prioritas} is null and coalesce(src.kesejahteraan_prioritas::text, '-') = coalesce({v_kesejahteraan_prioritas}::text, coalesce(src.kesejahteraan_prioritas::text, '-'))))
	and coalesce(src.sudah_diukur::text, '-') = coalesce({v_sudah_diukur}::text, coalesce(src.sudah_diukur::text, '-'))
	and coalesce(src.status_pengukuran::text, '-') = coalesce({v_status_pengukuran}::text, coalesce(src.status_pengukuran::text, '-'))
    """).format(
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
		v_sudah_diukur=sql.Literal(params['v_sudah_diukur']),
		v_status_pengukuran=sql.Literal(params['v_status_pengukuran'])
	)

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results