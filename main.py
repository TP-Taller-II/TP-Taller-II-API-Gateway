from os import getenv
from api_gateway.app import create_app

#print(getenv("PORT"))
create_app().run(port=9999)
