
<html>
<head>
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='pretty.css')}}">
    <title>Login</title>
</head>
<body>
        {% if failed %}
        <div class="error">
           Błędny login lub hasło
        </div>
    {% endif %}
<div>
    <form method="POST" >
            <div class="container">
            <label for="title"> Wprowadz login</label>
        <input type="text" placeholder="username" name="username"/>
        <label for="title"> Wprowadz haslo</label>
        <input type="password" placeholder="password" name="password"/>
        <input type="submit" value="Login">
            </div>
    </form>
    <a href="register"><button value="register">Register</button> </a>
</div>
</body>
</html>
