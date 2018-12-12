import model_datastore
from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)

model = model_datastore
loggedUser = None


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if model.isCorrectUser(request.form['username'], request.form['password']):
            loggedUser = model.getUser(request.form['username'])
            return redirect("mainPage")
        else:
            return render_template("login.vue", action="login", failed = True)        

    return render_template("login.vue", action="login", failed = False)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        if model.isUserInDB(request.form['username']):
            return render_template("register.vue", action="register", exists=True)
        else:
            data = request.form.to_dict(flat=True)
            book = model.create(data)
            return redirect("login")

    return render_template("register.vue", action="register", exists=False)



@app.route('/mainPage', methods=['GET', 'POST'])
def mainPage():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = model.BookList(cursor=token)
    if request.method == 'POST':
        if request.form['searchBy'] == 'tytul':
          books = model.getBookByTitle(request.form['search'])
        else:
            books = model.getBookByAuthor(request.form['search'])

    return render_template(
        "mainPage.vue",
        books=books,
        next_page_token=next_page_token,
        createdAuthor=False, 
        createdBook = False, 
        user = loggedUser,
        action = "mainPage")

@app.route('/addBook', methods=['GET', 'POST'])
def addBook():
    if request.method == 'POST':

        data = request.form.to_dict(flat=True)
        img = request.files.get('image')
        image_url = model.upload_image_file(img)
        data['imageUrl'] = image_url
        book = model.createBook(data)
        return redirect(url_for('mainPage', createdAuthor=False, createdBook = True, user = loggedUser))


    return render_template("addBook.vue", action="addBook", authors = model.AuthorList(), book={})


@app.route('/addAuthor', methods=['GET', 'POST'])
def addAuthor():
    if request.method == 'POST':

            if model.isAuthorInDB(request.form['firstName'],
                                 request.form['lastName']):
                return redirect("addAuthor.vue", action="addAuthor", exists=True)
            else:
                data = request.form.to_dict(flat=True)
                book = model.createAuthor(data)
                return redirect("mainPage.vue", createdAuthor=True, createdBook=False, user = loggedUser)

    return render_template("addAuthor.vue", action="addAuthor", exists=False)
