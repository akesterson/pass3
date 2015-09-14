import nose
import pass3
import pass3.storage
import os
import boto.s3.connection
import boto.s3.key
import json

def test_memory_archive_encrypted():
    storage = pass3.storage.MemoryStorage()
    storage.store(pass3.Record(
        scheme='http',
        host='localhost.localdomain',
        path='/somesite',
        user='test',
        password='test',
        title='Some Web Page : Welcome'
        ),
        passphrase='testing'
    )
    assert('records' not in storage.get_archive().keys())

def test_S3Storage():
    cfg = pass3.config.get_config()
    access_key = cfg['storage']['S3Storage']['access_key']
    secret_access_key = cfg['storage']['S3Storage']['secret_access_key']
    bucket = cfg['storage']['S3Storage']['bucket']
    
    aws = boto.s3.connection.S3Connection(access_key, secret_access_key, calling_format = boto.s3.connection.OrdinaryCallingFormat())
    bucket = aws.get_bucket(bucket)

    storage = pass3.storage.S3Storage(
        access_key=access_key,
        secret_access_key=secret_access_key,
        bucket=bucket,
        passphrase='testing'
        )
    storage.store(pass3.Record(
        scheme='http',
        host='localhost.localdomain',
        path='/somesite',
        user='test',
        password='test',
        title='Some Web Page : Welcome'
        ),
        passphrase='testing'
    )

    key = boto.s3.key.Key(bucket, 'pass3.json')
    doc = storage.get_archive()
    bucket.delete_key('pass3.json')
    assert(key.get_contents_as_string() == json.dumps(doc))
