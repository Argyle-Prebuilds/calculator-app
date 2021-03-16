import base64
import os

import requests

from api import settings
from api.utils.exceptions import ArgyleException
from api.utils.exceptions import ArgyleIntegration
from api_keys.models import ArgyleAPIKeys

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

    def _get_merged_results_from_url(self, url, params, limit=100):
        """
            Because a Payouts endpoint gives us paginated list, we need to fetch for all existing pages
        """

        results = []
        exist_next_page = True
        offset = 0

        while exist_next_page:

            response = requests.get(url, headers=self.get_headers(), params={**params, 'limit': limit,
                                                                             'offset': offset})
            data = response.json()

            if response.status_code == 400:
                raise ArgyleException()

            if 'detail' in data:
                raise ArgyleException(data['detail'])

            results += data['results']
            exist_next_page = bool(data["next"])
            offset += limit

        return results

    def get_all_payouts_by_company_and_date(self, user_id, from_start_date=None, to_start_date=None, employer=None,
                                            limit=100):
        """
        Lists all payouts.

        @param user_id: str, user_id
        @param from_start_date: str, The timestamp the payouts should be retrieved from
        @param to_start_date: str, The timestamp the payouts should be retrieved from
        @param employer: str, The payouts employer
        @param limit: str, The number of payouts objects to be returned. The default is 10.
        @return:

        """
        url = get_argyle_api_url() + '/payouts'

        params = {
            'user': str(user_id),
            'from_start_date': str(from_start_date) if from_start_date else None,
            'to_start_date': str(to_start_date) if to_start_date else None,
        }

        results = self._get_merged_results_from_url(url, params)
        # Needed filter by company:
        results = filter(lambda result: result['employer'] == employer, results)

        return results

    def get_all_payouts(self, user_id, from_start_date=None, to_start_date=None):
        """
        Lists all payouts.

        @param user_id: str, user_id
        @param from_start_date: str, The timestamp the payouts should be retrieved from
        @param to_start_date: str, The timestamp the payouts should be retrieved from
        @param limit: str, The number of payouts objects to be returned. The default is 10.
        @return:

        """
        url = get_argyle_api_url() + '/payouts'

        params = {
            'user': str(user_id),
            'from_start_date': str(from_start_date),
            'to_start_date': str(to_start_date),
        }
        results = self._get_merged_results_from_url(url, params)

        return results

    def get_all_employments(self, user_id):
        """
        Lists all employments.

        @param offset: int
        @param user_id: str, user_id
        @param limit: int, The number of employments objects to be returned. The default is 10.
        @return:

        """
        url = get_argyle_api_url() + '/employments'

        params = {
            'user': str(user_id),
        }

        results = self._get_merged_results_from_url(url, params)

        return results

    def get_employments(self, user_id, offset=0, limit=10):
        """
        Lists all employments.

        @param offset: int
        @param user_id: str, user_id
        @param limit: int, The number of employments objects to be returned. The default is 10.
        @return:

        """
        url = get_argyle_api_url() + '/employments'

        params = {
            'user': str(user_id),
            'limit': limit,
            'offset': offset
        }
        response = requests.get(url, headers=self.get_headers(), params=params)
        data = response.json()

        if 'detail' in data:
            raise ArgyleException(data['detail'])

        return data
