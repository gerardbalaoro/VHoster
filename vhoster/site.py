from .config import Config
from .server import Server
from .errors import *
from .helpers import *
from . import stubs
from datetime import datetime, timedelta
import importlib_resources as resources

class Site:

    def __init__(self, config: Config):
        """Initialize site class instance
        
        Arguments:
            config {Config}
        """
        self.config = config
        self.server = Server(self.config)
        self.sites = self.config.get('sites')

    def list(self):
        """List all sites
        
        Returns:
            list -- list of sites
        """
        return self.sites

    def find(self, domain):
        """Get single site
        
        Arguments:
            domain {str} -- site domain name
        
        Returns:
            dict -- site data
        """
        return next((site for id, site in enumerate(self.sites) if site['domain'] == domain), None)

    def create(self, domain, path, secure=False):
        """Create new site
        
        Arguments:
            domain {str} -- site domain name
            path {str} -- path to document root
        
        Keyword Arguments:
            secure {bool} -- enable SSL (default: {False})
        
        Raises:
            SiteExistsError: site already exists
        
        Returns:
            dict -- site data
        """

        if self.find(domain) != None:
            raise SiteExistsError(domain)
            return False

        site = {'domain': domain, 'path': path, 'secure': secure}
        self.sites.append(site)
        self.config.save(True)
        self.writeConfiguration(**site)
        self.writeDnsEntry(site['domain'])
        self.restartServices()
        return site

    def delete(self, domain):
        """Delete existing site
        
        Arguments:
            domain {str} -- site domain name
        
        Raises:
            SiteNotFoundError: site not found
        
        Returns:
            bool
        """
        site = self.find(domain)
        if site == None:
            raise SiteNotFoundError(domain)
            return False

        self.removeConfiguration(site['domain'])
        self.removeDnsEntry(site['domain'])
        self.sites.remove(site)
        self.config.save(True)
        self.restartServices()
        return True

    def update(self, domain, config: dict):
        """Update existing site with given configuration
        
        Arguments:
            domain {str} -- site domain name
            config {dict} -- site configuration
        
        Raises:
            SiteNotFoundError: site not found
            SiteExistsError: site already exists
        
        Returns:
            dict -- site data
        """
        site = self.find(domain)
        if site == None:
            raise SiteNotFoundError(domain)
            return False

        for key, value in config.items():
            if key == 'domain' and self.find(value):
                raise SiteExistsError(value)
                return False
            site[key] = value

        self.config.save()
        self.removeConfiguration(site['domain'])
        self.removeDnsEntry(site['domain'])
        self.writeConfiguration(**site)
        self.writeDnsEntry(site['domain'])
        self.restartServices()
        return site

    def rename(self, oldDomain, newDomain):
        """Change site domain name
        
        Arguments:
            oldDomain {str} -- old domain name
            newDomain {str} -- new domain name
        
        Returns:
            dict -- site data
        """
        return self.update(oldDomain, {'domain': newDomain})

    def link(self, domain, path):
        """Link directory as root to existing site
        
        Arguments:
            domain {str} -- site domain name
            path {str} -- path to document root
        
        Returns:
            dict -- site data
        """
        return self.update(domain, {'path': path})

    def secure(self, domain):
        """Enable SSL and serve site over HTTPS
        
        Arguments:
            domain {str} -- site domain name
        
        Returns:
            dict -- site data
        """
        return self.update(domain, {'secure': True})

    def unsecure(self, domain):
        """Disable SSL and stop serving site over HTTPS
        
        Arguments:
            domain {str} -- site domain name
        
        Returns:
            dict -- site data
        """
        return self.update(domain, {'secure': False})

    def writeConfiguration(self, domain, path, secure=False):
        """Create Apache configuration files for given domain
        
        Arguments:
            domain {str} -- site domain name
            path {str} -- path to document root
        
        Keyword Arguments:
            secure {bool} -- enable SSL (default: {False})
        """
        os.makedirs(data_path('sites'), exist_ok=True)
        conf_path = data_path('sites', domain + '.conf')
        self.createSslCertificate(domain)
        with open(conf_path, 'w+') as f:
            stub = resources.read_text(stubs, 'secure-site.conf' if secure else 'site.conf')
            conf = str_replace(stub, {
                'SITE_URL': self.getHostName(domain), 
                'SITE_PATH': os.path.abspath(path),
                'SITE_CERT': data_path('certs', '%s.conf' % self.getHostName(domain)),
                'SITE_KEY': data_path('certs', '%s.key' % self.getHostName(domain))
            })              
            f.write(conf)

        with open(self.config.get('apache.conf'), 'r+') as f:
            content = f.read()
            f.write('\nInclude "%s"' % conf_path)
            f.truncate()

    def removeConfiguration(self, domain):
        """Remove Apache configuration files for given domain
        
        Arguments:
            domain {str} -- site domain name
        """
        conf_path = data_path('sites', domain + '.conf')
        if os.path.exists(conf_path):
            os.remove(conf_path)

        with open(self.config.get('apache.conf'), 'r+') as f:
            content = []
            for line in f:
                if (line != 'Include "%s"' % conf_path):
                    content.append(line)
            f.seek(0)
            f.write(''.join(content).strip())
            f.truncate()

    def writeDnsEntry(self, domain):
        """Write DNS entry for given domain
        
        Arguments:
            domain {str} -- site domain name
        """
        with open(self.config.get('dns.file'), 'r+') as f:
            content = f.read()
            f.write('\n127.0.0.1 %s #VirtualHost' % self.getHostName(domain))
            f.write('\n127.0.0.1 www.%s #VirtualHost' % self.getHostName(domain))
            f.truncate()
    
    def removeDnsEntry(self, domain):
        """Remove DNS entry for given domain
        
        Arguments:
            domain {str} -- site domain name
        """
        with open(self.config.get('dns.file'), 'r+') as f:
            content = []
            for line in f:
                line = line.strip()
                if (line != '') and (not line in content) :
                    if line not in ['127.0.0.1 %s #VirtualHost' % self.getHostName(domain), '127.0.0.1 www.%s #VirtualHost' % self.getHostName(domain)]:
                        content.append(line)
            f.seek(0)
            f.write('\n'.join(content))
            f.truncate()

    def refresh(self, domain):
        """Refresh site configuration files
        
        Arguments:
            domain {str} -- site domain name
        
        Raises:
            SiteNotFoundError: site not found
        """
        site = self.find(domain)
        if site == None:
            raise SiteNotFoundError(domain)
            return False

        self.removeConfiguration(site['domain'])
        self.removeDnsEntry(site['domain'])
        self.writeConfiguration(**site)
        self.writeDnsEntry(site['domain'])
        self.restartServices()


    def refreshAll(self):
        """Refresh all site configuration files
        """
        for site in self.list():
            self.removeConfiguration(site['domain'])
            self.removeDnsEntry(site['domain'])
            self.writeConfiguration(**site)
            self.writeDnsEntry(site['domain'])

        self.restartServices()

    def getHostName(self, domain):
        """Get full domain name with TLD
        
        Arguments:
            domain {str} -- site domain name
        
        Returns:
            str -- domain name with TLD
        """
        return domain + '.' + self.config.get('tld', 'test')

    def createSslCertificate(self, domain):
        """Create SSL certificates for given domain
        
        Arguments:
            domain {str} -- site domain name
        """
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa

        os.makedirs(data_path('certs'), exist_ok=True)
        hostname = self.getHostName(domain)
        
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1024,
            backend=default_backend()
        )
        
        name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, hostname)
        ])

        alt_names = x509.SubjectAlternativeName([
            x509.DNSName(hostname),
            x509.DNSName('www.%s' % hostname)
        ])        
        
        cert = (
            x509.CertificateBuilder()
                .subject_name(name)
                .issuer_name(name)
                .public_key(key.public_key())
                .serial_number(1000)
                .not_valid_before(datetime.utcnow())
                .not_valid_after(datetime.utcnow() + timedelta(days=10*365))
                .add_extension(x509.BasicConstraints(ca=True, path_length=0), False)
                .add_extension(alt_names, False)
                .sign(key, hashes.SHA256(), default_backend())
        )

        with open(data_path('certs', '%s.crt' % hostname), 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        with open(data_path('certs', '%s.key' % hostname), 'wb') as f:
            f.write(key.private_bytes(
                serialization.Encoding.PEM, 
                serialization.PrivateFormat.TraditionalOpenSSL, 
                serialization.NoEncryption()
            ))

    def restartServices(self):
        """Restart essential services
        """
        self.server.restart()

        