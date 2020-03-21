from flask import Blueprint

server = Blueprint("server", __name__, template_folder="templates")

from . import (
    guru,
    kelas,
    akun,
    pegawai,
    murid,
    wali,
    profile,
    data,
    berita,
    learning,
    jadwal,
)
