from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

from github import Github
from os import getenv

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        # Get parameters either from the task parameters or environment variables
        api_key = kwargs.get('api_key', getenv('GITHUB_API_KEY'))
        login = kwargs.get('login')

        g = Github(api_key)

        try:
            keys = [key.key for key in g.get_user(login).get_keys()]
            # ret.append({attr: getattr(key, '_' + attr).value  for attr in ['id', 'key', 'title', 'url', 'verified']})
        except Exception as e:
            raise AnsibleError("Failed to get User's keys: {error}".format(error=str(e)))
        return keys
