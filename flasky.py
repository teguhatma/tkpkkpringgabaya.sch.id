from app import create_app, db
from app.models import (
    GuruModel,
    MuridModel,
    KelasModel,
    ElearningModel,
    BeritaModel,
    DataSekolahModel,
    NilaiModel,
    ProfileSekolahModel,
    UserModel,
    Role,
)
from dotenv import load_dotenv
import os

load_dotenv()
app = create_app(os.getenv("FLASK_ENV") or "production")


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        GuruModel=GuruModel,
        MuridModel=MuridModel,
        KelasModel=KelasModel,
        ElearningModel=ElearningModel,
        BeritaModel=BeritaModel,
        DataSekolahModel=DataSekolahModel,
        NilaiModel=NilaiModel,
        ProfileSekolahModel=ProfileSekolahModel,
        Role=Role,
    )


@app.cli.command()
def test():
    """ Testing using unittest """
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def deploy():
    """ Insert Admin dan Insert Kelas """
    Role.insert_roles()
    UserModel.insert_admin()
    GuruModel.insert_guru()
    KelasModel.insert_kelas()


@app.cli.command()
def drop():
    """ Drop All Table in Database """
    db.session.remove()
    db.drop_all()
