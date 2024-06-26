import pytest
from django.test import Client
from django.urls import reverse
from librarian_app.models import Emprunteur


# Même méthode que pour le test de l'ajout des medias (test_media_add).
@pytest.fixture
def client():
    return Client()


@pytest.fixture
def create_emprunteur_form_data():
    return {
        'nom': 'Nom de l\'Emprunteur',
        'bloquer': False,
    }


@pytest.mark.django_db
def test_add_emprunteur_view(client, create_emprunteur_form_data):
    url = reverse('add_emprunteur')

    response = client.post(url, create_emprunteur_form_data)

    assert response.status_code == 302
    assert response.url == reverse('list_emprunteurs')

    assert Emprunteur.objects.filter(nom='Nom de l\'Emprunteur', bloquer=False).exists()


@pytest.mark.django_db
def test_add_emprunteur_view_invalid_data(client):
    url = reverse('add_emprunteur')

    response = client.post(url, {})

    assert response.status_code == 200
    form = response.context['form']
    assert form.errors
