import pytest
from django.test import Client
from django.urls import reverse
from librarian_app.models import Livre


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def livre():
    return Livre.objects.create(name="Titre du Livre", auteur="Auteur du Livre")


@pytest.mark.django_db
# Vérifie que la page de confirmation de suppression s'affiche correctement.
def test_delete_livre_view_get(client, livre):
    url = reverse('delete_media', args=['livre', livre.id])

    response = client.get(url)

    assert response.status_code == 200
    #  Vérifie que le template correct est utilisé pour afficher la page de confirmation.
    assert 'librarian_media_list/media_delete.html' in (t.name for t in response.templates)
    #  Vérifie que le contexte de la réponse contient bien l'objet Livre à supprimer.
    assert response.context['media_item'] == livre


@pytest.mark.django_db
# Vérifie que la suppression de l'élément se fait correctement.
def test_delete_livre_view_post(client, livre):
    url = reverse('delete_media', args=['livre', livre.id])

    response = client.post(url)

    assert response.status_code == 302
    # Vérifie que l'objet livre avec l'ID spécifié a bien été supprimé de la base de données.
    assert not Livre.objects.filter(id=livre.id).exists()
