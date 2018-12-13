import model_datastore
from flask import Flask, request, jsonify, after_this_request, make_response


app = Flask(__name__)

model = model_datastore

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if model.isCorrectUser(username, request.form['password']):
            model.destroyAllUserSessions(username)
            session = model.createSession(username)
            out = jsonify(True)
            return out
            @after_this_request
            def setCookie(reponse):
                reponse.setset_cookie('session', session['sessionID'], max_age=60*60*24)
        else:
            return jsonify(False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if model.isUserInDB(request.form['username']):
            return jsonify(False)
        else:
            data = request.form.to_dict(flat=True)
            data['favBooks'] = []
            user = model.create(data)
            return jsonify(True)


@app.route('/Book', methods=['GET', 'POST', 'DELETE'])
@app.route('/Book/<id>', methods=['GET', 'POST', 'DELETE'])
def addBook(id = None):
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        if not model.checkIfBookExists(data['author'], data['title']):
            img = request.files.get('image')
            image_url = model.upload_image_file(img)
            data['imageUrl'] = image_url
            book = model.createBook(data)
            return jsonify(book)
        else:
            return jsonify(False)
    elif request.method == 'GET':
        book = model.BookRead(id)
        return jsonify(book)
    else:
        model.BookDelete(id)

@app.route('/isLogged', methods=['GET', 'POST'] )
def isLogged():
    if request.cookies.get('session') is None:
        return jsonify(False)
    else:
        uuid = request.cookies.get('session')
        if not model.checkIfSessionActive(uuid):
            return jsonify(False)
        else:
            return jsonify(True)

@app.route('/Author', methods=['GET', 'POST'])
def addAuthor():
    if request.method == 'POST':
            if model.isAuthorInDB(request.form['firstName'],
                                 request.form['lastName']):
                return jsonify(False)
            else:
                data = request.form.to_dict(flat=True)
                book = model.createAuthor(data)
                return jsonify(True)
    elif request.method == 'GET':
        return jsonify(model.AuthorList())
        

@app.route('/logout', method= ['POST', 'GET'])
def logout(): 
    uuid = request.cookies.get('session')
    user = model.getUsernameFromSession(uuid)
    model.destroyAllUserSessions(user)
    out = jsonify(msg = 'Logged out')
    return out
    @after_this_request
    def resetCookie(reponse):
        reponse.setset_cookie('session', uuid, max_age=0)

@app.route("/favBooks/<bookId>", method= ['POST', 'GET', 'DELETE'])    
@app.route("/favBooks", method= ['POST', 'GET', 'DELETE'])
def favBooks(bookID = None):

    uuid = request.cookies.get('session')
    username = model.getUsernameFromSession(uuid)
    user = model.getUser(username)
    if request.method == 'POST':
        book = bookID
        fav = list(user['favBooks'])
        fav.append(book)
        user['favBooks'] = fav
        u = model.UserUpdate(user, user[id])
        return jsonify(True)
    elif request.method == 'GET':
        favBooks = list((user['favBooks']))
        books = []
        for book in favBooks:
            books.append(model.BookRead(book))
        return jsonify(books)
    else:
        favBooks = list((user['favBooks']))
        for book in favBooks:
            if book == bookID:
                favBooks.remove(book)
        user['favBooks'] = fav
        u = model.UserUpdate(user, user[id])
        return jsonify(True)


