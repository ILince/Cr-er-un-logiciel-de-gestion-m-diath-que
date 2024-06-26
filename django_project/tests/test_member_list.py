import pytest
from django.test import Client
from django.urls import reverse
from librarian_app.models import Emprunteur


# Même méthode que le test d'affichage de la liste des medias (test_media_list).
@pytest.fixture
def client():
    return Client()


@pytest.fixture
def create_emprunteurs():
    Emprunteur.objects.create(nom='Nom de l\'Emprunteur 1', bloquer=False)
    Emprunteur.objects.create(nom='Nom de l\'Emprunteur 2', bloquer=True)


@pytest.mark.django_db
def test_list_emprunteurs_view(client, create_emprunteurs):
    url = reverse('list_emprunteurs')

    response = client.get(url)

    assert response.status_code == 200

    assert 'librarian_member_list/member_list.html' in (t.name for t in response.templates)

    emprunteurs = response.context['emprunteurs']
    assert len(emprunteurs) == 2
    assert emprunteurs[0].nom == 'Nom de l\'Emprunteur 1'
    assert emprunteurs[1].nom == 'Nom de l\'Emprunteur 2'
