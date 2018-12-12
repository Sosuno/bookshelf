<html>
<head>
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='pretty.css')}}">
    <title>{{book.title}}</title>
</head>
<body>
<div>
<img src="{{book.imageUrl}}" width="120" height="220">
Tytuł: {{ book.title }}
Autor: {{ book.author }}

{% if %}


{% else %}


{% endif %}
</div>

</body>
</html>