#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

"""The Application Interface"""

import logging
import asyncio
import json
from aiohttp import web

from sanic import Sanic
from sanic.response import json
from sanic_jwt import exceptions
from sanic_jwt import Initialize
from sanic.views import HTTPMethodView
from sanic_jwt.decorators import protected

from sanic.blueprints import Blueprint


log = logging.getLogger(__name__)

#blueprint = Blueprint("")


class User(object):

    def __init__(self, id, username, password):
        self.user_id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "User(id='{}')".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}

users = []
username_table = {u.username: u for u in users}

async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    username_table = {u.username: u for u in users}
    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if password != user.password:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user


class AuthApi(HTTPMethodView):
    """Application Interface for RPS"""

    def __init__(self, loop=None, port=8080, site=None, amqp=None,
                 id=None, username=None, password=None):
        loop = loop or asyncio.get_event_loop()

        self.app = Sanic(__name__)

        self.site = site
        self.port = port
        self.amqp = amqp
        self.db = {}

        users.append(User(id, username, password))

        self.app.add_route(self.index, "/", methods=['GET'],
                           strict_slashes=True)
        self.app.add_route(self.as_view(), "/v2/events",
                           strict_slashes=True)

    def start(self):
        Initialize(self.app, authenticate=authenticate)
        self.app.run(host='0.0.0.0', port=self.port)

    async def index(self, request):
        return json({
            'info': '000000000000',
            'amqp': '111111111111',
            'api_version': 'V1',
            'api': ['v2/system'],
            'modules version': 'IPP-I'})

    def get_system(self):
        return [
            {
                "version": "1.1.0",
                "id": 201,
                "type": "alarm",
                "system": 1,
                "segment": 2,
                "offset": 0.5,
                "timestamp": "2018-01-01 08:30:45",
                "remark": "reserve"},
            {
                "version": "1.1.0",
                "id": 208,
                "type": "alarm",
                "system": 3,
                "segment": 9,
                "offset": 0.8,
                "timestamp": "2018-01-01 09:39:01",
                "remark": "reserve"}
        ]

    decorators = [protected()]
    async def get(self, request):
        data = self.get_system()
        return json(data)


if __name__=="__main__":
    auth = AuthApi(id=1, username="user1", password="abcxyz")
    auth.start()
