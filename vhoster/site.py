from .config import Config
from .server import Server
from .certificate import Certificate
from .errors import *
from .helpers import *
from copy import deepcopy
import os

class SiteStore:  
    """Site storage provider class"""
    

    def __init__(self, config: Config):
        """Initialize store instance
        
        Arguments:
            config {Config} -- configuration instance
        """
        self.__config = config
        self.__store = self.__config.get('sites')

    def all(self):
        """Get all sites
        
        Returns:
            list
        """
        return deepcopy(self.__store)

    def create(self, **kwargs):
        """Create new site with given parameters and data
        
        Returns:
            int -- ID of newly created site
        """
        self.__store.append(kwargs)
        self.__config.save()
        return len(self.__store) - 1

    def find(self, id=None, domain=None, path=None, tld=None, ignore=None):
        """Find existing site using any given parameters                
        
        Keyword Arguments:
            id {int} -- site ID (default: {None})
            domain {str} -- site domain (default: {None})
            path {str} -- site path (default: {None})
            tld {str} -- site TLD (default: {None})
            ignore {int} -- ignore site with this ID
        
        Returns:
            tuple -- site id and data, (None, None) if not found
        """
        if id in range(len(self.__store)):
            return id, deepcopy(self.__store[id])

        for i, site in enumerate(self.__store):
            if (site['path'] == path) or (site['domain'] == domain and site.get('tld', tld)) == tld:
                if ignore == None or ignore != i:
                    return i, deepcopy(site)

        return None, None

    def update(self, id: int, **kwargs):
        """Update existing site values with specified parameters
        
        Arguments:
            id {int} -- site ID

        Returns:
            int -- ID of updated site 
        """
        if not id in range(len(self.__store)):
            raise rootError('Cannot find site with ID: %s' % id)

        self.__store[id] = {**self.__store[id], **kwargs}
        self.__config.save()
        return id

    def replace(self, id=None, **kwargs):
        """Create new or update existing site
        
        Keyword Arguments:
            id {int} -- ID of site to update, set to 'None' to create new (default: {None})

        Returns:
            int -- ID of replaced site
        """
        return self.create(**kwargs) if id == None else self.update(id, **kwargs)

    def delete(self, id: int):
        """Delete existing site given ID
        
        Arguments:
            id {int} -- site ID
        """
        if id not in range(len(self.__store)):
            raise rootError('Cannot find site with ID: %s' % id)

        del self.__store[id]
        self.__config.save()
        return id


class Site:
    """Virtual Site Object"""

    # Initalize default values
    __domain, __path, __secure = None, None, False
    __root, __tld, __share = '', None, False

    def __init__(self, config: Config, domain=None, path=None, root='', secure=False, tld=None, id=None):
        """Initialize Host class instance
        
        Arguments:
            config {Config} -- configuration instance
        
        Keyword Arguments:
            domain {str} -- site domain name (default: {None})
            path {str} -- path to site directory (default: {None})
            root {str} -- site document root (if different from path) (default: {''})
            secure {bool} -- enable SSL/TLS configuration (default: {False})
            tld {[type]} -- top-level domain (overrides default) (default: {None})
            id {[type]} -- site ID (for existing sites, should be used alone) (default: {None})
        """
        self.config = config
        self.store = SiteStore(config)
        self.server = Server(config)

        self.__crumbs = {}
        path = os.path.abspath(path) if path != None else path
        self.__id, site = self.store.find(id, domain, path, tld)

        if self.id != None:
            self.__domain = site['domain']
            self.__path = site['path']
            self.__root = site.get('root', '')
            self.__secure = site.get('secure', False)
            self.__tld = site.get('tld', None)
            self.__share = site.get('share', False)
        else:
            self.domain = domain
            self.path = path
            self.root = root
            self.secure = secure
            self.tld = tld

    def __repr__(self):
        """Return the canonical representation of this object

        Returns:
            str
        """
        return "%s(domain='%s', path='%s', root='%s', secure=%s, tld=%s)" % (
            self.__class__.__name__, self.domain, self.path, self.root, str(self.secure), str(self.tld))

    def __str__(self):
        """Return the string representation of this object

        Returns:
            str
        """
        return str(self.toDict())

    def list(self):
        """Get all sites from store
        
        Returns:
            list -- list of sites as instance of Host()
        """
        return [Site(self.config, id=id) for id, site in enumerate(self.store.all())]

    def toDict(self):
        """Return site data as dictionary
        
        Returns:
            dict
        """
        return {
            'domain': self.domain,
            'path': self.path,
            'root': self.root,
            'secure': self.secure,
            'tld': self.tld,
            'share': self.share
        }

    def find(self, domain=None, path=None, tld=None):
        return Site(self.config, domain, path, tld=tld)

    def save(self):
        """Save site to store and write configurations
        
        Raises:
            TypeError: Required properties must not be None or an empty string
        
        Returns:
            bool
        """
        if not self.domain or not self.path:
            raise TypeError(
                "Property 'domain' or 'path' must not be None or an empty string")
            return False

        data = self.toDict()        

        if self.isDirty():
            self.removeConfiguration()
            self.removeDnsEntry()
            self.removeCertificate()      
            self.__crumbs = {}

        self.store.replace(self.id, **data)
        self.writeConfiguration()
        self.writeDnsEntry()
        self.createCertificate()
        return True

    def exists(self):
        """Check if site already exists
        
        Returns:
            bool
        """
        return True if self.id != None else False

    def delete(self):
        """Delete site from store and remove configurations
        
        Returns:
            bool
        """
        if self.id == None:
            return False

        self.store.delete(self.id)
        self.removeConfiguration()
        self.removeDnsEntry()
        self.removeCertificate()
        self.__crumbs = {}
        self.__id = None
        return True

    def writeConfiguration(self):
        """Create Apache configuration files for this site"""
        confPath = self.confPath()
        with open(confPath, 'w+') as f:
            conf = template(
                'site.conf', 
                url=self.hostName(), 
                path=self.trueRoot(), 
                cert=self.certPath(), 
                certkey=self.certKeyPath(),
                secure=self.secure,
                share=get_free_tcp_port() if self.share else False
            )
            f.write(conf)
            success(os.path.basename(confPath), title='Created virtual host configuration file')

        with open(self.config.get('apache.conf'), 'r+') as f:
            content = f.read()
            f.write('\nInclude "%s"' % confPath)
            f.truncate()
            echo('Updated apache configuration file')

    def removeConfiguration(self):
        """Remove Apache configuration files for this site"""
        confPath = self.confPath(useCrumbs=self.isDirty())
        if os.path.exists(confPath):
            os.remove(confPath)
            success(os.path.basename(confPath), title='Removed virtual host configuration file')

        with open(self.config.get('apache.conf'), 'r+') as f:
            content = []
            for line in f:
                if (line != 'Include "%s"' % confPath):
                    content.append(line)
            f.seek(0)
            f.write(''.join(content).strip())
            f.truncate()
            echo('Updated apache configuration file')

    def writeDnsEntry(self):
        """Write DNS entry for this site"""
        with open(self.config.get('dns.file'), 'r+') as f:
            content = f.read()
            f.write('\n127.0.0.1 %s #VirtualHost' % self.hostName())
            f.write('\n127.0.0.1 www.%s #VirtualHost' % self.hostName())
            f.truncate()
            echo('Updated DNS (hosts) file')
    
    def removeDnsEntry(self):
        """Remove DNS entry for this site"""
        hostName = self.hostName(useCrumbs=self.isDirty())
        with open(self.config.get('dns.file'), 'r+') as f:
            content = []
            for line in f:
                line = line.strip()
                if (line != '') and (not line in content):
                    if line not in ['127.0.0.1 %s #VirtualHost' % hostName, '127.0.0.1 www.%s #VirtualHost' % hostName]:
                        content.append(line)
            f.seek(0)
            f.write('\n'.join(content))
            f.truncate()
            echo('Updated DNS (hosts) file')

    def createCertificate(self, allowUnsecure=False):
        """Create site certificate files, if secure
        
        Arguments:
            allowUnsecure {bool} -- create certificate regardless of secure property
        """
        if self.secure or allowUnsecure:
            certPath, keyPath = self.certPath(), self.certKeyPath()
            self.certificate.create(certPath, keyPath)
            self.certificate.trust(certPath)

    def removeCertificate(self):
        """Remove site certificate files"""    
        certPath, keyPath = self.certPath(useCrumbs=self.isDirty()), self.certKeyPath(useCrumbs=self.isDirty())
        self.certificate.untrust(certPath)
        self.certificate.delete(certPath, keyPath)
    
    def isDirty(self):
        """Check if site properties has been modified

        Returns:
            bool
        """
        return bool(self.__crumbs) and self.exists()

    def confPath(self, useCrumbs=False):
        """Return path to site configuration file
        
        Keyword Arguments:
            useCrumbs {bool} -- use previous value (default: {False})
        
        Returns:
            str
        """     
        path = os.path.abspath(os.path.join(self.config.get(
            'paths.conf') or data_path('conf'), self.hostName(useCrumbs=useCrumbs) + '.conf'))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    def certPath(self, useCrumbs=False):
        """Return path to site certificate file
        
        Keyword Arguments:
            useCrumbs {bool} -- use previous value (default: {False})
        
        Returns:
            str
        """    
        path = os.path.abspath(os.path.join(self.config.get(
            'paths.certs') or data_path('certs'), self.hostName(useCrumbs=useCrumbs) + '.crt'))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    def certKeyPath(self, useCrumbs=False):
        """Return path to site certificate key file
        
        Keyword Arguments:
            useCrumbs {bool} -- use previous value (default: {False})
        
        Returns:
            str
        """    
        path = os.path.abspath(os.path.join(self.config.get(
            'paths.certs') or data_path('certs'), self.hostName(useCrumbs=useCrumbs) + '.key'))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    def hostName(self, useCrumbs=False):
        """Return site domain name with TLD
        
        Keyword Arguments:
            useCrumbs {bool} -- use previous value (default: {False})
        
        Returns:
            str
        """    
        domain = self.__crumbs.get('domain', self.domain) if useCrumbs else self.domain
        tld = self.trueTLD(useCrumbs=useCrumbs)
        return domain + ('.%s' % tld if tld else '')

    def url(self, useCrumbs=False):
        """Return full site url with protocol and TLD
        
        Keyword Arguments:
            useCrumbs {bool} -- use previous values (default: {False})
        
        Returns:
            str
        """    
        secure = self.__crumbs.get('secure', self.secure)
        return '%s://%s' % ('https' if secure else 'http', self.hostName(useCrumbs=useCrumbs))

    def trueTLD(self, useCrumbs=False):
        """Return site true TLD, uses default if tld property is None
        
        Keyword Arguments:
            useCrumbs {bool} -- use previous values (default: {False})

        Returns:
            str
        """
        tld = self.tld if self.tld != None else self.config.get('tld', 'test')
        return self.__crumbs.get('tld', tld) if useCrumbs else tld

    def trueRoot(self, useCrumbs=False):
        """Return site true document root
        
        Keyword Arguments:
            useCrumbs {bool} -- use previous values (default: {False})

        Returns:
            str
        """
        root = self.__crumbs.get('root', self.root) if useCrumbs else self.root
        path = self.__crumbs.get('path', self.path) if useCrumbs else self.path
        if root:
            return os.path.abspath(os.path.join(path, root))
        else:
            return os.path.abspath(path)

    @property
    def id(self):
        return self.__id

    @property
    def certificate(self):
        return Certificate(self.domain)

    @property
    def domain(self):
        return self.__domain

    @domain.setter
    def domain(self, domain):
        if self.store.find(domain=domain, tld=self.tld, ignore=self.id) != (None, None):
            raise SiteExistsError(domain=domain + '.' + str(self.trueTLD()))
        else:
            if not self.__crumbs.get('domain'):
                self.__crumbs['domain'] = self.domain
            self.__domain = domain

    @property
    def path(self):
        return os.path.abspath(self.__path) if self.__path != None else None

    @path.setter
    def path(self, path):
        if self.store.find(path=path, ignore=self.id) != (None, None):
            raise SiteExistsError(path=path)
        else:
            if not self.__crumbs.get('path'):
                self.__crumbs['path'] = self.path
            self.__path = path

    @property
    def secure(self):
        return self.__secure

    @secure.setter
    def secure(self, secure: bool):
        if not self.__crumbs.get('secure'):
            self.__crumbs['secure'] = self.secure
        self.__secure = secure

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, root):
        if not self.__crumbs.get('root'):
            self.__crumbs['root'] = self.root
        self.__root = root

    @property
    def tld(self):
        return self.__tld

    @tld.setter
    def tld(self, tld):
        if self.store.find(domain=self.domain, tld=tld, ignore=self.id) != (None, None):
            raise SiteExistsError(domain=self.domain + '.' + str(tld))
        else:
            if not self.__crumbs.get('tld'):
                self.__crumbs['tld'] = self.tld
            self.__tld = tld

    @property
    def share(self):
        return self.__share

    @secure.setter
    def secure(self, share: bool):
        if not self.__crumbs.get('share'):
                self.__crumbs['share'] = self.share
        self.__share = share
