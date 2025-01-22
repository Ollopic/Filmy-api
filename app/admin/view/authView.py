from flask import request
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import decode_token

from app.db.models import User


class SecureModelView(ModelView):
    def is_accessible(self):
        return self.is_admin()

    def is_admin(self):
        try:
            token = request.cookies.get("token")
            if not token:
                return False

            decoded_token = decode_token(token)
            current_user_id = decoded_token["sub"]

            user = User.query.get(current_user_id)
            return user and user.is_admin

        except Exception as e:
            print("Erreur:", str(e))
            return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return self.inaccessible_callback(name, **kwargs)
