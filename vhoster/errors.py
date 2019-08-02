"""Site Errors"""

class SiteError(Exception):
    """Site Error
    
    Arguments:
        message {str}
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SiteExistsError(SiteError):
    """Site Exists Error
    
    Keyword Arguments:
        domain {str} -- site domain (default: {''})
        path {str} -- site path (default: {''})
    """

    def __init__(self, domain='', path=''):
        import os

        if domain:
            self.message = "A site has already been registered to '%s'" % domain
        elif path:
            self.message = "A site has already been linked to path '%s'" % os.path.abspath(path)
        else:
            self.message = 'Site already exists'


class SiteNotFoundError(SiteError):
    """Site Not Found Error
    
    Keyword Arguments:
        domain {str} -- site domain (default: {''})
        path {str} -- site path (default: {''})
    """

    def __init__(self, domain='', path=''):
        import os
        
        if domain:
            self.message = "No site registered to '%s'" % domain
        elif path:
            self.message = "No site linked to path '%s'" % os.path.abspath(path)
        else:
            self.message = 'Site not found'


class InvalidConfigError(Exception):
    """Invalid Config Error
    
    Keyword Arguments:
        message {str} -- (default: {''})
    """

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return 'Invalid configuration file' + (' (%s)' % self.message if self.message else '')
