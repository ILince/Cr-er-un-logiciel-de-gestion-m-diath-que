import pytest
from django.test import Client
from django.urls import reverse
from librarian_app.models import Emprunteur


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def emprunteur():
    return Emprunteur.objects.create(nom="Nom de l'Emprunteur", bloquer=False)


@pytest.mark.django_db
def test_update_emprunteur_view(client, emprunteur):
    url = reverse('update_emprunteur', kwargs={'pk': emprunteur.pk})

    response = client.get(url)

    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].instance == emprunteur

    updated_nom = "Nouveau Nom de l'Emprunteur"
    post_data = {
        'nom': updated_nom,
        'bloquer': False,
    }
    response = client.post(url, post_data)

    assert response.status_code == 302
    assert response.url == reverse('list_emprunteurs')

    # Vérifie que l'objet Emprunteur a été mis à jour dans la base de données.
    emprunteur.refresh_from_db()
    assert emprunteur.nom == updated_nom
