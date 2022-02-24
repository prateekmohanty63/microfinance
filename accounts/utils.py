from django.conf import settings
import string
import random

# Creates in initial username with random characters (not currently used)
def create_username(name):
        name = name.replace(" ", "")
        choices = string.ascii_letters + string.hexdigits
        choice = "".join(random.choice(choices) for _ in range(10))
        username = f'{name}{choice}'
        return username

def create_link(link_for: str):
    choice = string.ascii_letters + string.digits
    key = "".join(random.choice(choice) for _ in range(30))
    if link_for == 'sign-up':
        link = f"{settings.BASE_URL}verify?key={key}"
    elif link_for == 'reset-password':
        link = f"{settings.BASE_URL}forgot-password?key={key}"
    return link, key