import json
from rest_framework.test import APIClient
from django_dynamic_fixture import G
# from userdata.models import UserProfile


class TestCaseMixin:
    # def _get_authenticated_client(self, user=None):
    #     client = APIClient()
    #     if not user:
    #         user = G(UserProfile).user
    #     client.force_authenticate(user=user)
    #
    #     return client

    def call_get_api(self, url, user, json_request=None, headers=None):
        client = APIClient()
        # client = self._get_authenticated_client(user)

        if headers is None:
            headers = {}

        response = client.get(url, {}, format='json', **headers)
        return response

    def call_post_api(self, url, json_request=None, headers=None):
        client = APIClient()
        # client = self._get_authenticated_client(user)

        if json_request is None:
            json_request = {}

        if headers is None:
            headers = {}

        response = client.post(url, json_request, format='json', **headers)
        return response

    def call_put_api(self, url, user=None, json_request=None, headers=None):
        client = APIClient()
        # client = self._get_authenticated_client(user)

        if json_request is None:
            json_request = {}

        if headers is None:
            headers = {}

        response = client.put(url, json_request, format='json', **headers)
        return response

    def call_patch_api(self, url, user=None, json_request=None, headers=None):
        client = APIClient()
        # client = self._get_authenticated_client(user)

        if json_request is None:
            json_request = {}

        if headers is None:
            headers = {}

        response = client.patch(url, json_request, format='json', **headers)
        return response

    def call_delete_api(self, url, user=None, json_request=None, headers=None):
        client = APIClient()
        # client = self._get_authenticated_client(user)

        if json_request is None:
            json_request = {}

        if headers is None:
            headers = {}

        response = client.delete(url, json_request, format='json', **headers)
        return response

    def get_response_dict(self, response_obj):
        """
        return the HTTP response json as a dict
        :param response_obj:
        :return:
        """
        return json.loads(response_obj._container[0].decode("utf"))

    def assert_dict_contains_subset(self, subset, superset):
        # https://stackoverflow.com/questions/9323749/python-check-if-one-dictionary-is-a-subset-of-another-larger-dictionary/9323769#9323769
        return all(item in superset.items() for item in subset.items())
