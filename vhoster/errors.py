class SiteError(Exception):
    """Site Error"""

    def __init__(self, domain=''):
        self.message = 'Error on site ' + (str(domain) + ' ' if domain else '')

    def __str__(self):
        return self.message

class SiteExistsError(SiteError):
    """Site Exists Error"""

    def __init__(self, domain=''):
        self.message = 'Site ' + (str(domain) + ' ' if domain else '') + 'already exists'

    def __str__(self):
        return self.message

class SiteNotFoundError(SiteError):
    """Site Not Found Error"""

    def __init__(self, domain=''):
        self.message = 'Site ' + (str(domain) + ' ' if domain else '') + 'does not exist'

    def __str__(self):
        return self.message