## Sistem Informasi Akademik Pada TK PKK Pringgabaya Berbasis Web
[Website](http://www.tkpkkpringgabaya.sch.id)
> Website ini merupakan aplikasi web untuk skripsi


### Config the app
1. Create environment
> `python -m venv env`
2. Install package requirements
> `pip install -r requirements.txt`
3. Create your database from PostgreSQL
4. Create file `.env` in root folder
5. Change DATABASE_URI in `config.py`, example:
> `DATABASE_URI='postgresql://username:password@hostname/database'`
6. Change value `insert_admin` and `insert_guru` in `app/models.py`
7. Initilization your database
> `flask db init`
8. Migrate your database
> `flask db migrate`
9. Upgrade your database
> `flask db upgrade`
10. Insert role and user (_user can be change in `app/models.py`_)
> `flask deploy`

### Running the app
> `flask run`

### Tools
- [Flask](https://flask.palletsprojects.com/)
- [PostgreSQL](https://www.postgresql.org/)

### Author
- [Teguh Atma Yudha](https://github.com/teguhatma)
