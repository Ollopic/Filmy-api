import ast
import json

from flask import request
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, validators
from wtforms.validators import ValidationError

from app.db.models import Person


def validate_json(form, field):
    if field.data:
        try:
            data = json.loads(field.data)
            if not isinstance(data, dict):
                raise ValidationError("Le contenu doit être un objet JSON")
        except json.JSONDecodeError:
            try:
                data = ast.literal_eval(field.data)
                if not isinstance(data, dict):
                    raise ValidationError("Le contenu doit être un objet JSON")
                field.data = json.dumps(data)
            except (ValueError, SyntaxError):
                raise ValidationError("Le contenu doit être un objet JSON")


class PersonForm(FlaskForm):
    class Meta:
        csrf = False

    id_tmdb = IntegerField("ID TMDB", [validators.DataRequired()])
    data = TextAreaField("Données JSON", [validators.DataRequired(), validate_json])


class PersonAdmin(ModelView):
    form = PersonForm

    column_list = ["id", "id_tmdb", "name", "data"]
    column_labels = {"id_tmdb": "ID TMDB", "name": "Nom", "data": "Données JSON"}

    column_searchable_list = ["id_tmdb"]
    column_filters = ["id_tmdb"]

    can_view_details = True
    details_modal = True

    def _get_name(self, context, model, name):
        try:
            return model.data.get("name", "N/A") if isinstance(model.data, dict) else "N/A"
        except AttributeError:
            return "N/A"

    column_formatters = {"name": _get_name}

    def validate_form(self, form):
        if not super().validate_form(form) or not hasattr(form, "id_tmdb"):
            return False

        current_id = request.args.get("id", None, type=int)
        query = Person.query.filter(Person.id_tmdb == form.id_tmdb.data)

        if current_id:
            query = query.filter(Person.id != current_id)

        if query.first():
            form.id_tmdb.errors.append("Une personne avec cet ID TMDB existe déjà.")
            return False

        return True

    def on_model_change(self, form, model, is_created):
        if isinstance(model.data, str):
            model.data = json.loads(model.data)
