from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()
app = create_app(os.getenv("FLASK_ENV") or "production")


@app.cli.command()
def test():
    """ Testing using unittest """
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)

