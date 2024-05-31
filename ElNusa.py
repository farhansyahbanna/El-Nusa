import psycopg2
import os
import sys
from decimal import Decimal
from datetime import datetime

def connect_database():
    conn = psycopg2.connect(database='RentalMobil', user='postgres', password='farhan123', host='localhost', port='5432')
    return conn

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def click_enter_penyewa(username, password):
    print("\n")
    kembali = input("Tekan Enter untuk melanjutkan ke Menu...")
    print(kembali) 
    homepage_penyewa(username, password)


def pilihan():
    

    tampilan='''
    |===========================================================================|
    |          SILAHKAN REGISTER ATAU LOGIN TERLEBIH DAHULU                     |
    |          1. Register                                                      |
    |          2. Login                                                         |
    |                                                                           |
    |===========================================================================|
    '''
    print (tampilan)
    while True:
        inputan = input("Pilihan >")
        if inputan == "1":
            register_penyewa()
            
        elif inputan == "2":
            login_penyewa()

def register_penyewa():

    # Memasukkan data penyewa ke tabel `penyewa`
    nama_penyewa = input("Masukkan nama lengkap: ")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    no_telepon_penyewa = input("Masukkan No Telepon: ")
    alamat_penyewa = input("Masukkan Alamat: ")
    nik_ktp_penyewa= input("Masukkan NIK KTP: ")

    conn = connect_database()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO penyewa (nama_penyewa, username, password,no_telepon_penyewa, alamat_penyewa, nik_ktp_penyewa) VALUES (%s, %s, %s, %s, %s, %s)",
            (nama_penyewa, username, password, no_telepon_penyewa, alamat_penyewa, nik_ktp_penyewa)
        )
        conn.commit()
        print("Penyewa berhasil didaftarkan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def login_penyewa():
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    conn = connect_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM penyewa WHERE username = %s AND password = %s", (username, password))
        penyewa = cur.fetchone()

        if penyewa:
            print("Login berhasil!")
            print("Selamat datang, ", penyewa[1])
            click_enter_penyewa(username, password)
            
        else:
            print("Login gagal. Username atau password salah.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cur.close()
        conn.close()

def homepage_penyewa(username, password):
    
    clear_screen()

    print('='*70)
    print(f"{'SELAMAT DATANG DI EL NUSA TOUR':^70} \n {'RENTAL MOBIL TERPERCAYA ':^70}")
    print('='*70)

    print(" [1]. LIHAT PROFIL \n [2]. SEWA MOBIL \n [3]. PEMBAYARAN \n [4]. PENGEMBALIAN \n\n [0]. KELUAR")
    print('='*70)
    opsi = (input("Pilih Opsi yang ingin digunakan: "))
    while(True):
        if opsi == '1':
            profil_penyewa(username, password)      
        elif opsi == '2':
            sewa_mobil(username, password)
        elif opsi == '3':
            pembayaran(username, password)
        elif opsi == '4':
            pengembalian(username, password)
        elif opsi == '0':
            homepage_penyewa(username, password)

def profil_penyewa(username, password):
    conn = connect_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM penyewa WHERE username = %s", (username,))
        penyewa = cur.fetchone()

        if penyewa:
            print('='*70)
            print(f"{'PROFIL ANDA':^70}")
            print('='*70)
            print(f"ID User \t: {penyewa[0]}")
            print(f"Nama Penyewa \t: {penyewa[1]}")
            print(f"Username \t: {penyewa[2]}")
            print(f"No Telepon \t: {penyewa[4]}")
            print(f"Alamat \t\t: {penyewa[5]}")
            print('='*70)
            
            print("[1]. EDIT PROFIL \n[2]. KEMBALI")

            while True:
                pilihan = int(input("Pilihan >"))
                clear_screen()

                if pilihan == 1:
                    print(" [1]. EDIT NAMA \n [2]. EDIT USERNAME & PASSWORD \n [3]. EDIT ALAMAT ")
                    pilihan_edit = int(input("Pilihan >"))

                    if pilihan_edit == 1:
                        edit_nama_penyewa = input("Edit nama lengkap: ")

                        conn = connect_database()
                        cur = conn.cursor()
                        try:
                            cur.execute(
                               "UPDATE penyewa SET nama_penyewa = %s WHERE username = %s", (edit_nama_penyewa, username)
                            )
                            conn.commit()
                            print("Nama Penyewa berhasil diedit.")
                            click_enter_penyewa(username, password)
                        except Exception as e:
                            print(f"Terjadi kesalahan: {e}")
                            conn.rollback()
                        finally:
                            cur.close()
                            conn.close()
                    
                    elif pilihan_edit == 2:
                        edit_username = input("Edit Username: ")
                        edit_password = input("Edit Password")

                        conn = connect_database()
                        cur = conn.cursor()
                        try:
                            cur.execute(
                               "UPDATE penyewa SET username = %s, password = %s WHERE username = %s", (edit_username, edit_password, username)
                            )
                            conn.commit()
                            print("Username dan Password berhasil diedit.")
                            click_enter_penyewa(username, password)
                        except Exception as e:
                            print(f"Terjadi kesalahan: {e}")
                            conn.rollback()
                        finally:
                            cur.close()
                            conn.close()
                    
                    elif pilihan_edit == 3:
                        edit_alamat = input("Edit Alamat: ")

                        conn = connect_database()
                        cur = conn.cursor()
                        try:
                            cur.execute(
                               "UPDATE penyewa SET alamat_penyewa = %s WHERE username = %s", (edit_alamat, username)
                            )
                            conn.commit()
                            print("Alamat berhasil diedit.")
                            click_enter_penyewa(username, password)
                        except Exception as e:
                            print(f"Terjadi kesalahan: {e}")
                            conn.rollback()
                        finally:
                            cur.close()
                            conn.close()
                elif pilihan == 2:
                    click_enter_penyewa(username, password)
                else:
                    print("Input Tidak Valid")
                    click_enter_penyewa(username, password)

        else:
            print("Username tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cur.close()
        conn.close()

def sewa_mobil(username, password):
    clear_screen()
    conn = connect_database()
    #cur = conn.cursor()
    if conn:

        cur = conn.cursor()

        try:
            query = """
            SELECT 
                m.id_mobil, m.no_polisi_mobil, m.nama_mobil, m.harga_sewa_mobil, m.tahun_mobil, 
                m.kapasitas_penumpang, COALESCE(m.keterangan, ''), mm.nama_merk_mobil, sm.status_mobil 
            FROM 
                mobil m
            JOIN 
                merk_mobil mm ON m.id_merk_mobil = mm.id_merk_mobil
            JOIN 
                status_mobil sm ON m.id_status_mobil = sm.id_status_mobil
            ORDER BY 
                m.id_mobil ASC
            """
            cur.execute(query)
            mobil = cur.fetchall()

            if mobil:
                print('='*118)
                print(f"{'DAFTAR MOBIL':^118}")
                print('='*118)
                print(f"{'ID Mobil':<10}{'No Polisi':<12}{'Nama Mobil':<20}{'Harga Sewa':<15}{'Tahun Produksi':<15}{'Kapasitas':<10}{'Keterangan':<12}{'Merk Mobil':<15}{'Status':<10}")
                print('-'*118)
                for i in mobil:
                    print(f"{i[0]:<10}{i[1]:<12}{i[2]:<20}Rp.{i[3]:<12}{i[4]:<15}{i[5]:<10}{i[6]:<12}{i[7]:<15}{i[8]:<10}")
                print('='*118)

            else:
                print("Mobil tidak ditemukan.")
                click_enter_penyewa(username, password)
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")


        print("[1]. Pilih Mobil \n[2]. Kembali")
        while True:
            pilihan = int(input("Pilihan >"))
            if pilihan == 1:
                id_mobil = int(input("Masukkan ID mobil yang ingin disewa: "))
                while True:
                    tanggal_penyewaan = input("Masukkan tanggal penyewaan (YYYY-MM-DD): ")
                    #tanggal_akhir = input("Masukkan tanggal jatuh tempo (YYYY-MM-DD): ")
                    waktu_sewa = int(input("Masukkan Waktu Sewa Mobil per Hari: "))
                    sekarang = str(datetime.now().strftime('%Y-%m-%d'))
                    try:
                        tanggal_penyewaan_dt = datetime.strptime(tanggal_penyewaan, '%Y-%m-%d')
                       
                        #tanggal_akhir_dt = datetime.strptime(tanggal_akhir, '%Y-%m-%d')
                        sekarang_dt = datetime.now().strptime(sekarang, '%Y-%m-%d')

                        # if tanggal_akhir_dt <= tanggal_penyewaan_dt:
                        #     print("Tanggal jatuh tempo harus lebih besar dari tanggal penyewaan!")
                        if tanggal_penyewaan_dt < sekarang_dt:
                            print("Tanggal Penyewaan Telah berlalu!")
                        else:
                            # rentan_waktu = (tanggal_akhir_dt - tanggal_penyewaan_dt).days
                    
                            cur.execute("SELECT harga_sewa_mobil FROM mobil WHERE id_mobil = %s", (id_mobil,))
                            harga_per_hari = cur.fetchone()[0]                  
                            total_biaya = waktu_sewa * harga_per_hari

                            print(f"Total Harga untuk {waktu_sewa} hari adalah: {total_biaya}")
                            break
                   
                    except ValueError:
                            print("Format tanggal salah. Silakan coba lagi.")
                    
                try:
                    cur.execute("SELECT * FROM sopir")
                    sopir = cur.fetchall()

                    if sopir:
                        clear_screen()
                        print('='*40)
                        print(f"{'DATA SOPIR':^40}")
                        print('='*40)
                        print(f"{'ID Sopir':<15}{'Nama Sopir':<30}")
                        print('-'*40)
                        for i in sopir:
                            print(f"{i[0]:<15}{i[1]:<30}")
                        print('='*40)

                    else:
                        print("Sopir tidak ditemukan.")

                except Exception as e:
                    print(f"Terjadi kesalahan: {e}")
                # finally:
                #     cur.close()
                #     conn.close()
                            
                print("[1]. Pilih Sopir \n[2]. Tanpa Sopir")
                while True:
                    pilihan = int(input("Pilihan >"))
                    if pilihan == 1:
                        id_sopir = int(input("Masukkan ID Sopir yang diinginkan: "))
                        cur.execute("SELECT * FROM sopir WHERE id_sopir = %s", (id_sopir,))
                        sopir = cur.fetchone()[0]
                        print(f"{sopir} telah dipilih sebagai Sopir Anda.")
                        
                        id_lepas_kunci = 2
                        break
                    elif pilihan == 2:
                        print("Anda Tidak Memilih Sopir! Gunakan Mobil dengan Bijak.")
                        id_sopir = None
                        id_lepas_kunci = 1
                        break
                
                 #DEFAULT TRANSAKSI PENYEWAAN
                tanggal_jatuh_tempo = sekarang
                id_admin = 1
                id_jenis_pembayaran = 2
                id_status_pembayaran = 2
                try:
                    cur.execute("SELECT id_penyewa FROM penyewa WHERE username = %s", (username,))
                    id_penyewa = cur.fetchone()[0]

                except Exception as e:
                    print(f"Terjadi kesalahan: {e}")
                
                try:
                    query = """
                        INSERT into transaksi_penyewaan 
                        (tanggal_penyewaan, tanggal_jatuh_tempo, id_penyewa, id_admin, id_mobil, 
                        id_jenis_pembayaran, id_status_pembayaran, id_status_lepas_kunci, id_sopir, waktu_sewa) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """  
                    data =  (tanggal_penyewaan, tanggal_jatuh_tempo, id_penyewa, id_admin, id_mobil,
                    id_jenis_pembayaran, id_status_pembayaran, id_lepas_kunci, id_sopir, waktu_sewa)
                    cur.execute(query, data)
                    conn.commit()
                    print("Transaksi Berhasil Ditambahkan.")
                    click_enter_penyewa(username, password)
                except Exception as e:
                    print(f"Terjadi kesalahan: {e}")
                    conn.rollback()
                finally:
                    cur.close()
                    conn.close()       

            elif pilihan == 2:
                homepage_penyewa(username,password)

def pembayaran(username, password):
    clear_screen()
    conn = connect_database()
    cur = conn.cursor()

    try:
        query = """
        SELECT 
             t.id_transaksi_penyewaan ,p.nama_penyewa, t.tanggal_penyewaan, m.nama_mobil, COALESCE(s.nama_sopir, 'Kosong'), sp.status_pembayaran
             ,slk.status_lepas_kunci, (t.waktu_sewa * m.harga_sewa_mobil) as total_biaya
        
        FROM 
            transaksi_penyewaan t
        JOIN 
            mobil m ON m.id_mobil = t.id_mobil
        JOIN 
            penyewa p ON p.id_penyewa = t.id_penyewa
        JOIN
            status_pembayaran sp ON sp.id_status_pembayaran = t.id_status_pembayaran
        JOIN
            status_lepas_kunci slk ON slk.id_status_lepas_kunci = t.id_status_lepas_kunci
        LEFT JOIN
            sopir s ON s.id_sopir = t.id_sopir
        WHERE p.username = %s and sp.id_status_pembayaran = 2
        """
        cur.execute(query, (username,))
        transaksi = cur.fetchall()
        if transaksi:
            clear_screen()
            print('='*120)
            print(f"{'DAFTAR PENYEWAAN':^120}")
            print('='*120)
            print(f"{'ID Transkasi':<13}{'Nama Penyewa':<20}{'Tgl. Sewa':<20}{'Mobil':<20}{'Sopir':<15}{'Status Pembayaran':<18}{'Lepas Kunci':<15}")
            print('-'*120)
            total_biaya_keseluruhan = 0
            for i in transaksi:
                id_transaksi = i[0]
                nama_penyewa = i[1]
                tanggal_penyewaan = i[2].strftime('%Y-%m-%d')  # Format tanggal
                nama_mobil = i[3]
                nama_sopir = i[4]
                status_pembayaran = i[5]
                status_lepas_kunci = i[6]
                total_biaya = i[7]

                total_biaya_keseluruhan += total_biaya
                
                # Cetak data dengan format yang diinginkan
                print(f"{id_transaksi:<13}{nama_penyewa:<20}{tanggal_penyewaan:<20}{nama_mobil:<20}{nama_sopir:<15}{status_pembayaran:<18}{status_lepas_kunci:<15}")
            print('='*120)
            print(f"Total Biaya Anda: Rp.{total_biaya_keseluruhan} ")
            print("\n")
            print("PILIH METODE PEMBAYARAN")
            print("[1]. Transfer Bank \n[2]. Cash \n\n[0].Kembali")
            while True:
                pilihan = int(input("Pilihan >"))
                if pilihan == 1:
                    
                    while True:
                        no_rekening = input("Masukkan No. Rekening: ")
                        bank = input("Bank (BCA/BRI): ")
                        nominal_uang = Decimal(input("Masukkan Nominal Uang: "))

                        if nominal_uang < total_biaya:
                            print("Pembayaran Gagal. Nominal Uang Tidak Mencukupi")
                        else:
                            try:
                                query = '''INSERT INTO transfer_bank (nomor_rekening, bank, nominal_uang)
                                VALUES (%s, %s, %s)
                                '''
                                cur.execute(query, (no_rekening, bank, nominal_uang))
                                #id_jenis_pembayaran = cur.fetchone()[0]
                                conn.commit()

                                            
                            except Exception as e:
                                print(f"Terjadi kesalahan: {e}")
                                conn.rollback()
                            
                            id_status_pembayaran = 1
                            try:
                                query = '''UPDATE transaksi_penyewaan SET id_jenis_pembayaran = %s, id_status_pembayaran = %s WHERE id_transaksi_penyewaan = %s
                                '''

                                query2 = '''UPDATE transfer_bank SET id_jenis_pembayaran = %s,  WHERE nomor_rekening = %s
                                '''
                                cur.execute(query, (pilihan, id_status_pembayaran, id_transaksi))
                                cur.execute(query2, (pilihan, no_rekening))
                                #id_jenis_pembayaran = cur.fetchone()[0]
                                conn.commit()
                                print("Pembayaran Berhasil ")
                                        
                            except Exception as e:
                                print(f"Terjadi kesalahan: {e}")
                                conn.rollback()
                            
                            break
                            
                elif pilihan == 2:
                    
                    while True:
                        nominal_tunai = Decimal(input("Masukkan Nominal Tunai:"))
                        kembalian = nominal_tunai - total_biaya
                        if nominal_tunai < total_biaya:
                            print("Pembayaran Gagal. Nominal Uang Tidak Mencukupi")
                        else:
                            try:
                                query = '''INSERT INTO cash (nominal_tunai, kembalian)
                                VALUES (%s, %s, %s, %s)
                                '''
                                cur.execute(query, (nominal_tunai, kembalian))
                                #id_jenis_pembayaran = cur.fetchone()[0]
                                conn.commit()

                                            
                            except Exception as e:
                                print(f"Terjadi kesalahan: {e}")
                                conn.rollback()
                            
                            id_status_pembayaran = 1
                            try:
                                query = '''UPDATE transaksi_penyewaan SET id_jenis_pembayaran = %s, id_status_pembayaran = %s WHERE id_transaksi_penyewaan = %s
                                '''
                                
                                query2 = '''UPDATE cash SET id_jenis_pembayaran = %s  WHERE nominal_tunai = %s
                                '''
                                cur.execute(query, (pilihan, id_status_pembayaran, id_transaksi))
                                cur.execute(query2, (pilihan, nominal_tunai))
                                #id_jenis_pembayaran = cur.fetchone()[0]
                                conn.commit()
                                print("Pembayaran Berhasil")
                                        
                            except Exception as e:
                                print(f"Terjadi kesalahan: {e}")
                                conn.rollback()
                            
                            break
                elif pilihan == 0:
                    click_enter_penyewa(username, password)
                else:
                    print("Kesalahan Input. Coba Lagi")
                    
        else:
            print("Transaksi Penyewaan tidak ditemukan.")
            click_enter_penyewa(username, password)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cur.close()
        conn.close()

def pengembalian (username, password):
    clear_screen()
    conn = connect_database()
    if conn :

        cur = conn.cursor()

        try:
            query = """
            SELECT 
                t.id_transaksi_penyewaan ,p.nama_penyewa, t.tanggal_penyewaan, t.tanggal_jatuh_tempo, m.nama_mobil, COALESCE(s.nama_sopir, 'Kosong'), slk.status_lepas_kunci,
                sp.status_pembayaran
                 
            FROM 
                transaksi_penyewaan t
            JOIN 
                mobil m ON m.id_mobil = t.id_mobil
            JOIN 
                penyewa p ON p.id_penyewa = t.id_penyewa
            JOIN
                status_pembayaran sp ON sp.id_status_pembayaran = t.id_status_pembayaran
            JOIN
                status_lepas_kunci slk ON slk.id_status_lepas_kunci = t.id_status_lepas_kunci
            LEFT JOIN
                sopir s ON s.id_sopir = t.id_sopir
            WHERE p.username = %s and sp.id_status_pembayaran = 1
            
            """
            cur.execute(query, (username, ))
            pengembalian = cur.fetchall()

            if pengembalian:
                clear_screen()
                print('='*130)
                print(f"{'DAFTAR PENYEWAAN':^130}")
                print('='*130)
                print(f"{'ID Transkasi':<13}{'Nama Penyewa':<17}{'Tgl. Sewa':<13}{'Tgl. Jatuh Tempo':<18}{'Mobil':<15}{'Sopir':<15}{'Lepas Kunci':<15}{'Status Pembayaran':<18}")
                print('-'*130)
                for i in pengembalian:
                    id_transaksi = i[0]
                    nama_penyewa = i[1]
                    tanggal_penyewaan = i[2].strftime('%Y-%m-%d')
                    tanggal_jatuh_tempo = i[3].strftime('%Y-%m-%d')  # Format tanggal
                    nama_mobil = i[4]
                    nama_sopir = i[5] 
                    status_lepas_kunci = i[6]
                    status_pembayaran = i[7]

                    print(f"{id_transaksi:<13}{nama_penyewa:<17}{tanggal_penyewaan:<13}{tanggal_jatuh_tempo:<18}{nama_mobil:<15}{nama_sopir:<15}{status_lepas_kunci:<15}{status_pembayaran:<18}")
                print('='*130)

            else:
                print("Transaksi Penyewaan tidak ditemukan.")
                click_enter_penyewa(username, password)

            print("[1]. Kembalikan Mobil \n\n[0]. Kembali")
            while True:
                pilihan = int(input("Pilihan >"))
                if pilihan == 1:
                    while True:
                        id_pengembalian = int(input("Masukkan ID Transaksi yang ingin dikembalikan: "))
                        sekarang = str(datetime.now().strftime('%Y-%m-%d'))
                        try:
                            query ="""SELECT tp.id_transaksi_penyewaan 
                            FROM transaksi_penyewaan tp
                            join penyewa p on (p.id_penyewa = tp.id_penyewa)
                            WHERE username= %s
                            """
                            cur.execute(query, (username, ))
                            id_transaksi = cur.fetchone()[0]

                            #DEFAULT PENGEMBALIAN
                            denda = 0
                            tanggal_pengembalian = sekarang
                            id_status_pengembalian = 2

                            if id_transaksi == id_pengembalian :

                                query = """INSERT into pengembalian (tanggal_pengembalian, denda, id_transaksi_penyewaan, id_status_pengembalian) 
                                values (%s,%s,%s,%s) 
                                """
                                cur.execute(query,(tanggal_pengembalian, denda, id_transaksi, id_status_pengembalian))
                                conn.commit()
                                print("Pengembalian Mobil Berhasil. Silahkan Tunggu Konfirmasi dari Admin.")
                                click_enter_penyewa(username, password)
                                break
                            else :
                                print("ID Transaksi salah / tidak ditemukan")

                        except Exception as e:
                            print(f"Terjadi kesalahan: {e}")
                            conn.rollback()

                elif pilihan == 0:
                    click_enter_penyewa(username, password)
                else:
                    print("Kesalahan Input. Coba Lagi")
                    click_enter_penyewa(username, password)
        
        except Exception as e:
            print(f"Terjadi kesalahan : {e}")
        finally:
            cur.close()
            conn.close()
#==========================================================================================================================
#====================ADMIN============================================================================================

#JANGAN LUPA TUGAS ADMIN: MENGATUR TANGGAL JATUH TEMPO, MENGATUR KONFIRMASI PENGEMBALIAN, KONFIRMASI PEMBAYARAN (OPSIONAL)

def click_enter_admin(username, password):
    print("\n")
    kembali = input("Tekan Enter untuk melanjutkan ke Menu...")
    print(kembali) 
    homepage_admin(username, password)

def login_admin():
    print(" ROLE ADMIN ")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    conn = connect_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        admin = cur.fetchone()

        if admin:
            print("Login berhasil!")
            print("Selamat datang Admin, ", admin[1])
            print("\n")
            click_enter_admin(username, password)
            
        else:
            print("Login gagal. Username atau password salah.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cur.close()
        conn.close()


def homepage_admin(username, password):
    
    clear_screen()

    print('='*70)
    print(f"{'SELAMAT DATANG ADMIN DI EL NUSA TOUR':^70} \n {'RENTAL MOBIL TERPERCAYA ':^70}")
    print('='*70)

    print(" [1]. LIHAT PROFIL ADMIN \n [2]. DATA MOBIL \n [3]. DATA SOPIR \n [4]. PEMBAYARAN \n [5]. LIHAT TRANSAKSI \n [6]. KONFIRMASI PENGEMBALIAN \n\n [0]. KELUAR")
    print('='*70)
    opsi = (input("Pilih Opsi yang ingin digunakan: "))
    while(True):
        if opsi == '1':
            profil_admin(username, password)      
        elif opsi == '2':
            data_mobil(username, password)
        elif opsi == '3':
            data_sopir(username, password)
        elif opsi == '4':
            pass
            #data_pembayaran(username, password)
        elif opsi == '5':
            pass
            #data_transaksi(username, password)
        elif opsi == '6':
            data_pengembalian(username, password)


def profil_admin(username, password):
    conn = connect_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username,password))
        admin = cur.fetchone()

        if admin:
            clear_screen()
            print('='*70)
            print(f"{'PROFIL ADMIN':^70}")
            print('='*70)
            print(f"ID Admin \t: {admin[0]}")
            print(f"Nama Admin \t: {admin[1]}")
            print(f"Username \t: {admin[2]}")
            print('='*70)

            click_enter_admin(username, password)
        else:
            print("Username tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cur.close()
        conn.close()

def data_mobil(username, password):
    clear_screen()
    print('='*70)
    print(f"{'DATA MOBIL':^70}")
    print('='*70)

    print(" [1]. LIHAT DATA MOBIL \n [2]. TAMBAH MOBIL \n [3]. EDIT DATA MOBIL \n [4]. HAPUS DATA MOBIL \n\n [0]. KELUAR")
    
    opsi = (input("Pilih Opsi yang ingin digunakan: "))
    while(True):
        if opsi == '1':
            lihat_mobil(username, password)
        elif opsi == '2':
            # pass
            #lihat_merk(username, password)
            tambah_mobil(username, password)
        elif opsi == '3':
            pass
        elif opsi == '4':
            pass
        elif opsi == '0':
            click_enter_admin(username, password)

def lihat_mobil(username, password):
    clear_screen()
    conn = connect_database()
    cur = conn.cursor()

    try:
        query = """
        SELECT 
            m.id_mobil, m.no_polisi_mobil, m.nama_mobil, m.harga_sewa_mobil, m.tahun_mobil, 
            m.kapasitas_penumpang, COALESCE(m.keterangan, ''), mm.nama_merk_mobil, sm.status_mobil 
        FROM 
            mobil m
        JOIN 
            merk_mobil mm ON m.id_merk_mobil = mm.id_merk_mobil
        JOIN 
            status_mobil sm ON m.id_status_mobil = sm.id_status_mobil
        """
        cur.execute(query)
        mobil = cur.fetchall()

        if mobil:
            clear_screen()
            print('='*120)
            print(f"{'DAFTAR MOBIL':^120}")
            print('='*120)
            print(f"{'ID Mobil':<10}{'No Polisi':<15}{'Nama Mobil':<20}{'Harga Sewa':<15}{'Tahun Produksi':<15}{'Kapasitas':<10}{'Keterangan':<12}{'Merk Mobil':<15}{'Status':<10}")
            print('-'*120)
            for i in mobil:
                print(f"{i[0]:<10}{i[1]:<15}{i[2]:<20}{i[3]:<15}{i[4]:<15}{i[5]:<10}{i[6]:<12}{i[7]:<15}{i[8]:<10}")
            print('='*120)

            click_enter_admin(username, password)
        else:
            print("Mobil tidak ditemukan.")
            click_enter_admin(username, password)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cur.close()
        conn.close()

def tambah_mobil(username, password):
    clear_screen()
    print('='*70)
    print(f"{'TAMBAH MOBIL':^70}")
    print('='*70)

    no_polisi = input("Masukkan No. Polisi Mobil: ")
    id_merk = int(input("Masukkan ID Merk: "))
    nama_mobil = input("Masukkan nama Sopir: ")
    harga_sewa_mobil = Decimal(input("Masukkan Harga Sewa / Hari: Rp.  "))
    tahun_mobil = int(input("Masukkan Tahun Produksi Mobil: "))
    kapasitas = int(input("Masukkan Kapasitas Penumpang: "))
    keterangan = input("Masukkan Keterangan Tambahan: ")
    id_status = int(input("Masukkan ID Status: "))

    conn = connect_database()
    cur = conn.cursor()
    try:
        query = """
            INSERT into mobil (no_polisi_mobil, nama_mobil, harga_sewa_mobil, 
            tahun_mobil, kapasitas_penumpang, keterangan, id_status_mobil, id_merk_mobil) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """  
        data =  (no_polisi, nama_mobil, harga_sewa_mobil, tahun_mobil, kapasitas, keterangan, id_status, id_merk)
        cur.execute(query, data)
        conn.commit()
        print("Sopir Berhasil Ditambahkan.")
        click_enter_admin(username, password)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def edit_mobil(username, password):
    conn = connect_database()
    cur = conn.cursor()

    try:
        query = """
            "SELECT id_mobil, no_polisi_mobil, nama_mobil, harga_sewa_mobil, tahun_mobil, kapasitas_penumpang, keterangan, id_status_mobil, id_merk_mobil FROM mobil") VA
            """
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally: 
        pass

def hapus_mobil(username, password):
    pass
def lihat_merk(username, password):
    clear_screen()
    conn = connect_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM merk_mobil")
        merk_mobil = cur.fetchall()

        if merk_mobil:
            clear_screen()
            print('='*70)
            print(f"{'MERK MOBIL':^70}")
            print('='*70)
            print(f"{'ID Merk':<15}{'Merk Mobil':<30}")
            print('-'*70)
            for i in merk_mobil:
                print(f"{i[0]:<15}{i[1]:<30}")
            print('='*70)

            click_enter_admin(username, password)
        else:
            print("Merk Mobil tidak ditemukan.")
            click_enter_admin(username, password)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cur.close()
        conn.close()

#DATA SOPIR ================================================================================================================
def data_sopir(username, password):
    clear_screen()
    print('='*70)
    print(f"{'DATA SOPIR':^70}")
    print('='*70)

    print(" [1]. LIHAT DATA SOPIR \n [2]. TAMBAH SOPIR \n [3]. EDIT DATA SOPIR \n [4]. HAPUS DATA SOPIR \n\n [0]. KELUAR")
    
    opsi = (input("Pilih Opsi yang ingin digunakan: "))
    while(True):
        if opsi == '1':
            lihat_data_sopir(username, password)
        elif opsi == '2':
            tambah_sopir(username, password)
        elif opsi == '3':
            edit_sopir(username, password)
        elif opsi == '4':
            hapus_sopir(username, password)
        elif opsi == '0':
            click_enter_admin(username, password)

def lihat_data_sopir(username, password):
    clear_screen()
    conn = connect_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM sopir")
        sopir = cur.fetchall()

        if sopir:
            clear_screen()
            print('='*70)
            print(f"{'DATA SOPIR':^70}")
            print('='*70)
            print(f"{'ID Sopir':<15}{'Nama Sopir':<30}{'No. Telepon':<20}")
            print('-'*70)
            for i in sopir:
                print(f"{i[0]:<15}{i[1]:<30}{i[2]:<20}")
            print('='*70)

            click_enter_admin(username, password)
        else:
            print("Sopir tidak ditemukan.")
            click_enter_admin(username, password)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cur.close()
        conn.close()

def tambah_sopir(username, password):
    clear_screen()
    print('='*70)
    print(f"{'TAMBAH SOPIR':^70}")
    print('='*70)

    nama_sopir = input("Masukkan nama Sopir: ")
    no_telepon_sopir = input("Masukkan No. Telepon: ")

    conn = connect_database()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO sopir (nama_sopir, no_telepon_sopir) VALUES (%s, %s)",
            (nama_sopir, no_telepon_sopir)
        )
        conn.commit()
        print("Sopir Berhasil Ditambahkan.")
        click_enter_admin(username, password)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def edit_sopir(username, password):
    clear_screen()
    print('='*70)
    print(f"{'EDIT DATA SOPIR':^70}")
    print('='*70)

    conn = connect_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM sopir ORDER BY id_sopir ASC")
        sopir = cur.fetchall()

        if sopir:
            clear_screen()
            print('='*70)
            print(f"{'DATA SOPIR':^70}")
            print('='*70)
            print(f"{'ID Sopir':<15}{'Nama Sopir':<30}{'No. Telepon':<20}")
            print('-'*70)
            for i in sopir:
                print(f"{i[0]:<15}{i[1]:<30}{i[2]:<20}")
            print('='*70)
            
            id_sopir = int(input("Masukkan ID Sopir yang diedit: "))
            edit_nama_sopir = input("Edit Nama Sopir: ")
            edit_no_telepon = input("Edit No. Telepon: ")

            try:
                cur.execute(
                    "UPDATE sopir SET nama_sopir = %s, no_telepon_sopir = %s WHERE id_sopir = %s", (edit_nama_sopir, edit_no_telepon, id_sopir)
                )
                conn.commit()
                print("Data Sopir berhasil diedit.")
                click_enter_admin(username, password)
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
                conn.rollback()
            finally:
                cur.close()
                conn.close()
            click_enter_admin(username, password)
        else:
            print("Sopir tidak ditemukan.")
            click_enter_admin(username, password)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cur.close()
        conn.close()

def hapus_sopir(username, password):
    clear_screen()
    print('='*70)
    print(f"{'HAPUS DATA SOPIR':^70}")
    print('='*70)

    conn = connect_database()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM sopir ORDER BY id_sopir ASC")
        sopir = cur.fetchall()

        if sopir:
            clear_screen()
            print('='*70)
            print(f"{'DATA SOPIR':^70}")
            print('='*70)
            print(f"{'ID Sopir':<15}{'Nama Sopir':<30}{'No. Telepon':<20}")
            print('-'*70)
            for i in sopir:
                print(f"{i[0]:<15}{i[1]:<30}{i[2]:<20}")
            print('='*70)
            
            id_sopir = int(input("Masukkan ID Sopir yang dihapus: "))

            try:
                cur.execute(
                    f"DELETE FROM sopir WHERE id_sopir = {id_sopir}"
                )
                conn.commit()
                print("Data Sopir berhasil dihapus.")

                click_enter_admin(username, password)
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
                conn.rollback()
            finally:
                cur.close()
                conn.close()
            click_enter_admin(username, password)
        else:
            print("Sopir tidak ditemukan.")
            click_enter_admin(username, password)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cur.close()
        conn.close()

def data_pengembalian(username, password):
    clear_screen()
    conn = connect_database()
    cur = conn.cursor()

    try:
        query = """
        SELECT pb.id_pengembalian, pb.id_transaksi_penyewaan, pb.tanggal_pengembalian, tp.tanggal_jatuh_tempo, pb.denda, spb.status_pengembalian
        FROM pengembalian pb JOIN status_pengembalian spb ON spb.id_status_pengembalian = pb.id_status_pengembalian
        JOIN transaksi_penyewaan tp ON tp.id_transaksi_penyewaan = pb.id_transaksi_penyewaan
           
        """
        cur.execute(query)
        data_pengembalian = cur.fetchall()

        if data_pengembalian:
            clear_screen()
            print('='*100)
            print(f"{'DAFTAR PENGEMBALIAN':^100}")
            print('='*100)
            print(f"{'ID Pengembalian':<18}{'ID Transaksi':<15}{'Tanggal Pengembalian':<22}{'Tanggal Jatuh Tempo':<22}{'Denda':<15}{'Status Pengembalian':<15}")
            print('-'*100)
            for i in data_pengembalian:
                id_pengembalian = i[0]
                id_transaksi = i[1]
                tanggal_kembali = i[2].strftime('%Y-%m-%d')
                tanggal_jatuh_tempo = i[3].strftime('%Y-%m-%d')
                denda = i[4]
                status_pengembalian = i[5]
                print(f"{id_pengembalian:<18}{id_transaksi:<15}{tanggal_kembali:<22}{tanggal_jatuh_tempo:<22}{denda:<15}{status_pengembalian:<15}")
            print('='*100)

            print("[1]. Konfirmasi Pengembalian \n[2]. Tambah Denda \n\n[0]. Keluar")
            opsi = (input("Pilihan> "))
            while(True):
                if opsi == '1':
                    while True:
                        input_id_pengembalian = int(input("Masukkan ID Pengembalian: "))
                        print("[1]. Sudah \n[2]. Belum")
                        id_status_pengembalian = int(input("Masukkan ID Status Pengembalian (1/2): "))
                        if id_status_pengembalian == 1 or id_status_pengembalian == 2:
                            try:
                                query ="""UPDATE pengembalian SET id_status_pengembalian = %s WHERE id_pengembalian = %s
                                """
                                cur.execute(query, (id_status_pengembalian, input_id_pengembalian))                            
                                conn.commit()
                                print("Konfirmasi Pengembalian Berhasil Disimpan")
                                click_enter_admin(username, password)

                            except Exception as e:
                                print(f"Terjadi kesalahan: {e}")
                                conn.rollback()
                        else:
                            print("Kesalahan Input. Coba Lagi")

                elif opsi == '2':
                    tambah_sopir(username, password)
                
                elif opsi == '0':
                    click_enter_admin(username, password)
                else:
                    print("Kesalahan Input. Coba Lagi")
        else:
            print("Data Pengembalian tidak ditemukan.")
            click_enter_admin(username, password)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cur.close()
        conn.close()


# def read_penyewa():
#     conn = connect_database()
#     cur = conn.cursor()    
#     query = "SELECT * FROM penyewa"
#     cur.execute(query)
#     data = cur.fetchall()
#     for i in data:
#         print(i)
#     cur.close()
#     conn.close()

def back_pilihan():
    print("\n")
    kembali = input("Tekan Enter untuk melanjutkan ke Menu...")
    print(kembali) 
    pilihan()

#pilihan()
#read_penyewa()
#register_penyewa()
#login_penyewa()
login_admin()