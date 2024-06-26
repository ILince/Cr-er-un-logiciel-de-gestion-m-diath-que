from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


# Methode de connexion _________________________________________________________________________________________________

def login_view(request):
    # Si le formulaire de connexion a été soumis.
    if request.method == 'POST':
        # Alors, création d'une instance du formulaire d'authentification.
        form = AuthenticationForm(request,
                                  request.POST)
        # Si les données du formulaire sont valides.
        if form.is_valid():
            # Alors, récupération des données validées,
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Et Comparaissant des données validées avec les informations d'identification.
            user = authenticate(username=username,
                                password=password)
            # Si l'utilisateur a bien été authentifié.
            if user is not None:
                # Alors, création d'une session utilisateur et redirection de l'utilisateur vers la vue librarian_menu.
                login(request, user)
                return redirect('librarian_menu')
            else:
                # Sinon affichage d'un message d'erreur.
                form.add_error(None,
                               "Nom d'utilisateur ou mot de passe incorrect")
    else:
        # Sinon affichage d'un formulaire de connexion vide.
        form = AuthenticationForm()
    return render(request, 'librarian_log/librarian_log.html', {'form': form})


# Affichage du menu du blibliothécaire connecté ________________________________________________________________________

def librarian_menu(request):
    return render(request, 'librarian_menu/librarian_home.html')
