
<html>
<head>
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='pretty.css')}}">
    <title>Dodaj Authora</title>
</head>
<body>

    {% if exists %}
        <div class="error">
            Taki autor już istnieje
        </div>
    {% endif %}
<form method="POST">
    <div class="container">
    <label for="firstName"> Imię
    <input type="text" placeholder="Enter Author's first Name " name="firstName" id="firstName">
    </label>
    <label for="lastName"> Nazwisko
    <input type="text" placeholder="Enter Author's Surname " name="lastName" id="lastName">
    </label>
    <input type="submit" value="dodaj">
    </div>
</form>

</body>
</html>
