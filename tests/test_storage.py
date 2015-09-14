import nose
import pass3
import pass3.storage
import os
import boto.s3.connection
import boto.s3.key
import json
import sys
import time

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
    cfg['storage']['S3Storage']['file'] = "pass3-%d_%d_%d.json" % (
        sys.version_info[0],
        sys.version_info[1],
        sys.version_info[2]
        )
    filename = cfg['storage']['S3Storage']['file']
        
    aws = boto.s3.connection.S3Connection(access_key, secret_access_key, calling_format = boto.s3.connection.OrdinaryCallingFormat())
    bucket = aws.get_bucket(bucket)

    storage = pass3.storage.S3Storage(
        access_key=access_key,
        secret_access_key=secret_access_key,
        bucket=bucket,
        passphrase='testing',
        filename = filename
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

    key = boto.s3.key.Key(bucket, filename)
    doc = storage.get_archive()
    try:
        assert(key.get_contents_as_string() == json.dumps(doc))
    finally:
        bucket.delete_key(filename)
