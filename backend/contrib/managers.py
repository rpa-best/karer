import os
import requests

from rest_framework.exceptions import NotFound, ValidationError


class ApiManager:
    def __init__(self, url):
        self._url = url
        self._params = {}

    def filter(self, **kwargs):
        for key, value in kwargs.items():
            self._params[key] = value
        return self

    def fetch(self):
        return requests.get(self._url, params=self._params, auth=('career_api', 'Tarah067'), headers={'Authorization': 'Basic career_api:Tarah067'}).json()

    def get(self, pk):
        try:
            url = os.path.join(self._url, str(pk))
            return requests.get(url, params=self._params).json()
        except Exception as _exp:
            raise NotFound(detail=str(_exp))

    def create(self, data):
        try:
            return requests.post(self._url, data=data, params=self._params).json()
        except Exception as _exp:
            raise ValidationError(detail=str(_exp))

    def update(self, pk, data):
        try:
            url = os.path.join(self._url, str(pk))
            return requests.patch(url, data=data, params=self._params).json()
        except Exception as _exp:
            raise ValidationError(detail=str(_exp))
