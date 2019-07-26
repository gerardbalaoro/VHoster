"""Site Errors"""


class SiteError(Exception):
    """Site Error"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SiteExistsError(SiteError):
    """Site Exists Error"""

    def __init__(self, domain='', path=''):
        if domain:
            self.message = "A site has already been registered to: %s" % domain
        elif path:
            self.message = "A site has already been linked to path: %s" % path
        else:
            self.message = 'Site already exists'


class SiteNotFoundError(SiteError):
    """Site Not Found Error"""

    def __init__(self, domain='', path=''):
        if domain:
            self.message = "No site is registered to: %s" % domain
        elif path:
            self.message = "No site linked to path: %s" % path
        else:
            self.message = 'Site not found'
