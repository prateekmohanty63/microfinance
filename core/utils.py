import random
import string

#===============================================================================
# Random string and Id generators
#===============================================================================

# 16 digit random string for Ids
def randomstr():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 16))

def randomlongstr():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 32))

# 64 digit random string for Public Links
def randomverylongstr():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 64))