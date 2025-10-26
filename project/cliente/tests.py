{% extends "core/base.html" %}
{% load static %}

{% block title %}
    TeLaArmo
{% endblock title %}

{% block content %}
<h1 class="text-center mt-3">TeLaArmo</h1>
<p class="text-center">Registrate, crea tu equipo y te armo la alineación. Mejor que GianGPT ⚽</p>

<!-- 🔹 Botones principales -->
<div class="d-flex justify-content-center align-items-center my-3">
    <div class="d-flex justify-content-center gap-3 flex-wrap">
        <a href="{% url 'cliente:crear_equipo' %}" class="btn btn-primary btn-lg rounded-pill shadow-sm">
            Equipos Creados
        </a>

        {% if not user.is_authenticated %}
            <a href="{% url 'core:register' %}" class="btn btn-success btn-lg rounded-pill shadow-sm">
                Registrarse
            </a>
            <a href="{% url 'core:login' %}" class="btn btn-outline-success btn-lg rounded-pill shadow-sm">
                Acceder
            </a>
        {% else %}
            <form action="{% url 'core:logout' %}" method="post" style="display:inline;">
                {% csrf_token %}
                <button type="submit" class="btn btn-danger btn-lg rounded-pill shadow-sm">
                    Cerrar sesión
                </button>
            </form>
        {% endif %}
    </div>
</div>

<!-- 🔹 Sección inferior (imagen + texto + cards) -->
<div class="row gx-4 gx-lg-5 align-items-center mt-4">
    <div class="col-lg-7">
        <img class="img-fluid rounded mb-4 mb-lg-0" src="{% static 'core/img/photo.jpeg' %}" alt="Imagen" />
    </div>
    <div class="col-lg-5">
        <h1 class="font-weight-light">Calcio 2.1</h1>
        <p>Deportivo Ansiedad de la ciudad de Buenos Aires</p>
        <a class="btn btn-success" href="https://wa.me/549112345678" target="_blank">Whatsapp</a>
    </div>
</div>

<!-- 🔹 Card con mensaje -->
<div class="card text-white bg-secondary my-4 py-4 text-center shadow">
    <div class="card-body">
        <p class="text-white m-0">
            Deja de pelear por la alineación: ¡aquí armas tu equipo como un crack!
        </p>
    </div>
</div>

{% endblock content %}

<footer>
    {% include "core/footer.html" %}
</footer>

