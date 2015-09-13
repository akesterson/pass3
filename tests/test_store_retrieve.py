import nose
import pass3

def test_store_retrieve():
    engine = pass3.Engine(
        password='testing')
    entry = pass3.Record(
        scheme='http',
        host='localhost.localdomain',
        path='/somesite',
        user='test',
        password='test',
        title='Some Web Page : Welcome'
        )
    engine.store(entry)
    records = [x for x in engine.search(scheme='http', host='localhost.localdomain', path='/somesite')]
    assert( len(records) == 1 )
    assert( records[0].scheme == 'http' )
    assert( records[0].host == 'localhost.localdomain' )
    assert( records[0].path == '/somesite' )
    assert( records[0].user == 'test' )
    assert( records[0].password == 'test' )
    assert( records[0].title == 'Some Web Page : Welcome' )

def test_store_retrieve_multiple():
    engine = pass3.Engine(
        password='testing'
        )
    engine.store(
        pass3.Record(
            scheme='http',
            host='localhost.localdomain',
            path='/somesite',
            user='test',
            password='test',
            title='test'
        )
    )
    engine.store(
        pass3.Record(
            scheme='http',
            host='localhost.localdomain',
            path='/some_other_site',
            user='test',
            password='test',
            title='test 2'
        )
    )
    records = [x for x in engine.search(scheme='http', host='localhost.localdomain')]
    assert( len(records) == 2 )
    assert( records[0].scheme == 'http' )
    assert( records[0].host == 'localhost.localdomain' )
    assert( records[0].path == '/somesite' )
    assert( records[0].user == 'test' )
    assert( records[0].password == 'test' )
    
    assert( records[1].scheme == 'http' )
    assert( records[1].host == 'localhost.localdomain' )
    assert( records[1].path == '/some_other_site' )
    assert( records[1].user == 'test' )
    assert( records[1].password == 'test' )

def test_store_retrieve_alternate():
    engine = pass3.Engine(
        password='testing'
        )
    record = pass3.Record(
        scheme='http',
        host='localhost.localdomain',
        path='/somesite',
        user='test',
        password='test',
        title='test'
        )
    record.add_alternate(
        pass3.Record(
            scheme='http',
            host='localhost.localdomain',
            path='/some_other_site'
        )
    )
    engine.store(record)
    records = [x for x in engine.search(scheme='http', host='localhost.localdomain', path='/somesite')]
    assert( len(records) == 1 )
    assert( records[0].scheme == 'http' )
    assert( records[0].host == 'localhost.localdomain' )
    assert( records[0].path == '/somesite' )
    assert( records[0].user == 'test' )
    assert( records[0].password == 'test' )
    assert( len(records[0].alternates) == 1 )
    assert( records[0].alternates[0].scheme == 'http' )
    assert( records[0].alternates[0].host == 'localhost.localdomain' )
    assert( records[0].alternates[0].path == '/some_other_site' )
    
    records = [x for x in engine.search(scheme='http', host='localhost.localdomain', path='some_other_site')]
    assert( len(records) == 1 )
    assert( records[0].scheme == 'http' )
    assert( records[0].host == 'localhost.localdomain' )
    assert( records[0].path == '/somesite' )
    assert( records[0].user == 'test' )
    assert( records[0].password == 'test' )

    assert( len(records[0].alternates) == 1 )
    assert( records[0].alternates[0].scheme == 'http' )
    assert( records[0].alternates[0].host == 'localhost.localdomain' )
    assert( records[0].alternates[0].path == '/some_other_site' )
