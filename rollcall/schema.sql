CREATE TABLE SinhVien
(
    IDTay NVARCHAR(500),
	MSSV NVARCHAR(10),
	HoTen NVARCHAR(150) not null,
    PRIMARY KEY(MSSV)
);

CREATE TABLE HocPhan
(
	MaHocPhan NVARCHAR(10) primary key,
    Phong NVARCHAR(10) not null,
    MonHoc NVARCHAR(20) not null,
    GioBatDau DATETIME not null,
    GioKetThuc DATETIME not null,
    HocKy INT not null
);

CREATE TABLE DangKy
(
	MSSV NVARCHAR(10),
    MaHocPhan NVARCHAR(10),
    DiemDanh INT default(0),

    foreign key(MSSV) references SinhVien(MSSV),
    foreign key(MaHocPhan) references HocPhan(MaHocPhan),
    primary key(MSSV,MaHocPhan)
);