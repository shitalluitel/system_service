import json
import uuid

from flask import g, sessions, session
from flask_restful import Resource, reqparse

from system_service import app
from system_service.api.v1.common.errors import InternalServerError, DeviceNotExistsError
from system_service.api.v1.resources.users.models import User as UserModel
from system_service.app import db


class User(Resource):
    def put(self, nic_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        instance = self.__update_device(nic_id, parser.parse_args())
        return instance, 200

    def __update_device(self, _id, _request):
        try:
            instance = UserModel.objects(id=_id).update(
                name=_request.get('name')
            )
            return instance
        except Exception:
            raise InternalServerError(
                "[API] Unable to update given data."
            )


class Users(Resource):
    def get(self):
        device = UserModel.objects.all()
        response_data = json.loads(device.to_json())
        return response_data


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        return {'session_cookie': self.__verify_user(parser.parse_args())}

    def __verify_user(self, _request):
        username = _request.get('username')
        password = _request.get('password')
        user = UserModel.objects(username=username).first()

        if not user or not user.verify_password(password):
            return False
        g.user = user
        session['uid'] = uuid.uuid4()
        return str(session.get('uid'))
