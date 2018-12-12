<html>
  <head>
      <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='pretty.css')}}">
    <title>Main</title>
  </head>
  <body>
    Witaj {{ user.username }} ! ||
  <a class=goto href="{{url_for('addBook') }}" >Dodaj Książke</a> ||
  <a class=goto href="{{url_for('addAuthor') }}" >Dodaj Autora</a> ||
  <a class=goto href="logout.html">Wyloguj</a>


  {% if createdAuthor %}
    <div class = "success">
      Pomyślnie utworzono autora
   </div>
  {% endif %}
  {% if createdBook %}
    <div class = "success">
      Pomyślnie utworzono książkę
    </div>
  {% endif %}

  Szukaj książki
  <form method="POST">
    <input name="search">
    Szukaj po:
    Tytule: <input type="radio" value="tytul" name="searchBy" checked>
    Autorze: <input type="radio" value="autor" name="searchBy">
    <input type="submit" value="Szukaj">
  </form>

  <div class="bookList">
    <table>
      <tr>
        <th>
          Okładka
        </th>
        <th>
          Tytuł
        </th>
        <th>
          Autor
        </th>
        <th>
          Dodaj do ulubionych
        </th>
      </tr>
        {% for book in books %}
        <tr>
        <td><div class="media-left">
          {% if book.imageUrl %}
            <img class="book-image" src="{{book.imageUrl}}" width="100px" height="200px">
          {% else %}
            <img class="book-image" src="https://storage.googleapis.com/solwit-pjatk-bookshelf/Cover-placeholder.gif" width="100px" height="200px">
          {% endif %}
        </div></td>
        <td> {{book.title}} </td>
        <td>{{book.author}} </td>
        <td> <input type="checkbox" name="{{book.id}}" > </td>
        </tr>
          {% else %}
          </table>
          Brak książek w bazie.
          <a class=goto href="{{url_for('addBook') }}">Dodaj</a>     
        {% endfor %}
    </table>
    {% if next_page_token %}
    <nav>
      <ul class="pager">
        <li><a href="?page_token={{next_page_token}}">More</a></li>
      </ul>
    </nav>
    {% endif %}

  </div>
  </body>
</html>
