from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def full_name(self):
        """Return user's full name.

        Returns:
            Another method.
        """
        return self.get_full_name()

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
