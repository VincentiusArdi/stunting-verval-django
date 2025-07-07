import psycopg2

def voltageDecrypt(v_id_provinsi, chipertext, method):

    v_id_provinsi = int(v_id_provinsi)

    connA = psycopg2.connect(
        dbname="volt_verval2024",
        user="dev_siga",
        password="devsiga11s",
        host="103.225.242.119",
        port="5435"
    )

    connB = psycopg2.connect(
        dbname="volt_verval2024",
        user="dev_siga",
        password="devsiga11s",
        host="103.225.242.100",
        port="5435"
    )

    connC = psycopg2.connect(
        dbname="volt_verval2024",
        user="dev_siga",
        password="devsiga11s",
        host="103.225.242.99",
        port="5435"
    )

    connD = psycopg2.connect(
        dbname="volt_verval2024",
        user="dev_siga",
        password="devsiga11s",
        host="103.225.242.118",
        port="5435"
    )

    if v_id_provinsi in {11, 13, 14, 17}:
        connection = connC
    elif v_id_provinsi in {12, 18}:
        connection = connB
    elif v_id_provinsi in {9, 16, 7, 28, 21, 23, 36, 10, 8, 30, 31, 33, 40, 32, 29, 26, 25, 27, 6, 2}:
       connection = connA
    elif v_id_provinsi in {1, 5, 15, 20, 22, 19, 39, 37, 38, 4, 24, 3}:
        connection = connD
    else:
        return {"error": f"Schema on going tidak ditemukan untuk id_provinsi = {v_id_provinsi}"}, 400
    

    try:
        with connection.cursor() as cur:
                cur.execute("SELECT voltaccess(%s, %s)", (chipertext, method))
                result = cur.fetchone()
                plaintext = result[0] if result else None
                print("decrypt :" , plaintext)
                cur.close()
                return plaintext
    except Exception as e:
            return str(e), 500