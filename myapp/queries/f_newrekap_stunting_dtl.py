import psycopg2
import pandas as pd
from psycopg2 import sql, extras
from datetime import datetime, timedelta
from pandas.tseries.offsets import MonthEnd

provinsi_map = {
    12: "jabar",
    18: "ntb",
    11: "dki",
    13: "jateng",
    14: "diy",
    17: "bali"
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


async def newrekap_stunting_dtl_vmp8(params):
    conn = psycopg2.connect(
        dbname="BKKBN",
        user="dev_siga",
        password="devsiga11s",
        host="103.225.242.241",
        port="5500"
    )

    cursor = conn.cursor(cursor_factory=extras.DictCursor)

    v_id_provinsi = int(params.get("v_id_provinsi"))
    schema = provinsi_map.get(v_id_provinsi)
    if not schema:
        raise ValueError(f"Provinsi tidak ditemukan untuk id_provinsi = {v_id_provinsi}")

    # v_tahun = params['v_tahun']
    # v_bulan = params['v_bulan']
    
    # v_tahun = int(params.get("v_tahun")) if params.get("v_tahun") else None
    # v_bulan = int(params.get("v_bulan")) if params.get("v_bulan") else None

    # if v_tahun is None or v_bulan is None:
    #     v_tanggal = datetime(2024, 5, 31)
    # else:
    #     v_tanggal = (pd.Timestamp(year=v_tahun, month=v_bulan, day=1) + MonthEnd(1)).to_pydatetime()

    # v_tanggal = await calculate_v_tanggal(v_tahun, v_bulan)
    # params['v_tanggal'] = v_tanggal

    v_nomor_keluarga = params.get('v_nomor_keluarga')
    v_nik_tidak_wajar = params.get('v_nik_tidak_wajar')


    query = sql.SQL("""
		SELECT pk.kki::varchar AS kki,
        pk.nik::varchar AS nik,
        pk.nama::varchar AS nama,
        (case when pk.hubungan_dengan_kk = 1 then 'KK' when pk.hubungan_dengan_kk = 2 then 'Istri' when pk.hubungan_dengan_kk = 3 then 'Anak' else 'Lainnya' end)::varchar as hubungan_dengan_kk,
        pk.tanggal_lahir::date as tanggal_lahir,
        pk.jenis_kelamin,
        null::int as kode_ibu_kandung,
        pk.nik_tidak_wajar,
        pk.sts_paud
        FROM 
         (select a.kki
			,a.nik
			,a.nama
			,a.hubungan_dengan_kk
			,a.tanggal_lahir
			,a.jenis_kelamin
--			,a.kode_ibu_kandung
			,case when a.nik similar to '%[^0-9]%'
				or a.nik like '12345%' or a.nik like '00000%' or a.nik like '%00000' or a.nik like '010101%' or a.nik like '030303%' or a.nik like '090909%' or a.nik like '%66666' or a.nik like '%88888' or a.nik like '%55555' or a.nik like '%11111'
				or ((a.nik like '%99999' or a.nik like '99999%') and a.nik <> '9999999999999999')
				or a.nik in ('0000000000000000','1111111111111111','2222222222222222','3333333333333333','4444444444444444','5555555555555555','6666666666666666','7777777777777777','8888888888888888','1901089999999999')
				or length(a.nik) < 16
			then true else false end as nik_tidak_wajar
			,a.sts_paud
     	from sigabaru.rekap_data_keluarga_dtl a
        where a.kki = {v_nomor_keluarga}
	 		and coalesce((case when a.nik similar to '%[^0-9]%'
				or a.nik like '12345%' or a.nik like '00000%' or a.nik like '%00000' or a.nik like '010101%' or a.nik like '030303%' or a.nik like '090909%' or a.nik like '%66666' or a.nik like '%88888' or a.nik like '%55555' or a.nik like '%11111'
				or ((a.nik like '%99999' or a.nik like '99999%') and a.nik <> '9999999999999999')
				or a.nik in ('0000000000000000','1111111111111111','2222222222222222','3333333333333333','4444444444444444','5555555555555555','6666666666666666','7777777777777777','8888888888888888','1901089999999999')
				or length(a.nik) < 16
			then true else false end)::text, '-') = coalesce({v_nik_tidak_wajar}::text, coalesce((case when a.nik similar to '%[^0-9]%'
				or a.nik like '12345%' or a.nik like '00000%' or a.nik like '%00000' or a.nik like '010101%' or a.nik like '030303%' or a.nik like '090909%' or a.nik like '%66666' or a.nik like '%88888' or a.nik like '%55555' or a.nik like '%11111'
				or ((a.nik like '%99999' or a.nik like '99999%') and a.nik <> '9999999999999999')
				or a.nik in ('0000000000000000','1111111111111111','2222222222222222','3333333333333333','4444444444444444','5555555555555555','6666666666666666','7777777777777777','8888888888888888','1901089999999999')
				or length(a.nik) < 16
			then true else false end)::text, '-'))
		  ) pk
		order by
		(case when pk.hubungan_dengan_kk = 1 then 1
			when pk.hubungan_dengan_kk = 2 then 2
			when pk.hubungan_dengan_kk = 3 then 3
			else 4 end),
		pk.tanggal_lahir
    """).format(
		# v_tanggal=sql.Literal(params['v_tanggal']),
		v_nomor_keluarga=sql.Literal(params['v_nomor_keluarga']),
		v_nik_tidak_wajar=sql.Literal(params['v_nik_tidak_wajar'])
	)

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results