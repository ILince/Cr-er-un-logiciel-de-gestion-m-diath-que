from django.shortcuts import render
from librarian_app.models import Livre, DVD, CD, BoardGame


# AFFICHER la liste des médias et des jeux de plateau __________________________________________________________________

def list_all_media(request):
    livres = Livre.objects.all()
    dvds = DVD.objects.all()
    cds = CD.objects.all()
    boardgames = BoardGame.objects.all()
    return render(request, 'member_media/media_list.html', {
        'livres': livres,
        'dvds': dvds,
        'cds': cds,
        'boardgames': boardgames,
    })
