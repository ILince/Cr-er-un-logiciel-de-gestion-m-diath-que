import pytest
from django.test import Client
from django.urls import reverse
from librarian_app.models import Livre, DVD, CD, BoardGame

@pytest.mark.django_db
def test_list_media_view():
    # Création des modèles avec des données de test.
    Livre.objects.create(name='Livre 1', auteur='Auteur 1')
    DVD.objects.create(name='DVD 1', realisateur='Réalisateur 1')
    CD.objects.create(name='CD 1', artiste='Artiste 1')
    BoardGame.objects.create(name='Jeu de plateau 1', createur='Créateur 1')

    client = Client()
    url = reverse('list_media')

    response = client.get(url)

    # Vérifications
    assert response.status_code == 200
    # Vérifie que les clés sont présentes dans le contexte de la réponse et que donc les objets correspondants ont été passés au template.
    assert 'livres' in response.context
    assert 'dvds' in response.context
    assert 'cds' in response.context
    assert 'boardgames' in response.context

    # Vérifie que le bon template est utilisé.
    assert 'librarian_media_list/media_list.html' in [template.name for template in response.templates]
