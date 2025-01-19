from flask import flash
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, validators

from app.db.models import User
from app.utils import hash_password


class UserCreateForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField("Username", [validators.Length(min=4, max=25), validators.DataRequired()])
    mail = StringField("Email", [validators.Email(), validators.DataRequired()])
    password = PasswordField("Password", [validators.Length(min=6), validators.DataRequired()])
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

    def create_model(self, form):
        try:
            with self.session.no_autoflush:
                if self.session.query(User).filter_by(username=form.username.data).first():
                    flash("Ce nom d'utilisateur est déjà utilisé", "error")
                    return False

                if self.session.query(User).filter_by(mail=form.mail.data).first():
                    flash("Cette adresse email est déjà utilisée", "error")
                    return False

                model = self.model()
                form.populate_obj(model)
                model.password = hash_password(form.password.data)
                self.session.add(model)
                self._on_model_change(form, model, True)
                self.session.commit()
                return model
        except Exception as ex:
            self.session.rollback()
            flash(str(ex), "error")
            return False

    def update_model(self, form, model):
        try:
            with self.session.no_autoflush:
                existing_user = self.session.query(User).filter_by(username=form.username.data).first()
                if existing_user and existing_user.id != model.id:
                    flash("Ce nom d'utilisateur est déjà utilisé", "error")
                    return False

                existing_email = self.session.query(User).filter_by(mail=form.mail.data).first()
                if existing_email and existing_email.id != model.id:
                    flash("Cette adresse email est déjà utilisée", "error")
                    return False

                form.populate_obj(model)
                if form.password.data:
                    model.password = hash_password(form.password.data)
                self._on_model_change(form, model, False)
                self.session.commit()
                return True
        except Exception as ex:
            self.session.rollback()
            flash(str(ex), "error")
            return False
