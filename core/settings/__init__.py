import os
from .base import *

# Import the correct settings depending on if this is a dev or prod app
if os.getenv('environment') is not None:
    if os.environ['environment'] == 'production':
       from .production import *
    else:
      from .dev import *
else:
   from .dev import *
