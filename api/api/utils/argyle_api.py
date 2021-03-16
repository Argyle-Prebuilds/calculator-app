import base64
import os

import requests
from api.utils.exceptions import ArgyleException
from api.utils.exceptions import ArgyleIntegration
from api_keys.models import ArgyleAPIKeys

from api import settings

BASE_URL = os.environ['BASE_URL']


def get_argyle_api_url():
    api_settings = ArgyleAPIKeys.get_argyle_keys()

    return settings.SANDBOX_ARGYLE_API_URL if api_settings.is_sandbox_mode else settings.ARGYLE_API_URL


def convert_to_base64(text):
    text_base64 = text.encode('ascii')
    text_bytes = base64.b64encode(text_base64)
    return text_bytes.decode('ascii')


class ArgyleAPIWrapper:

    def get_argyle_credentials(self):
        keys = ArgyleAPIKeys.get_argyle_keys()

        if not keys:
            raise ArgyleIntegration('No Argyle credentials')

        if not keys.client_id or not keys.client_secret:
            return None

        credentials = f"{keys.client_id}:{keys.client_secret}"
        return credentials

    def get_headers(self):
        credentials = self.get_argyle_credentials()
        token = convert_to_base64(credentials)

        return {'content-type': 'application/json', 'Authorization': f"Basic {token}"}

    def fetch_argyle_profile(self, user_id):
        """
        Fetch Argyle Profile

        @param user_id: str, user_id
        @return:
        """
        url = get_argyle_api_url() + '/profiles'
        response = requests.get(url, headers=self.get_headers(), params={'user': user_id})

        data = response.json()
        if 'detail' in data:
            raise ArgyleException()

        if 'results' in data and len(data['results']):
            return data['results'][0]

        return None
