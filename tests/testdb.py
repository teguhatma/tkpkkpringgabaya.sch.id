import unittest
from flask import current_app
from app import create_app, db
from app.models import *


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def text_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])

    def test_a_input_kelas(self):
        input = KelasModel(ruang="A")
        db.session.add(input)
        db.session.commit()

    def test_a_input_guru(self):
        input = GuruModel(
            nama="Siti Kartini, S.Pd.",
            nik="19651231198321",
            jabatan="Guru",
            alamat="Dasan Bantek",
            nip="11141234514",
            kelurahan="Pringgabaya",
            kecamatan="Pringgabaya",
            kabupaten="Lombok Timur",
            provinsi="Nusa Tenggara Barat",
            agama="Islam",
            kelas=KelasModel.query.first(),
            tempat_lahir="Pringgabaya",
            tanggal_lahir="15 September 1965",
            golongan="IV/e",
            pendidikan_terakhir="S1 PGPAUD",
            jenis_kelamin="Perempuan",
            tahun_masuk="2010",
        )
        user = UserModel(
            email="sitikartini@gmail.com",
            role=Role.query.filter_by(name="Admin").first(),
        )
        user.password("adminadmin")
        db.session.add(user)
        db.session.commit()
        input.user = user
        db.session.add(input)
        db.session.commit()

    def test_b_rubah_guru(self):
        data = GuruModel.query.first()
        data.nama = "Siti Kartini, S.Pd."
        data.nik = "1965123119831121"
        data.jabatan = "Guru"
        data.alamat = "Dasan Bantek"
        data.nip = "11141234514"
        data.kelurahan = "Pringgabaya"
        data.kecamatan = "Pringgabaya"
        data.kabupaten = "Lombok Timur"
        data.provinsi = "Nusa Tenggara Barat"
        data.agama = "Islam"
        data.kelas = KelasModel.query.first()
        data.tempat_lahir = "Pringgabaya"
        data.tanggal_lahir = "15 September 1965"
        data.golongan = "IV/e"
        data.pendidikan_terakhir = "S1 PGPAUD"
        data.jenis_kelamin = "Perempuan"
        data.tahun_masuk = "2010"

        db.session.add(data)
        db.session.commit()

    def test_c_hapus_guru(self):
        data = GuruModel.query.first()
        db.session.delete(data)
        db.session.commit()

    def test_a_input_murid(self):
        input = MuridModel(
            nomor_induk="701",
            nama="Shifan Azmabiyan Hadi",
            nama_panggilan="Shifan",
            anak_ke="1",
            alamat="Jalan Sandubaya Nomor 33 Pringgabaya",
            dusun="Dasan Bantek",
            kelurahan="Pringgabaya",
            kecamatan="Pringgabaya",
            kabupaten="Lombok Timur",
            provinsi="Nusa Tenggara Barat",
            agama="Islam",
            tempat_lahir="Pringgabaya",
            tanggal_lahir="15 September 2010",
            lulus=False,
            nama_ibu_kandung="Yulida Adelina, S.Pd.",
            jenis_kelamin="Laki-laki",
            tahun_pelajaran="2019/ 2020",
            kelas=KelasModel.query.first(),
        )
        user = UserModel(
            email="shifanazmabiyan@gmail.com",
            role=Role.query.filter_by(name="Murid").first(),
        )
        user.password("adminadmin")
        input.user = user
        db.session.add(user)
        db.session.commit()
        db.session.add(input)
        db.session.commit()

    def test_b_rubah_murid(self):
        data = MuridModel.query.first()
        data.nomor_induk = "701"
        data.nama = "Shifan Azmabiyan Rubah"
        data.nama_panggilan = "Shifan"
        data.anak_ke = "1"
        data.alamat = "Jalan Sandubaya Nomor 33 Pringgabaya"
        data.dusun = "Dasan Bantek"
        data.kelurahan = "Pringgabaya"
        data.kecamatan = "Pringgabaya"
        data.kabupaten = "Lombok Timur"
        data.provinsi = "Nusa Tenggara Barat"
        data.agama = "Islam"
        data.tempat_lahir = "Pringgabaya"
        data.tanggal_lahir = "15 September 2010"
        data.lulus = False
        data.nama_ibu_kandung = "Yulida Adelina, S.Pd."
        data.jenis_kelamin = "Laki-laki"
        data.tahun_pelajaran = "2019/ 2020"
        data.kelas = KelasModel.query.first()

        db.session.add(data)
        db.session.commit()

    def test_c_hapus_murid(self):
        data = MuridModel.query.first()
        db.session.delete(data)
        db.session.commit()

    def test_a_input_wali_murid(self):
        input = WaliMuridModel(
            nama="Yulida Adelina, S.Pd.",
            agama="Islam",
            alamat="Jalan Sandubaya Nomor 33 Pringgabaya",
            kelurahan="Pringgabaya",
            kecamatan="Pringgabaya",
            kabupaten="Lombok Timur",
            provinsi="Nusa Tenggara Barat",
            jenis_kelamin="Perempuan",
            tempat_lahir="Pringgabaya",
            tanggal_lahir="01 Januari 1994",
            pekerjaan="PNS",
            nomor_telepon="081907823905",
            murid=MuridModel.query.first(),
        )
        db.session.add(input)
        db.session.commit()

    def test_b_rubah_wali_murid(self):
        data = WaliMuridModel.query.first()
        data.nama = "Yulida Adelina, S.Pd."
        data.agama = "Islam"
        data.alamat = "Jalan Sandubaya Nomor 33 Pringgabaya"
        data.kelurahan = "Pringgabaya"
        data.kecamatan = "Pringgabaya"
        data.kabupaten = "Lombok Timur"
        data.provinsi = "Nusa Tenggara Barat"
        data.jenis_kelamin = "Perempuan"
        data.tempat_lahir = "Pringgabaya"
        data.tanggal_lahir = "01 Januari 1994"
        data.pekerjaan = "PNS"
        data.nomor_telepon = "081907823905"
        data.murid = MuridModel.query.first()

        db.session.add(data)
        db.session.commit()

    def test_c_hapus_wali_murid(self):
        data = WaliMuridModel.query.first()
        db.session.delete(data)
        db.session.commit()

    def test_a_input_profile_sekolah(self):
        input = ProfileSekolahModel(
            nama_lembaga="TK PKK Pringgabaya",
            kode_pos="83654",
            kelurahan="Pringgabaya",
            kecamatan="Pringgabaya",
            kabupaten="Lombok Timur",
            alamat="Jalan Sandubaya Nomor 33 Pringgabaya",
            provinsi="Nusa Tenggara Barat",
            no_statistik="8712/ Statistik",
            akte_notaris="88192/ Notaris",
            kegiatan_belajar="16 Jam",
            tahun_berdiri="2010",
            status_tk="Swasta",
            no_izin_pendirian="09988/ Pendirian",
            no_izin_operasional="088871/ Operasional",
            kurikulum="2013",
            no_telepon="081907823905",
            website="tkpkkpringgabaya.sch.id",
            email="info@tkpkkpringgabaya.sch.id",
            visi_misi="Visi Misi",
        )
        input.sosmed = {
            "instagram": "https://istagram.com/tkpkkpringgabaya",
            "facebook": "https://facebook.com/tkpkkpringgabaya",
            "twitter": "https://instagram.com/tkpkkpringgabaya",
        }
        db.session.add(input)
        db.session.commit()

    def test_b_rubah_profile_sekolah(self):
        data = ProfileSekolahModel.query.first()
        data.nama_lembaga = "TK PKK Pringgabaya"
        data.kode_pos = "83654"
        data.kelurahan = "Pringgabaya"
        data.kecamatan = "Pringgabaya"
        data.kabupaten = "Lombok Timur"
        data.alamat = "Jalan Sandubaya Nomor 33 Pringgabaya"
        data.provinsi = "Nusa Tenggara Barat"
        data.no_statistik = "8712/ Statistik"
        data.akte_notaris = "88192/ Notaris"
        data.kegiatan_belajar = "16 Jam"
        data.tahun_berdiri = "2010"
        data.status_tk = "Swasta"
        data.no_izin_pendirian = "09988/ Pendirian"
        data.no_izin_operasional = "088871/ Operasional"
        data.kurikulum = "2013"
        data.no_telepon = "081907823905"
        data.website = "tkpkkpringgabaya.sch.id"
        data.email = "info@tkpkkpringgabaya.sch.id"
        data.visi_misi = "Visi Misi"

        data.sosmed = {
            "instagram": "https://istagram.com/tkpkkpringgabaya",
            "facebook": "https://facebook.com/tkpkkpringgabaya",
            "twitter": "https://instagram.com/tkpkkpringgabaya",
        }
        db.session.add(data)
        db.session.commit()

    def test_a_input_dokumen_sekolah(self):
        input = DataSekolahModel(judul="TK PKK Pringgabaya", deskripsi="Deskripsi",)
        db.session.add(input)
        db.session.commit()

    def test_b_rubah_dokumen_sekolah(self):
        data = DataSekolahModel.query.first()
        data.judul = "TK PKK Pringgabaya"
        data.deskripsi = "Deskripsi"
        db.session.add(data)
        db.session.commit()

    def test_c_hapus_dokumen_sekolah(self):
        data = DataSekolahModel.query.first()
        db.session.delete(data)
        db.session.commit()

    def test_a_input_berita(self):
        input = BeritaModel(
            judul="TK PKK Pringgabaya", deskripsi="Deskripsi", tampilkan=True,
        )
        db.session.add(input)
        db.session.commit()

    def test_b_rubah_berita(self):
        data = BeritaModel.query.first()
        data.judul = "TK PKK Pringgabaya"
        data.deskripsi = "Deskripsi"
        data.tampilkan = True
        db.session.add(data)
        db.session.commit()

    def test_c_hapus_berita(self):
        data = BeritaModel.query.first()
        db.session.delete(data)
        db.session.commit()

    def test_a_input_elearning(self):
        input = ElearningModel(
            deskripsi="Deskripsi",
            judul="TK PKK Pringgabaya",
            kelas=KelasModel.query.first(),
        )
        db.session.add(input)
        db.session.commit()

    def test_b_rubah_elearning(self):
        data = ElearningModel.query.first()
        data.deskripsi = "Deskripsi"
        data.judul = "TK PKK Pringgabaya"
        data.kelas = KelasModel.query.first()
        db.session.add(data)
        db.session.commit()

    def test_c_hapus_elearning(self):
        data = ElearningModel.query.first()
        db.session.delete(data)
        db.session.commit()

    def test_a_input_jadwal_sekolah(self):
        input = JadwalKelasModel(
            mata_pelajaran="Agama Islam",
            jam="07.00",
            jam_end="08.00",
            hari="Senin",
            kelas=KelasModel.query.first(),
        )
        db.session.add(input)
        db.session.commit()

    def test_b_rubah_jadwal_sekolah(self):
        data = JadwalKelasModel.query.first()
        data.mata_pelajaran = "Agama Islam"
        data.jam = "07.00"
        data.jam_end = "08.00"
        data.hari = "Senin"
        data.kelas = KelasModel.query.first()
        db.session.add(data)
        db.session.commit()

    def test_c_hapus_jadwal_sekolah(self):
        data = JadwalKelasModel.query.first()
        db.session.delete(data)
        db.session.commit()

    def test_a_input_prestasi_sekolah(self):
        input = PrestasiModel(
            nama="TK PKK Pringgabaya",
            kategori="Kategori",
            tahun="Tahun",
            juara="Juara",
            tingkat="Tingkat",
        )
        db.session.add(input)
        db.session.commit()

    def test_b_rubah_prestasi_sekolah(self):
        data = PrestasiModel.query.first()
        data.nama = "TK PKK Pringgabaya"
        data.kategori = "Kategori"
        data.tahun = "Tahun"
        data.juara = "Juara"
        data.tingkat = "Tingkat"
        db.session.add(data)
        db.session.commit()

    def test_c_hapus_prestasi_sekolah(self):
        data = PrestasiModel.query.first()
        db.session.delete(data)
        db.session.commit()

    def test_a_input_nilai_model(self):
        input = NilaiModel(
            deskripsi="Deskripsi",
            aspek_penilaian="Perkembangan Nilai Agama dan Moral",
            semester="Semester I",
            tahun_pelajaran="2019/ 2020",
            murid_id=MuridModel.query.first().id,
        )
        db.session.add(input)
        db.session.commit()

    def test_b_rubah_nilai_model(self):
        data = NilaiModel.query.first()
        data.aspek_penilaian = "Perkembangan Nilai Agama dan Moral"
        data.semester = "Semester I"
        data.tahun_pelajaran = "2019/ 2020"
        data.murid_id = MuridModel.query.first().id
        data.deskripsi = "Deskripsi Rubah"
        db.session.add(data)
        db.session.commit()

    def test_c_hapus_nilai_model(self):
        data = NilaiModel.query.first()
        db.session.delete(data)
        db.session.commit()

    # def zeyeng(self):
    #     db.session.remove()
    #     db.drop_all()
    #     self.app_context.pop()

