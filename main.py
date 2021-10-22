from os import getenv

from api_gateway.app import create_app

create_app().run(port=getenv("PORT"))
