#! /usr/bin/env python
#
# Mixpanel, Inc. -- http://mixpanel.com/
#
# Python API client library to consume mixpanel.com analytics data.
#
# Copyright 2010-2013 Mixpanel, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import urllib
import urllib2
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

try:
    import json
except ImportError:
    import simplejson as json

class Mixpanel(object):

    ENDPOINT = 'https://mixpanel.com/api'
    VERSION = '2.0'

    def __init__(self, api_secret):
        self.api_secret = api_secret

    def request(self, methods, params, http_method='GET', format='json'):
        """
            methods - List of methods to be joined, e.g. ['events', 'properties', 'values']
                      will give us http://mixpanel.com/api/2.0/events/properties/values/
            params - Extra parameters associated with method
        """
        params['format'] = format

        request_url = '/'.join([self.ENDPOINT, str(self.VERSION)] + methods)
        # request_url = '{}/{}'.format(
        #     '/'.join([self.ENDPOINT, str(self.VERSION)]),
        #     'export')
        if http_method == 'GET':
            data = None
            request_url = request_url + '/?' + self.unicode_urlencode(params)
        else:
            data = self.unicode_urlencode(params)

        # headers = {'Authorization': 'Basic {encoded_secret}'.format(
        #     encoded_secret=base64.b64encode(self.api_secret))}
        # request = urllib2.Request(request_url, data, headers)
        # response = urllib2.urlopen(request, timeout=120)
        print request_url
        # return json.loads(response.read())
        response = requests.get(url=request_url, auth=HTTPBasicAuth(self.api_secret, ''))
        return json.loads(response.content)

        # data = response.read()
        # return [json.loads(line) for line in data.split('\n')[:-1]]

    def unicode_urlencode(self, params):
        """
            Convert lists to JSON encoded strings, and correctly handle any
            unicode URL parameters.
        """
        if isinstance(params, dict):
            params = params.items()
        for i, param in enumerate(params):
            if isinstance(param[1], list):
                params[i] = (param[0], json.dumps(param[1]),)

        return urllib.urlencode(
            [(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params]
        )

if __name__ == '__main__':
    api = Mixpanel(settings.MIXPANEL_SECRET_KEY)
    data = api.request(['events'], {
        'event': ['pages'],
        'unit': 'hour',
        'interval': 24,
        'type': 'general'
    })
    print data
