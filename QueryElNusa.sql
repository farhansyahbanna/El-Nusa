CREATE TABLE admin (
    id_admin   serial NOT NULL PRIMARY KEY,
    nama_admin VARCHAR(50) NOT NULL,
    username   VARCHAR(20) NOT NULL UNIQUE,
    password   VARCHAR(12) NOT NULL
);

CREATE TABLE cash (
    id_jenis_pembayaran serial NOT NULL PRIMARY KEY,
    nominal_tunai       DECIMAL NOT NULL,
    kembalian           INTEGER NOT NULL
);

CREATE TABLE jenis_pembayaran (
    id_jenis_pembayaran serial NOT NULL PRIMARY KEY,
    jenis_pembayaran    VARCHAR(20) NOT NULL
);

CREATE TABLE merk_mobil (
    id_merk_mobil       serial NOT NULL PRIMARY KEY,
    nama_merk_mobil     VARCHAR(20) NOT NULL,
);

CREATE TABLE mobil (
    id_mobil                     serial NOT NULL PRIMARY KEY,
    no_polisi_mobil              VARCHAR(20) NOT NULL,
    nama_mobil                   VARCHAR(30) NOT NULL,
    harga_sewa_mobil             INTEGER NOT NULL,
    tahun_mobil                  INTEGER NOT NULL,
    kapasitas_penumpang          INTEGER NOT NULL,
    keterangan                   VARCHAR(255),
    id_status_mobil serial,
    id_merk_mobil     serial NOT NULL
);

CREATE TABLE pengembalian (
    id_pengembalian                            serial NOT NULL PRIMARY KEY,
    tanggal_pengembalian                       DATE NOT NULL,
    denda                                      DECIMAL NOT NULL, 
    id_transaksi_penyewaan serial NOT NULL
);

CREATE UNIQUE INDEX pengembalian__idx ON
    pengembalian (
        id_transaksi_penyewaan
    ASC );

CREATE TABLE penyewa (
    id_penyewa         serial NOT NULL PRIMARY KEY,
    nama_penyewa       VARCHAR(50) NOT NULL,
    username           VARCHAR(20) NOT NULL UNIQUE,
    password           VARCHAR(12) NOT NULL,
    no_telepon_penyewa VARCHAR(12) NOT NULL,
    alamat_penyewa     VARCHAR(50) NOT NULL,
    nik_ktp_penyewa    VARCHAR(21) NOT NULL
);

CREATE TABLE sopir (
    id_sopir         serial NOT NULL PRIMARY KEY,
    nama_sopir       VARCHAR(50) NOT NULL,
    no_telepon_sopir VARCHAR(13) NOT NULL
);

CREATE TABLE status_lepas_kunci (
    id_status_lepas_kunci serial NOT NULL PRIMARY KEY,
    status_lepas_kunci    INTEGER NOT NULL
);

CREATE TABLE status_mobil (
    id_status_mobil serial NOT NULL PRIMARY KEY,
    status_mobil    VARCHAR(10) NOT NULL
);

CREATE TABLE status_pembayaran (
    id_status_pembayaran serial NOT NULL PRIMARY KEY,
    status_pembayaran    VARCHAR(10) NOT NULL
);

CREATE TABLE transaksi_penyewaan (
    id_transaksi_penyewaan                   serial NOT NULL PRIMARY KEY,
    tanggal_penyewaan                        DATE NOT NULL,
    tanggal_jatuh_tempo                      DATE NOT NULL,
    id_penyewa                       serial NOT NULL,
    id_sopir                           serial NOT NULL,
    id_admin                           serial NOT NULL,
    id_mobil                           serial NOT NULL, 
    id_jenis_pembayaran     serial, 
    id_status_pembayaran   serial NOT NULL, 
    id_status_lepas_kunci serial
);

CREATE TABLE transfer_bank (
    id_jenis_pembayaran serial NOT NULL PRIMARY KEY,
    nomor_rekening      VARCHAR(13) NOT NULL,
    bank                VARCHAR(4000),
    nominal_uang        DECIMAL NOT NULL
);

CREATE TABLE status_pengembalian (
	Id_status_pengembalian serial not null primary key,
	Status_pengembalian varchar(20) not null,
);

ALTER TABLE cash
    ADD CONSTRAINT cash_jenis_pembayaran_fk FOREIGN KEY ( id_jenis_pembayaran )
        REFERENCES jenis_pembayaran ( id_jenis_pembayaran );

ALTER TABLE mobil
    ADD CONSTRAINT mobil_merk_mobil_fk FOREIGN KEY ( id_merk_mobil )
        REFERENCES merk_mobil ( id_merk_mobil );

ALTER TABLE mobil
    ADD CONSTRAINT mobil_status_mobil_fk FOREIGN KEY ( id_status_mobil )
        REFERENCES status_mobil ( id_status_mobil );

ALTER TABLE pengembalian
    ADD CONSTRAINT pengembalian_transaksi_penyewaan_fk FOREIGN KEY ( id_transaksi_penyewaan )
        REFERENCES transaksi_penyewaan ( id_transaksi_penyewaan );

ALTER TABLE transaksi_penyewaan
    ADD CONSTRAINT transaksi_penyewaan_admin_fk FOREIGN KEY ( id_admin )
        REFERENCES admin ( id_admin );

ALTER TABLE transaksi_penyewaan
    ADD CONSTRAINT transaksi_penyewaan_jenis_pembayaran_fk FOREIGN KEY ( id_jenis_pembayaran )
        REFERENCES jenis_pembayaran ( id_jenis_pembayaran );

ALTER TABLE transaksi_penyewaan
    ADD CONSTRAINT transaksi_penyewaan_mobil_fk FOREIGN KEY ( id_mobil )
        REFERENCES mobil ( id_mobil );

ALTER TABLE transaksi_penyewaan
    ADD CONSTRAINT transaksi_penyewaan_penyewa_fk FOREIGN KEY ( id_penyewa )
        REFERENCES penyewa ( id_penyewa );

ALTER TABLE transaksi_penyewaan
    ADD CONSTRAINT transaksi_penyewaan_sopir_fk FOREIGN KEY ( id_sopir )
        REFERENCES sopir ( id_sopir );

ALTER TABLE transaksi_penyewaan
    ADD CONSTRAINT transaksi_penyewaan_status_lepas_kunci_fk FOREIGN KEY ( id_status_lepas_kunci )
        REFERENCES status_lepas_kunci ( id_status_lepas_kunci );

ALTER TABLE transaksi_penyewaan
    ADD CONSTRAINT transaksi_penyewaan_status_pembayaran_fk FOREIGN KEY (id_status_pembayaran )
        REFERENCES status_pembayaran ( id_status_pembayaran );

ALTER TABLE transfer_bank
    ADD CONSTRAINT transfer_bank_jenis_pembayaran_fk FOREIGN KEY ( id_jenis_pembayaran )
        REFERENCES jenis_pembayaran ( id_jenis_pembayaran );

ALTER TABLE pengembalian
    add constraint pengembalian_status_pengembalian_fk foreign key (id_status_pengembalian)
        references status_pengembalian (id_status_pengembalian);
