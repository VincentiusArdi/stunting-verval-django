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


async def stunting_dtl_rega(params):
    conn = psycopg2.connect(
        dbname="volt_verval2024",
        user="dev_siga",
        password="devsiga11s",
        host="103.225.242.119",
        port="5435"
    )

    cursor = conn.cursor(cursor_factory=extras.DictCursor)
    
    v_id_provinsi = int(params.get("v_id_provinsi"))
    schema = schema_map.get(v_id_provinsi)
    if not schema:
        raise ValueError(f"Schema tidak ditemukan untuk id_provinsi = {v_id_provinsi}")

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
    v_nomor_keluarga = params.get('v_nomor_keluarga')
    v_nik_tidak_wajar = params.get('v_nik_tidak_wajar')


    query = sql.SQL("""
        select b.kki, b.nik, b.nama, b.hubungan_dengan_kk, b.tanggal_lahir, b.usia, b.usia_bulan, b.kode_ibu_kandung, b.jenis_kelamin, b.bulan_rekap, b.tahun_rekap, b.id_provinsi, b.id_kabupaten, b.id_kecamatan, b.id_kelurahan, b.id_rw, b.id_rt, b.foto_rumah, b.foto_jamban, b.individu_baru, b.sts_paud,
		case when b.nik similar to '%[^0-9]%'
			or b.nik like '12345%' or b.nik like '00000%' or b.nik like '%00000' or b.nik like '010101%' or b.nik like '030303%' or b.nik like '090909%' or b.nik like '%66666' or b.nik like '%88888' or b.nik like '%55555' or b.nik like '%11111'
			or ((b.nik like '%99999' or b.nik like '99999%') and b.nik <> '9999999999999999')
			or b.nik in ('0000000000000000','1111111111111111','2222222222222222','3333333333333333','4444444444444444','5555555555555555','6666666666666666','7777777777777777','8888888888888888','1901089999999999')
			or length(b.nik) < 16
		then true else false end as nik_tidak_wajar,
		b.id_frm, b.sts_kawin, b.id_pekerjaan, b.status_pekerjaan, b.jns_pendidikan, b.pendampingan, b.disabilitas, b.mengurus_diri, b.bekerja_luar_negeri, b.jenis_bantuan, b.bansos_genting_nutrisi, b.ket_mitra_genting_nutrisi
		from (
			select a.kki
				,LEFT(public.voltaccess(b.nik, 'numeric'), 16)::varchar as nik
				,LEFT(public.voltaccess(b.nama, 'alphanumericv2'), 200)::varchar as nama
				,b.hubungan_dengan_kk
				,b.tanggal_lahir
				,b.usia
				,b.usia_bulan
				,b.kode_ibu_kandung
				,b.jenis_kelamin
				,a.bulan_rekap
				,a.tahun_rekap
				,a.id_provinsi
				,a.id_kabupaten
				,a.id_kecamatan
				,a.id_kelurahan
				,a.id_rw
				,a.id_rt
				,a.foto_rumah
				,a.foto_jamban
				,b.individu_baru
				,b.sts_paud
				,b.id_frm
				,b.sts_kawin
				,b.id_pekerjaan
				,b.status_pekerjaan
				,b.jns_pendidikan
				,b.pendampingan
				,b.disabilitas
				,b.mengurus_diri
				,b.bekerja_luar_negeri
				,c.jenis_bantuan
				,c.bansos_genting_nutrisi
				,c.ket_mitra_genting_nutrisi
			from {schema}.stunting_head a
			left join {schema}.stunting_dtl b on a.id_stunting = b.id_stunting
			left join (select * from {schema}.stunting_genting b
				where b.jenis_bantuan = 2
				and b.tahun_genting = {v_tahun} and b.bulan_genting = {v_bulan}
			) c on b.id_stunting = c.id_stunting and b.nik= c.nik and b.nama = c.nama
			where a.kki = {v_nomor_keluarga}
		) b
		where coalesce((case when b.nik similar to '%[^0-9]%'
				or b.nik like '12345%' or b.nik like '00000%' or b.nik like '%00000' or b.nik like '010101%' or b.nik like '030303%' or b.nik like '090909%' or b.nik like '%66666' or b.nik like '%88888' or b.nik like '%55555' or b.nik like '%11111'
				or ((b.nik like '%99999' or b.nik like '99999%') and b.nik <> '9999999999999999')
				or b.nik in ('0000000000000000','1111111111111111','2222222222222222','3333333333333333','4444444444444444','5555555555555555','6666666666666666','7777777777777777','8888888888888888','1901089999999999')
				or length(b.nik) < 16
			then true else false end)::text, '-')
			= coalesce({v_nik_tidak_wajar}::text, coalesce((case when b.nik similar to '%[^0-9]%'
				or b.nik like '12345%' or b.nik like '00000%' or b.nik like '%00000' or b.nik like '010101%' or b.nik like '030303%' or b.nik like '090909%' or b.nik like '%66666' or b.nik like '%88888' or b.nik like '%55555' or b.nik like '%11111'
				or ((b.nik like '%99999' or b.nik like '99999%') and b.nik <> '9999999999999999')
				or b.nik in ('0000000000000000','1111111111111111','2222222222222222','3333333333333333','4444444444444444','5555555555555555','6666666666666666','7777777777777777','8888888888888888','1901089999999999')
				or length(b.nik) < 16
			then true else false end)::text, '-'))
		order by b.hubungan_dengan_kk, b.tanggal_lahir
    """).format(
        schema=sql.Identifier(schema),
		v_tanggal=sql.Literal(params['v_tanggal']),
		v_bulan=sql.Literal(params['v_bulan']),
		v_tahun=sql.Literal(params['v_tahun']),
		v_nomor_keluarga=sql.Literal(params['v_nomor_keluarga']),
		v_nik_tidak_wajar=sql.Literal(params['v_nik_tidak_wajar'])
	)

    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results