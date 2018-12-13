
<html>
<head>
    <title>Dodaj książke</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='pretty.css')}}">
</head>
<body>
Wprowadź dane książki
<form method="POST" enctype="multipart/form-data">

    <div class="container">
    <label for="title"> Tytuł</label>
    <input type=text placeholder="Wprowadz tytul" name="title" id="title" value="{{book.title}}" required autocomplete="off">

    <label for="authors"> Wybierz autora</label>
    <input placeholder="znajdz autora na liscie" list="authors" name="author" required autocomplete="off">
    <datalist id="authors">
       {% for author in authors %}
        <option value="{{ author.firstName}} {{author.lastName}}">
            {{ author.firstName}} {{author.lastName}}
            </option>
            {% else %}
            <option value="nope">Brak autorów w bazie</option>
        {% endfor %}
    </datalist>
    Jeśli nie znalazłeś autora na liście możesz<a class=link href="addAuthor"> dodać</a>

    <input type="textarea" name="description" placeholder="Opis" size="50">    


        <label for="image">Cover Image</label>
        <input type="file" name="image" id="image" class="form-control"/>

<input type="submit" value="Dodaj">
</div>
</form>
</body>
</html>
