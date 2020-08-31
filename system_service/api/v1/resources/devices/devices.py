import json
from datetime import datetime

from flask_restful import Resource, reqparse

from system_service.api.v1.common.errors import InternalServerError, DeviceNotExistsError, \
    DeviceLimitExceededExistsError
from system_service.api.v1.resources.devices.models import Device as DeviceModel
from system_service.api.v1.resources.users.models import User as UserModel


class Device(Resource):
    def delete(self, nic_id):
        self.__remove_device(nic_id)

        return None, 200

    @staticmethod
    def __remove_device(_id):
        try:
            _obj = DeviceModel.objects.get(id=_id)
        except Exception:
            raise DeviceNotExistsError
        _obj.delete()

    def put(self, nic_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        instance = self.__update_device(nic_id, parser.parse_args())
        return instance, 200

    @staticmethod
    def __update_device(_id, _request):
        try:
            instance = DeviceModel.objects(id=_id).update(
                name=_request.get('name')
            )
            return instance
        except Exception:
            raise InternalServerError(
                "[API] Unable to update given data."
            )


class Devices(Resource):
    def get(self):
        device = DeviceModel.objects.all()
        response_data = json.loads(device.to_json())
        return response_data

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('devices', type=list, location='json')
        self.__add_devices(parser.parse_args())
        return None, 200

    def __add_devices(self, _request):
        devices = [tuple(device.values()) for device in _request['devices']]
        try:
            DeviceModel.objects.insert(
                list(
                    map(
                        lambda data: DeviceModel(
                            name=data[0]
                        ),
                        devices
                    )
                )
            )
        except Exception as e:
            raise InternalServerError(
                "[API] One of the added devices is already exists.")


class AddDevicesToUser(Resource):
    def put(self, nic_id, user_id):
        instance = self.__update_device(nic_id, user_id)
        return instance, 200

    @staticmethod
    def __update_device(_id, user_id):
        instance = DeviceModel.objects(id=_id).first()
        assigned_to = getattr(instance, 'assigned_to') or 0
        if assigned_to >= 3:
            raise DeviceLimitExceededExistsError(
                '[API] This device has already been assigned to 3 users.'
            )
        instance.update(assigned_to=assigned_to + 1)

        try:
            UserModel.objects(id=user_id).update_one(push__devices=str(_id))
        except Exception as e:
            raise InternalServerError(
                "[API] Unable to add user to device."
            )


class About(Resource):
    def get(self):
        return {
            'version': '1.0.0',
            'server_time': str(datetime.utcnow())
        }
