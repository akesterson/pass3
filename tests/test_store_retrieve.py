import nose
import pass3

def test_store_retrieve():
    engine = pass3.Engine(
        password='testing',
        access_key='testing',
        storage_key='testing')
    stored_obj = engine.store(
        scheme='http',
        uri='localhost.localdomain/somesite',
        user='test',
        password='test'
        )
    records = engine.search(
        scheme='http',
        uri='localhost.localdomain/somesite'
        )
    assert( len(records) == 1 )
    assert( records[0].scheme == 'http' )
    assert( records[0].uri == 'localhost.localdomain/somesite' )
    assert( records[0].user == 'test' )
    assert( records[0].password == 'test' )

def test_store_retrieve_multiple():
    engine = pass3.Engine(
        password='testing',
        access_key='testing',
        storage_key='testing')
    stored_obj = engine.store(
        scheme='http',
        uri='localhost.localdomain/somesite',
        user='test',
        password='test'
        )
    stored_obj = engine.store(
        scheme='http',
        uri='localhost.localdomain/some_other_site',
        user='test',
        password='test'
        )
    records = engine.search(
        scheme='http',
        uri='localhost.localdomain'
        )
    assert( len(records) == 2 )
    assert( records[0].scheme == 'http' )
    assert( records[0].uri == 'localhost.localdomain/somesite' )
    assert( records[0].user == 'test' )
    assert( records[0].password == 'test' )
    
    assert( records[1].scheme == 'http' )
    assert( records[1].uri == 'localhost.localdomain/some_other_site' )
    assert( records[1].user == 'test' )
    assert( records[1].password == 'test' )

def test_store_retrieve_alternate():
    engine = pass3.Engine(
        password='testing',
        access_key='testing',
        storage_key='testing')
    stored_obj = engine.store(
        scheme='http',
        uri='localhost.localdomain/somesite',
        user='test',
        password='test'
        )
    alternate_obj = engine.add_alternate(
        target=stored_obj,
        scheme='http',
        uri='localhost.localdomain/some_other_site'
        )
    records = engine.search(
        scheme='http',
        uri='localhost.localdomain/somesite'
        )
    assert( len(records) == 1 )
    assert( records[0].scheme == 'http' )
    assert( records[0].uri == 'localhost.localdomain/somesite' )
    assert( records[0].user == 'test' )
    assert( records[0].password == 'test' )

    records = engine.search(
        scheme='http',
        uri='localhost.localdomain/some_other_site'
        )
    assert( len(records) == 1 )
    assert( records[0].scheme == 'http' )
    assert( records[0].uri == 'localhost.localdomain/somesite' )
    assert( records[0].user == 'test' )
    assert( records[0].password == 'test' )

    assert( len(records[0].alternates) == 1 )
    assert( records[0].alternates[0].scheme == 'http' )
    assert( records[0].alternates[0].uri == 'localhost.localdomain/some_other_site' )
