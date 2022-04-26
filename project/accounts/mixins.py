from django.shortcuts import redirect
from django.conf import settings

class RedirectMixin:
    """
    Redirect to redirect_url if the test_func() method returns False.
    """

    redirect_url = settings.UNAUTHORIZED_URL

    def get_redirect_url(self):
        """
        Override this method to override the redirect_url attribute.
        """
        redirect_url = self.redirect_url
        if not redirect_url:
            raise ImproperlyConfigured(
                '{0} is missing the redirect_url attribute. Define {0}.redirect_url or override '
                '{0}.get_redirect_url().'.format(self.__class__.__name__)
            )
        return str(redirect_url)

    def test_func(self):
        raise NotImplementedError(
            '{0} is missing the implementation of the test_func() method.'.format(self.__class__.__name__)
        )

    def get_test_func(self):
        """
        Override this method to use a different test_func method.
        """
        return self.test_func

    def dispatch(self, request, *args, **kwargs):
        test_result = self.get_test_func()()
        if not test_result:
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)

class AdminRedirectMixin(RedirectMixin):
    def test_func(self):
        if self.request.user.roles.values_list('name', flat=True)[0] == "admin":
            return True

class FacultyRequiredMixin(RedirectMixin):
    def test_func(self):
        if self.request.user.roles.values_list('name', flat=True)[0] == "faculty":
            return True

class StudentRequiredMixin(RedirectMixin):
    def test_func(self):
        if self.request.user.roles.values_list('name', flat=True)[0] == "student":
            return True
