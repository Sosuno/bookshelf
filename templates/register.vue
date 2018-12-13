
<html>
<head>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='pretty.css')}}">
    <title>Register user</title>
</head>
<body>

    {% if exists %}
        <div class="error">
            Taki użytkownik już istnieje
        </div>
    {% endif %}
<form method="POST">
    <div class="container">
    <label for="username"> Wprowadz login</label>
    <input type="text" placeholder="Username" name="username" min="3" max="20" required>

    <label for="password"> Wprowadz haslo</label>
    <input type="password" placeholder="Password" name="password" min="3" required>
    <input type="hidden" name="security_lvl" value="normal">
    <input type="hidden" name="favBooks" value="[]">
    <input type="submit" VALUE="Register">
    </div>
</form>

</body>
</html>
