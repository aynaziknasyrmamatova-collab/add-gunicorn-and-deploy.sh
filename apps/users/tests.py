from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class AuthenticationTokenTests(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "password123"
        self.email = "testuser@example.com"
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_register_returns_tokens(self):
        url = reverse("user-register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "strongpassword123",
            "password2": "strongpassword123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tokens", response.data)
        self.assertIn("token", response.data["tokens"])
        self.assertIn("jwt", response.data["tokens"])

    def test_drf_token_login_and_authenticated_profile(self):
        login_url = reverse("token-login")
        response = self.client.post(login_url, {"username": self.username, "password": self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token_key = response.data.get("token")
        self.assertTrue(bool(token_key))

        # Access profile with Token
        profile_url = reverse("user-profile")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token_key}")
        profile_response = self.client.get(profile_url)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data["username"], self.username)

        # Logout with Token
        logout_url = reverse("token-logout")
        logout_response = self.client.post(logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_jwt_login_and_refresh(self):
        login_url = reverse("jwt-login")
        response = self.client.post(login_url, {"username": self.username, "password": self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data.get("access")
        refresh_token = response.data.get("refresh")
        self.assertTrue(bool(access_token))
        self.assertTrue(bool(refresh_token))

        # Access profile with JWT Bearer
        profile_url = reverse("user-profile")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        profile_response = self.client.get(profile_url)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data["username"], self.username)

        # Refresh access token
        refresh_url = reverse("jwt-refresh")
        refresh_response = self.client.post(refresh_url, {"refresh": refresh_token})
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)

    def test_swagger_endpoints(self):
        schema_res = self.client.get(reverse("schema"))
        self.assertEqual(schema_res.status_code, status.HTTP_200_OK)

        swagger_res = self.client.get(reverse("swagger-ui"))
        self.assertEqual(swagger_res.status_code, status.HTTP_200_OK)

        redoc_res = self.client.get(reverse("redoc"))
        self.assertEqual(redoc_res.status_code, status.HTTP_200_OK)

