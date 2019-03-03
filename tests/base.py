# from app.app import db, config_app, login
# from app.modeles.utilisateurs import User
# from app.modeles.donnees import table1, table2
from unittest import TestCase


class Base(TestCase):
    # import de la BDD

    def setUp(self):
        self.app = config_app("test")
        self.db = db
        self.client = self.app.test_client()
        self.db.create_all(app=self.app)

    def tearDown(self):
        self.db.drop_all(app=self.app)

    # def insert_all(self, places=True): 
    #     # On donne à notre DB le contexte d'exécution
    #     with self.app.app_context():
    #         if places:
    #             for fixture in self.places:
    #                 self.db.session.add(fixture)
    #         self.db.session.commit()