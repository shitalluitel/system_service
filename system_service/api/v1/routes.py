from flask_restful import Api

from system_service.api.v1.common.authorization import is_authorized
from system_service.api.v1.common.errors import UnauthorizedError
from system_service.api.v1.resources.devices.devices import Devices, Device, AddDevicesToUser, About
from system_service.api.v1.resources.users.users import Users, User, Login
from system_service.app import logger, app


def create(api: Api):
    api_prefix = "/api/v1"
    device_id = "<string:nic_id>"
    user_id = "<string:user_id>"

    # for device
    api.add_resource(Devices, "{}/devices".format(api_prefix))
    api.add_resource(Device, "{}/devices/{}".format(api_prefix, device_id))
    api.add_resource(AddDevicesToUser, "{}/add/device/{}/user/{}".format(api_prefix, device_id, user_id))

    # for user
    api.add_resource(Users, "{}/users/".format(api_prefix))
    api.add_resource(User, "{}/users/{}".format(api_prefix, user_id))
    api.add_resource(Login, "{}/login".format(api_prefix))

    # about system
    api.add_resource(About, "{}/about".format(api_prefix))

    logger.info("[API] Loaded \'devices\' resource.")


@app.before_request
def authorize():
    if is_authorized() is False:
        raise UnauthorizedError
