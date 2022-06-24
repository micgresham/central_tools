from .models import Profile
from .pymenu import Menu

class AuthRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """

    route_app_labels = ('auth', 'contenttypes', 'sessions', 'admin')
   

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
#        print("-------IN DB ROUTER-------")
#        print(model._meta.app_label)
#        print("--------------------------") 
        if model._meta.app_label in self.route_app_labels:
            return 'auth_db'
        if model == Profile:
            return 'auth_db'
        if model == Menu:
            return 'auth_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
#        print("-------IN DB ROUTER-------")
#        print(model._meta.app_label)
#        print("--------------------------") 

        if model._meta.app_label in self.route_app_labels:
            return 'auth_db'
        if model == Profile:
            return 'auth_db'
        if model == Menu:
            return 'auth_db'

        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label in self.route_app_labels or \
           obj2._meta.app_label == 'home':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label in ('auth','admin','sessions','contenttypes'):
            return db == 'auth_db'
        return None

