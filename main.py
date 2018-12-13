import model_datastore
from flask import Flask, request, jsonify


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
            out.set_cookie('session', session['sessionID'], max_age=60*60*24)
            return out
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

@app.route('/getBooks', methods=['GET', 'POST'])
def getBooks():
    books = model.BookList()
    if request.method == 'POST':
        if request.form['searchBy'] == 'tytul':
          books = model.getBookByTitle(request.form['search'])
        else:
            books = model.getBookByAuthor(request.form['search'])

    return jsonify(books)

@app.route('/addBook', methods=['GET', 'POST'])
def addBook():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        img = request.files.get('image')
        image_url = model.upload_image_file(img)
        data['imageUrl'] = image_url
        book = model.createBook(data)
        return jsonify(book)

@app.route('/getAuthors',  methods=['GET', 'POST'])
def getAuthors():
    return jsonify(model.AuthorList())

@app.route('/isLogged', methods=['GET', 'POST'] )
def isLogged():
    if request.cookies.get('session') is None:
        return jsonify(False)
    else:
        uuid = request.cookies.get('session')
        if not model.checkIfSessionActive(uuid):
            notLogged = True
            return jsonify(False)
        else:
            return jsonify(True)



@app.route('/addAuthor', methods=['GET', 'POST'])
def addAuthor():
    if request.method == 'POST':
            if model.isAuthorInDB(request.form['firstName'],
                                 request.form['lastName']):
                return jsonify(False)
            else:
                data = request.form.to_dict(flat=True)
                book = model.createAuthor(data)
                return jsonify(True)

@app.route('/logout')
def logout(): 
    uuid = request.cookies.get('session')
    user = model.getUsernameFromSession(uuid)
    model.destroyAllUserSessions(user)
    out = jsonify(msg = 'Logged out')
    out.set_cookie('session', uuid, max_age=0)
    return out

@app.route("/book/<id>")
def book(id):
    book = model.BookRead(id)
    return jsonify(book)

@app.route("/addTofav")
def addTofav():
    book = request.form['bookID']
    uuid = request.cookies.get('session')
    username = model.getUsernameFromSession(uuid)
    user = model.getUser(username)
    fav = list(user['favBooks'])
    fav.append(book)
    user['favBooks'] = fav
    u = model.UserUpdate(user, user[id])
    return jsonify(True)

@app.route("/getFav")
def getFav():
    uuid = request.cookies.get('session')
    username = model.getUsernameFromSession(uuid)
    user = model.getUser(username)
    favBooks = list((user['favBooks']))
    books = []
    for book in favBooks:
        books.append(model.BookRead(book))
    return jsonify(books)
