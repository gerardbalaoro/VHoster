from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
from vhoster.helpers import *
import os


class Certificate:
    """SSL/TLS Certificate Toolkit

    Arguments:
        domain {str} -- domain name
    """

    def __init__(self, domain):
        self.domain = domain

    def create(self, certPath, keyPath):
        """Create SSL/TLS certificate

        Arguments:
            certPath {str} -- path to store certificate file (.crt)
            keyPath {str} -- path to store certificate key (.key)
        """
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1024,
            backend=default_backend()
        )

        name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, self.domain)
        ])

        alt_names = x509.SubjectAlternativeName([
            x509.DNSName(self.domain),
            x509.DNSName('www.%s' % self.domain)
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

        with open(certPath, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
            info(os.path.basename(certPath), title='Certificate Created')

        with open(keyPath, 'wb') as f:
            f.write(key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption()
            ))

    def delete(self, certPath, keyPath):
        """Delete SSL/TLS certificate

        Arguments:
            certPath {str} -- path to certificate file (.crt)
            keyPath {str} -- path to certificate key (.key)
        """
        for path in [certPath, keyPath]:
            if os.path.exists(path) and os.path.isfile(path):
                os.unlink(path)
                info(os.path.basename(path), title='Deleted')

    def trust(self, certPath):
        """Add to trusted root certificates

        Arguments:
            certPath {str} -- path to certificate file (.crt)
        """
        if not os.path.exists(certPath) and os.path.isfile(certPath):
            error(certPath, 'File not found')
            return None

        fileName = os.path.basename(certPath)
        command = run_command(
            'certutil -addstore -f "ROOT" ' + repr(certPath), True)

        if command['returncode'] == 0:
            info(fileName, title='Added to trusted certificates')
        else:
            error(fileName, title='Failed to add to trusted certificates')
            warn('\n' + template('cmd.txt', **command))

    def untrust(self, certPath):
        """Remove from trusted root certificates

        Arguments:
            certPath {str} -- path to certificate file (.crt)
        """
        fingerprint = self.getFingerprint(certPath)

        if fingerprint:
            fileName = os.path.basename(certPath)
            command = run_command(
                'certutil -delstore "ROOT" %s' % repr(fingerprint), True)

            if command['returncode'] == 0:
                success(fileName, title='Added to trusted certificates')
            else:
                error(fileName, title='Failed to add to trusted certificates')
                warn('\n' + template('cmd.txt', **command))

    def getFingerprint(self, certPath):
        """Get certificate fingerprint

        Arguments:
            certPath {str} -- path to certificate file (.crt)

        Return:
            str -- certificate fingerprint encoded using SHA1
        """
        if not os.path.exists(certPath):
            return None

        with open(certPath, 'rb') as certFile:
            cert = x509.load_pem_x509_certificate(
                certFile.read(), default_backend())
            fingerprint = cert.fingerprint(hashes.SHA1())
            return ":".join("{:02x}".format(c) for c in fingerprint).upper()
