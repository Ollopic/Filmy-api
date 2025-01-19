from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, validators

from app.db.models import User
from app.utils import hash_password


class UserCreateForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField("Username", [validators.Length(min=4, max=25)])
    mail = StringField("Email", [validators.Email()])
    password = PasswordField("Password", [validators.Length(min=6)])
    is_admin = BooleanField("Admin")
    profile_image = StringField("Profile Image")


class UserEditForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField("Username", [validators.Length(min=4, max=25)])
    mail = StringField("Email", [validators.Email()])
    password = PasswordField("Password")
    is_admin = BooleanField("Admin")
    profile_image = StringField("Profile Image")


class UserAdmin(ModelView):
    form = UserEditForm
    create_form = UserCreateForm

    column_list = ["id", "username", "mail", "is_admin", "profile_image"]
    column_searchable_list = ["username", "mail"]
    column_filters = ["is_admin"]

    column_labels = {
        "username": "Nom d'utilisateur",
        "mail": "Email",
        "is_admin": "Administrateur",
        "profile_image": "Image de profil",
    }

    def on_model_change(self, form, model, is_created):
        if is_created or form.password.data:
            model.password = hash_password(form.password.data)


def init_admin(app, db):
    admin = Admin(app, name="Administration", template_mode="bootstrap4")
    admin.add_view(UserAdmin(User, db.session))
