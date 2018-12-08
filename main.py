import model_datastore
from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)

model = model_datastore
loggedin = False


@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if model.isCorrectUser(request.form['username'], request.form['password']):
            loggedin = True
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
        createdAuthor=False)

@app.route('/addBook')
def addBook():
    if request.method == 'POST':

            if model.isUserInDB(request.form['username']):
                return render_template("register.html", action="register", exists=True)
            else:
                data = request.form.to_dict(flat=True)
                book = model.create(data)
                return redirect("login")


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
                return redirect("mainPage", createdAuthor=True)

    return render_template("addAuthor.html", action="addAuthor", exists=False)
