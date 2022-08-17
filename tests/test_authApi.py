"""
Created on 2022-08-17

@author: th
"""
import tempfile
import uuid

from jpwidgets.bt5widgets import SimpleAuthApi
from tests.basetest import BaseTest


class TestSimpleAuthApi(BaseTest):
    """tests SimpleAuthApi"""

    def test_user_handling(self):
        """
        tests creation, deletion and auth of users
        """
        with tempfile.NamedTemporaryFile(suffix=".yaml") as fp:
            authApi = SimpleAuthApi(filepath=fp.name)
            test_params = [("alice", "pwd1234"), ("bob", "qdtvbo")]
            for param in test_params:
                with self.subTest("test user creation", param=param):
                    user, pwd = param
                    authApi.addUser(name=user, password=pwd)
                    self.assertTrue(authApi.existsUser(user))
                    self.assertTrue(authApi.isAuthenticated(user, pwd))
                with self.subTest("test user session login", param=param):
                    user, pwd = param
                    sessionId = str(uuid.uuid4())
                    authApi.login(sessionId, user)
                    self.assertTrue(authApi.isLoggedIn(sessionId=sessionId))
                    authApi.logout(sessionId=sessionId)
                    self.assertFalse(authApi.isLoggedIn(sessionId))
                with self.subTest("test user session login", param=param):
                    user, pwd = param
                    authApi.removeUser(name=user)
                    self.assertFalse(authApi.existsUser(name=user))

    def test_fileLoading(self):
        """tests reloading user information from file"""
        with tempfile.NamedTemporaryFile(suffix=".yaml") as fp:
            test_user = [("alice", "pwd1234"), ("bob", "qdtvbo")]
            authApi = SimpleAuthApi(filepath=fp.name)
            for name, pwd in test_user:
                authApi.addUser(name, pwd)

            authApiReloaded = SimpleAuthApi(filepath=fp.name)
            for name, pwd in test_user:
                self.assertTrue(authApiReloaded.existsUser(name))
                self.assertTrue(authApiReloaded.isAuthenticated(name, pwd))
