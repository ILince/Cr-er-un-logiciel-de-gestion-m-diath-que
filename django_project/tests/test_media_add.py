import pytest
from django.test import Client
from django.urls import reverse
from librarian_app.models import Livre


@pytest.fixture
# Simulation de requêtes HTTP vers les vues.
def client():
    return Client()


@pytest.fixture
# Création d'un objet "livre" test dans la base de données.
def create_livre_form_data():
    return {
        'name': 'Titre du Livre',
        'auteur': 'Auteur du Livre',
    }


@pytest.mark.django_db
def test_add_livre_view(client, create_livre_form_data):
    url = reverse('add_livre')

    # Effectue une requête POST vers l'URL en soumettant les données valides de create_livre_form_data.
    response = client.post(url, create_livre_form_data)

    assert response.status_code == 302
    assert response.url == reverse('list_media')
    assert Livre.objects.filter(name='Titre du Livre', auteur='Auteur du Livre').exists()


@pytest.mark.django_db
def test_add_livre_view_invalid_data(client):
    url = reverse('add_livre')

    # Effectue une requête POST vers l'URL en soumettant les données invalides.
    response = client.post(url, {})

    assert response.status_code == 200
    #  Récupère le formulaire dans le contexte de la réponse.
    form = response.context['form']
    # Vérifie que des erreurs existent dans le formulaire.
    assert form.errors
