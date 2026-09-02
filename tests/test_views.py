from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')

        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'SuperSecretPassword123!'

        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password=self.password,
        )

    def test_signup_view_get(self):
        """Tests that the registration page loads correctly (HTTP 200)."""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile657/signup.html')

    def test_signup_view_post_success(self):
        """Tests that a new user is created when the form is filled out correctly."""
        data = {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
        }
        response = self.client.post(self.signup_url, data)

        user_exists = User.objects.filter(username=self.username).exists()
        self.assertTrue(user_exists)

        self.assertEqual(response.status_code, 302)

    def test_signup_view_post_missing_email(self):
        """Tests that registration fails if the required email field is missing/blank."""
        data = {
            'username': 'noemailuser',
            'email': '',  # Invalid: blank email
            'password1': self.password,
            'password2': self.password,
        }
        response = self.client.post(self.signup_url, data)

        # The page should return HTTP 200 and display the form again with an error message
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'], 'email', 'This field is required.'
        )

        user_exists = User.objects.filter(username='noemailuser').exists()
        self.assertFalse(user_exists)

    def test_signup_view_post_invalid_data(self):
        """Tests that no user is created if the form is invalid (e.g. no password)."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': '',  # Invalid: blank password
        }
        response = self.client.post(self.signup_url, data)

        # The page should return 200 (show the form again with error messages)
        self.assertEqual(response.status_code, 200)

        user_exists = User.objects.filter(username='newuser').exists()
        self.assertFalse(user_exists)

    def test_login_view_get(self):
        """Tests that the login page loads correctly (HTTP 200)."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'profile657/login.html')

    def test_login_view_post_success(self):
        """Tests login with correct credentials."""
        data = {'username': 'existinguser', 'password': self.password}
        response = self.client.post(self.login_url, data)

        # On successful login, we should be redirected (302)
        self.assertEqual(response.status_code, 302)

        # Verify that the user is actually logged into the session
        # Django saves the user's ID in the session during the '_auth_user_id'
        self.assertEqual(str(self.client.session['_auth_user_id']), str(self.user.pk))

    def test_login_view_post_failure(self):
        """Testing login with the wrong password."""
        data = {'username': 'existinguser', 'password': 'WrongPassword!'}
        response = self.client.post(self.login_url, data)

        # The page should reload (HTTP 200) and display error message
        self.assertEqual(response.status_code, 200)

        # Verify that the user is NOT logged in
        self.assertNotIn('_auth_user_id', self.client.session)


class UpdateEmailTests(TestCase):
    def setUp(self):
        self.update_email_url = reverse('update_email')
        self.password = 'SuperSecret123!'

        self.user = User.objects.create_user(
            username='testuser', email='old@example.com', password=self.password
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            email='taken@example.com',
            password='AnotherPassword123!',
        )

    def test_update_email_view_requires_login(self):
        """Tests that you have to be logged in to reach the view."""
        response = self.client.get(self.update_email_url)
        # Should be redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_update_email_view_get(self):
        """Tests that logged-in users can load the page correctly."""
        self.client.login(username='testuser', password=self.password)
        response = self.client.get(self.update_email_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile657/update_email.html')

    def test_update_email_success(self):
        """Trying to change the email address to a valid and available one."""
        self.client.login(username='testuser', password=self.password)

        data = {'email': 'new_awesome_email@example.com'}
        response = self.client.post(self.update_email_url, data)

        self.assertEqual(response.status_code, 302)

        # Retrieve the user from the database again and verify that it has been modified
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'new_awesome_email@example.com')

    def test_update_email_taken(self):
        """Tests that you can't switch to an email that's already in use."""
        self.client.login(username='testuser', password=self.password)

        # Try switching to the "otheruser"'s email address
        data = {'email': 'taken@example.com'}
        response = self.client.post(self.update_email_url, data)

        # Should return HTTP 200 and display the form again with error message
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'], 'email', 'The e-mailadress is wrong.'
        )

        # Make sure that the database was not changed
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'old@example.com')
