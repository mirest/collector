from tests.base import BaseTestCase

from .models import User, UserManager


class TestUsers(BaseTestCase):

    def test_login_is_successfull(self):
        response = self.post_put_response('users:login', self.user_data())
        self.assertEqual(201, response.status_code)

    def test_login_fails(self):
        response = self.post_put_response(
            'users:login', self.user_data(username="kimb"))
        self.assertEqual(400, response.status_code)

    def test_get_user_succeeds(self):
        response = self.get_delete_response('users:user')
        self.assertEqual(200, response.status_code)

    def test_create_user_fails(self):
        response = self.post_put_response('users:tenants', self.user_data(
            email='kk@kd.com', name='dimo', phonenumber="3", username='asdf'))
        self.assertEqual(201, response.status_code)

    def test_user_manager_creates_user_succeds(self):
        manager = UserManager()
        manager.model = User
        user = manager.create_superuser(
            **self.user_data(email='kk@kd.com', username='5678'))
        assert user.__str__() == user.email
        assert isinstance(user, User)

    def test_user_manager_creates_user_fails(self):
        manager = UserManager()
        manager.model = User
        with self.assertRaises(ValueError) as context:
            manager.create_superuser(
                **self.user_data(username='5678', email=None))
        self.assertTrue(
            'The given email must be set' in str(context.exception))

    @classmethod
    def user_data(self, **kwargs):
        data = {
            'username': "kimbugp",
            'password': 123,
            **kwargs
        }
        return data
