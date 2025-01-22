from flask import request
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, validators

from app.admin.view.authView import SecureModelView
from app.db.models import Collection, User


class CollectionForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField("Nom", [validators.Length(min=1, max=100), validators.DataRequired()])
    picture = StringField("Image")
    user_id = SelectField("Utilisateur", coerce=int, validators=[validators.DataRequired()])


class CollectionAdmin(SecureModelView):
    form = CollectionForm
    column_list = ["id", "name", "picture", "user.username"]
    column_labels = {"name": "Nom", "picture": "Image", "user.username": "Utilisateur"}
    column_searchable_list = ["name", "user.username"]
    column_filters = ["user.username"]

    def _populate_user_choices(self, form):
        form.user_id.choices = [(user.id, user.username) for user in User.query.order_by(User.username).all()]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        self._populate_user_choices(form)
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        self._populate_user_choices(form)
        return form

    def validate_form(self, form):
        if not super().validate_form(form) or not hasattr(form, "name") or not hasattr(form, "user_id"):
            return False

        current_id = request.args.get("id", None, type=int)
        query = Collection.query.filter(Collection.name == form.name.data, Collection.user_id == form.user_id.data)

        if current_id:
            query = query.filter(Collection.id != current_id)

        if query.first():
            form.name.errors.append("Une collection avec ce nom existe déjà pour cet utilisateur.")
            return False

        return True
