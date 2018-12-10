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
            return render_template("login.html", action="login", failed = True)        

    return render_template("login.html", action="login", failed = False)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        if model.isUserInDB(request.form['username']):
            return render_template("register.html", action="register", exists=True)
        else:
            data = request.form.to_dict(flat=True)
            book = model.create(data)
            return redirect("login")

    return render_template("register.html", action="register", exists=False)



@app.route('/mainPage')
def mainPage():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = model.BookList(cursor=token)

    return render_template(
        "mainPage.html",
        books=books,
        next_page_token=next_page_token,
        createdAuthor=False, 
        createdBook = True, 
        user = loggedUser)

@app.route('/addBook', methods=['GET', 'POST'])
def addBook():
    if request.method == 'POST':

        data = request.form.to_dict(flat=True)
        image_url = model.upload_image_file(request.files.get('imageURL'))
        data['imageURL'] = image_url
        book = model.createBook(data)
        return render_template("mainPage.html", createdAuthor=False, createdBook = True, user = loggedUser)


    return render_template("addBook.html", action="addBook", authors = model.AuthorList())


@app.route('/addAuthor', methods=['GET', 'POST'])
def addAuthor():
    if request.method == 'POST':

            if model.isAuthorInDB(request.form['firstName'],
                                 request.form['lastName'],    
                                 request.form['birthYear']):
                return render_template("addAuthor.html", action="addAuthor", exists=True)
            else:
                data = request.form.to_dict(flat=True)
                book = model.createAuthor(data)
                return render_template("mainPage.html", createdAuthor=True, createdBook=False, user = loggedUser)

    return render_template("addAuthor.html", action="addAuthor", exists=False)
