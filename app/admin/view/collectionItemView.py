from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, validators
from wtforms.fields import DateField
from wtforms.validators import ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField

from app.admin.view.authView import SecureModelView
from app.db.models import Collection, Film, User


class CollectionItemForm(FlaskForm):
    class Meta:
        csrf = False

    state = SelectField(
        "État",
        choices=[("Physique", "Physique"), ("Numérique", "Numérique")],
        validators=[validators.DataRequired()],
    )
    borrowed = BooleanField("Emprunté", default=False)
    borrowed_at = DateField("Date d'emprunt", format="%Y-%m-%d", validators=[validators.Optional()])
    borrowed_by = StringField("Emprunté par", validators=[validators.Optional()])
    favorite = BooleanField("Favori", default=False)

    collection = QuerySelectField(
        "Collection",
        query_factory=lambda: Collection.query.all(),
        allow_blank=True,
        get_label="name",
    )

    user_id = SelectField("Utilisateur", coerce=int, validators=[validators.DataRequired()])
    film_id = SelectField("Film", coerce=int, validators=[validators.DataRequired()])


class CollectionItemAdmin(SecureModelView):
    form = CollectionItemForm

    column_list = [
        "id",
        "state",
        "borrowed",
        "borrowed_at",
        "borrowed_by",
        "favorite",
        "collection_name",
        "film_id",
        "user.username",
    ]
    column_labels = {
        "state": "État",
        "borrowed": "Emprunté",
        "borrowed_at": "Date d'emprunt",
        "borrowed_by": "Emprunté par",
        "favorite": "Favori",
        "collection_name": "Nom de la Collection",
        "film_id": "Film",
        "user.username": "Utilisateur",
    }

    column_searchable_list = ["state", "borrowed_by"]
    column_filters = ["state", "borrowed", "favorite", "collection_id", "film_id", "user_id"]

    def _populate_user_choices(self, form):
        form.user_id.choices = [(user.id, user.username) for user in User.query.order_by(User.username).all()]

    def _populate_film_choices(self, form):
        form.film_id.choices = [
            (film.id, film.data.get("original_title", "Titre inconnu"))
            for film in Film.query.order_by(Film.id_tmdb).all()
        ]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        self._populate_user_choices(form)
        self._populate_film_choices(form)
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        self._populate_user_choices(form)
        self._populate_film_choices(form)
        return form

    def _format_collection_name(view, context, model, name):
        if model.collection and model.collection.name:
            return model.collection.name
        return "N/A"

    def _get_movie_name(self, context, model, name):
        if model.film:
            return model.film.data.get("original_title", "N/A")
        return "N/A"

    column_formatters = {
        "collection_name": _format_collection_name,
        "film_id": _get_movie_name,
    }

    def validate_form(self, form):
        if not super().validate_form(form):
            return False

        if form.data.get("borrowed_at") and not form.data.get("borrowed"):
            form.borrowed.errors.append("La case 'Emprunté' doit être cochée si une date d'emprunt est spécifiée.")
            return False

        if form.data.get("borrowed_by") and not form.data.get("borrowed"):
            form.borrowed.errors.append("La case 'Emprunté' doit être cochée si un emprunteur est spécifié.")
            return False

        if form.data.get("borrowed") and not form.data.get("borrowed_at"):
            form.borrowed_at.errors.append("La date d'emprunt est requise si l'élément est marqué comme emprunté.")
            form.borrowed_by.errors.append("L'emprunteur est requis si l'élément est marqué comme emprunté.")
            return False

        return True

    def on_model_change(self, form, model, is_created):
        if form.borrowed_at.data and isinstance(form.borrowed_at.data, str):
            try:
                from datetime import datetime

                model.borrowed_at = datetime.strptime(form.borrowed_at.data, "%Y-%m-%d")
            except ValueError:
                raise ValidationError("Le format de la date d'emprunt doit être 'YYYY-MM-DD HH:MM:SS'.")
