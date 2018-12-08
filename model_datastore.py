from flask import current_app
from google.cloud import datastore


builtin_list = list


def init_app(app):
    pass


def get_client():
    return datastore.Client('solwit-pjatk-arc-2018-gr4')


# [START from_datastore]a
def from_datastore(entity):
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity
# [END from_datastore]


# [START list]
def BookList(limit=10, cursor=None):
    ds = get_client()

    query = ds.query(kind='Book', order=['title'])
    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_iterator.pages)

    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor
# [END list]


def BookRead(id):
    ds = get_client()
    key = ds.key('Book', int(id))
    results = ds.get(key)
    return from_datastore(results)


# [START update]
def BookUpdate(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('Book', int(id))
    else:
        key = ds.key('Book')

    entity = datastore.Entity(
        key=key,
        exclude_from_indexes=['description'])

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)

createBook = BookUpdate

# [END update]


def BookDelete(id):
    ds = get_client()
    key = ds.key('Book', int(id))
    ds.delete(key)



def AuthorRead(id):
    ds = get_client()
    key = ds.key('Author', int(id))
    results = ds.get(key)
    return from_datastore(results)


# [START update]
def AuthorUpdate(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('Author', int(id))
    else:
        key = ds.key('Author')

    entity = datastore.Entity(
        key=key,
        exclude_from_indexes=['birthYear'])

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)

createAuthor = AuthorUpdate

# [END update]


def AuthorList():
    ds = get_client()

    query = ds.query(kind='Author', order=['lastName'])
    results = query.fetch()
    return results

def AuthorDelete(id):
    ds = get_client()
    key = ds.key('Author', int(id))
    ds.delete(key)


def isAuthorInDB(name, surname, birthYear):
    ds = get_client()
    query = ds.query(kind='Author')
    query.add_filter('firstName', '=', name)
    query.add_filter('lastName', '=', surname)
    query.add_filter('birthYear', '=', birthYear)
    result = list(query.fetch())
    if result:
        return True
    else:
        return False



    
def getUser(limit=10, cursor=None):
    ds = get_client()

    query = ds.query(kind='User', )
    
    

    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor

def UserRead(id):
    ds = get_client()
    key = ds.key('User', int(id))
    results = ds.get(key)
    return from_datastore(results)


# [START update]
def UserUpdate(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('User', int(id))
    else:
        key = ds.key('User')

    entity = datastore.Entity(
        key=key,
        )

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)


create = UserUpdate
# [END update]


def UserDelete(id):
    ds = get_client()
    key = ds.key('User', int(id))
    ds.delete(key)


def isUserInDB(username):
    ds = get_client()
    query = ds.query(kind='User')
    query.add_filter('username', '=', username)
    result = list(query.fetch())
    if result:
        return True
    else:
        return False

def isCorrectUser(username, password):
    ds = get_client()
    query = ds.query(kind = 'User')
    query.add_filter('username', '=', username)
    query.add_filter('password', '=', password)
    result = list(query.fetch())
    if result:
        return True
    else:
        return False