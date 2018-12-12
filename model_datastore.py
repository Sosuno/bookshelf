from st import storage
import uuid 
from flask import current_app
from google.cloud import datastore


builtin_list = list


def init_app(app):
    pass


def get_client():
    return datastore.Client('solwit-pjatk-arc-2018-gr4')


def from_datastore(entity):
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity

#---------------------------------> BOOKS

def BookList(limit=10, cursor=None):
    ds = get_client()

    query = ds.query(kind='Book', order=['title'])

    query_iter = query.fetch(start_cursor=cursor, limit=5)
    page = next(query_iter.pages)

    entities = list(page)
    next_cursor = query_iter.next_page_token
    
    return entities, next_cursor

def BookRead(id):
    ds = get_client()
    key = ds.key('Book', int(id))
    results = ds.get(key)
    return from_datastore(results)

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

def BookDelete(id):
    ds = get_client()
    key = ds.key('Book', int(id))
    ds.delete(key)

def upload_image_file(file):
    if not file:
       return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url

def getBookByTitle(title):
    ds = get_client()
    query = ds.query(kind = 'Book')
    books = query.fetch()
    results = []
    for book in books:
        if title.lower() in book['title'].lower():
            results.append(book)
    
    return results


def getBookByAuthor(author):
    ds = get_client()
    query = ds.query(kind = 'Book')
    books = query.fetch()
    results = []
    for book in books:
        if author.lower() in book['author'].lower():
            results.append(book)
    
    return results


#---------------------------------> AUTHORS

def AuthorRead(id):
    ds = get_client()
    key = ds.key('Author', int(id))
    results = ds.get(key)
    return from_datastore(results)


def AuthorUpdate(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('Author', int(id))
    else:
        key = ds.key('Author')

    entity = datastore.Entity(
        key=key)

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)

createAuthor = AuthorUpdate



def AuthorList():
    ds = get_client()

    query = ds.query(kind='Author', order=['lastName'])
    results = query.fetch()
    return results

def AuthorDelete(id):
    ds = get_client()
    key = ds.key('Author', int(id))
    ds.delete(key)


def isAuthorInDB(name, surname):
    ds = get_client()
    query = ds.query(kind='Author')
    query.add_filter('firstName', '=', name)
    query.add_filter('lastName', '=', surname)
    result = list(query.fetch())
    if result:
        return True
    else:
        return False

def getAuthor(name, surname):
    ds = get_client()
    query = ds.query(kind = 'Author')
    query.add_filter('username', '=', name)
    query.add_filter('surname', '=', surname)
    result = list(query.fetch())
    return result


#---------------------------------> USERS
    
def getUser(username):
    ds = get_client()
    query = ds.query(kind = 'User')
    query.add_filter('username', '=', username)
    result = list(query.fetch())

    return result
def UserRead(id):
    ds = get_client()
    key = ds.key('User', int(id))
    results = ds.get(key)
    return from_datastore(results)


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


#---------------------------------> SESSION

def createSession(username):
    ds = get_client()

    key = ds.key('Session')
    entity = datastore.Entity(key=key)
    entity.update({
        'sessionID': uuid.UUID(),
        'user': username,
        'status': 'active'
    })
    ds.put(entity)
    return from_datastore(entity)

def destroySession(sessionID):
    ds = get_client()
    key = ds.key('Session', int(sessionID))
    ds.delete(key)