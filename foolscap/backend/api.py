"""Handling requests to server."""

import re
import sys
import logging

import requests


class API:

    def __init__(self, auth_handler=None, parser=None,
                 protocol='https://', host='0.0.0.0',
                 version='/v1', verify=True):
        self.auth = auth_handler
        self.protocol = protocol
        self.host = host
        self.version = version
        self.verify = verify
        self.parser = parser

    @property
    def get_note_content(self):
        return bind_method(
            api=self,
            path='/notes/{note_id}/content',
            payload_type='note',  # ?
            allowed_param=['note_id'],
        )

    def put_note_content(self, *args, **kwargs):
        return bind_method(
            api=self,
            path='/notes/{note_id}/content',
            method='PUT',
            payload_type='note',
            allowed_param=['note_id', 'content'],
        )(*args, **kwargs)

    @property
    def get_note_json(self):
        return bind_method(
            api=self,
            path='/notes/{note_id}/json',
            payload_type='json',
            allowed_param=['note_id'],
        )

    def put_note_json(self, *args, **kwargs):
        return bind_method(
            api=self,
            path='/notes/{note_id}/json',
            method='PUT',
            payload_type='json',
            allowed_param=['note_id', 'json'],
        )(*args, **kwargs)

    @property
    def get_meta_data(self):
        return bind_method(
            api=self,
            path='/meta_data/load',
            payload_type='json',
            allowed_param=[],
        )

    @property
    def delete_note(self):
        return bind_method(
            api=self,
            path='/notes/{note_id}',
            method='DELETE',
            payload_type='note',
            allowed_param=['note_id'],
        )


log = logging.getLogger('foolscap.api')
re_path_template = re.compile('{\w+}')


def bind_method(**config):

    class Method:
        api = config['api']
        path = config['path']
        payload_type = config.get('payload_type', None)
        payload_list = config.get('payload_list', False)

        method = config.get('method', 'GET')

        allowed_param = config.get('allowed_param', [])
        session = requests.Session()

        def __init__(self, args, kwargs):
            api = self.api

            self.post_data = kwargs.pop('post_data', None)

            self.api_host = api.host
            self.api_root = api.version
            self.api_protocol = api.protocol

            self.parser = kwargs.pop('parser', api.parser)

            self.build_parameters(args, kwargs)
            self.build_path()

        def build_parameters(self, args, kwargs):
            self.session.params = {}
            for idx, arg in enumerate(args):
                if arg is None:
                    continue
                try:
                    # Tweepy converts string to utf-8
                    self.session.params[self.allowed_param[idx]] = arg
                except IndexError:
                    raise IndexError('Too many parameters supplied!')

            for k, arg in kwargs.items():
                if arg is None:
                    continue
                if k in self.session.params:
                    raise Exception('Multiple values for parameter %s supplied!' % k)

                # Also converted to utf-8
                self.session.params[k] = arg

            log.debug('PARAMS: %r', self.session.params)

        def build_path(self):
            """Replaces path variables with their value."""
            for variable in re_path_template.findall(self.path):
                name = variable.strip('{}')

                try:
                    # value = quote(self.session.params[name])
                    value = self.session.params[name]
                except KeyError:
                    raise KeyError('No parameter value found for: %s' % name)
                del self.session.params[name]
                self.path = self.path.replace(variable, value)

        def execute(self):
            # Build request URL
            url = self.api_root + self.path
            full_url = self.api_protocol + self.api_host + url

            retries_performed = 0
            while retries_performed < 1:
                auth = None
                if self.api.auth:
                    auth = self.api.auth.apply_auth()

                try:
                    resp = self.session.request(self.method,
                                                full_url,
                                                data=self.post_data,
                                                auth=auth)
                except Exception as e:
                    raise Exception('Failed to send: %s' % e, sys.exc_info()[2])

                if resp.status_code == 200:
                    break
                else:
                    raise Exception(resp.text, resp.status_code)

            # result = self.parser.parse(self, resp.text)
            return resp.text

    def _call(*args, **kwargs):
        method = Method(args, kwargs)
        if kwargs.get('create'):
            return method
        else:
            return method.execute()

    return _call
