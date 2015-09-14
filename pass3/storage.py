import boto.s3.connection
import boto.s3.key
import boto.exception
import sys
import pass3.encryption
import pass3.record
import json
import time
import logging

class MemoryStorage(object):
    """
    Stores passwords in memory in their encrypted form
    """
    def __init__(self):
        super(MemoryStorage, self).__init__()
        self.__archive__ = {'records': []}
        
    def store(self, record, passphrase):
        archive = self.decrypt_archive(passphrase)
        archive['records'].append(record)
        self.encrypt_archive(archive, passphrase)

    def delete(self, record, passphrase):
        archive = self.decrypt_archive(passphrase)
        for r in archive['records']:
            if r.title == record.title:
                archive['records'].remove(r)
                return
            
    def iteritems(self, passphrase):
        for record in self.decrypt_archive(passphrase)['records']:
            yield record

    def size(self, passphrase):
        return len(self.decrypt_archive(passphrase)['records'])

    def get_archive(self):
        return self.__archive__
    
    def decrypt_archive(self, passphrase):
        archive = self.get_archive()
        if not ('message' in archive and 'cipher' in archive):
            return archive
        try:
            decrypted = pass3.encryption.decrypt_message(archive['message'], archive['cipher'], passphrase)
        except ValueError, e:
            raise pass3.exceptions.PasswordException(str(e))
        doc = json.loads(decrypted)
        doc['records'] = [pass3.record.Record.from_dict(x) for x in doc['records']]
        return doc
    
    def encrypt_archive(self, decrypted, passphrase):
        doc = {}
        doc['records'] = [x.to_dict() for x in decrypted['records']]
        (cipher, message) = pass3.encryption.encrypt_message(json.dumps(doc), passphrase)
        self.__archive__ = {'cipher': cipher, 'message': message}

        
class S3Storage(MemoryStorage):
    """
    A storage backend which fetches and decrypts records from Amazon S3,
    and does not retain them decrypted in memory, or in unencrypted form on disk.
    Keeps an encrypted copy in memory and only reads/writes to S3 when necessary,
    all queries are performed against the in-memory copy (but the directory is
    decrypted on each query).
    """
    def __init__(self, access_key, secret_access_key, bucket, filename, passphrase):
        super(S3Storage, self).__init__()
        self.__aws__ = boto.s3.connection.S3Connection(
            access_key,
            secret_access_key,
            calling_format = boto.s3.connection.OrdinaryCallingFormat()
            )
        self.__bucket__ = self.__aws__.get_bucket(bucket)
        self.__filename__ = filename
        
    def store(self, record, passphrase):
        archive = self.decrypt_archive(passphrase)
        archive['records'].append(record)
        super(S3Storage, self).store(record, passphrase)
        self.store_archive()

    def delete(self, record, passphrase):
        super(S3Storage, self).delete(record, passphrase)
        self.store_archive()

    def iteritems(self, passphrase):
        for record in self.decrypt_archive(passphrase)['records']:
            yield pass3.record.Record.from_dict(record)

    def get_archive(self):
        if (not 'cipher' in self.__archive__.keys()) and (len(self.__archive__.get('records', 0)) == 0):
            try:
                key = boto.s3.key.Key(self.__bucket__, self.__filename__)
                self.__archive__ = json.loads(key.get_contents_as_string())
            except boto.exception.S3ResponseError, e:
                if ('404' in [str(e.status), str(e.error_code)]):
                    logging.warning("%s not found in S3; creating a new archive..." % self.__filename__)
        return self.__archive__

    def store_archive(self):
        key = boto.s3.key.Key(self.__bucket__, self.__filename__)
        key.set_contents_from_string(json.dumps(self.__archive__))
