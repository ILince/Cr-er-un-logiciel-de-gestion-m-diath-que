from django import forms

from librarian_app.models import Emprunteur, Livre, DVD, CD, BoardGame, Emprunt


# Formulaire de connexion des bibliothécaires __________________________________________________________________________

class LibrarianLoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


# Formulaires d'ajouts ou de modifications des Médias/Jeux de Plateau __________________________________________________

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['name', 'auteur', 'disponible']


class DVDForm(forms.ModelForm):
    class Meta:
        model = DVD
        fields = ['name', 'realisateur', 'disponible']


class CDForm(forms.ModelForm):
    class Meta:
        model = CD
        fields = ['name', 'artiste', 'disponible']


class BoardGameForm(forms.ModelForm):
    class Meta:
        model = BoardGame
        fields = ['name', 'createur']


# Formulaire d'ajouts ou de modifications de membre ____________________________________________________________________

class EmprunteurForm(forms.ModelForm):
    class Meta:
        model = Emprunteur
        fields = ['nom', 'bloquer']


# Formulaire d'ajouts des Emprunts _____________________________________________________________________________________

class EmpruntForm(forms.ModelForm):
    # Champ avec tous les emprunteurs/membres disponibles.
    emprunteur = forms.ModelChoiceField(queryset=Emprunteur.objects.all(),
                                        label="Sélectionnez l'emprunteur")
    # Champ avec uniquement les objets disponibles de chaque type de média.
    livre = forms.ModelChoiceField(queryset=Livre.objects.filter(disponible=True), required=False,

                                   label="Sélectionnez le livre")
    dvd = forms.ModelChoiceField(queryset=DVD.objects.filter(disponible=True), required=False,
                                 label="Sélectionnez le DVD")
    cd = forms.ModelChoiceField(queryset=CD.objects.filter(disponible=True), required=False, label="Sélectionnez le CD")

    # Définition des métadonnées du formulaire.
    class Meta:
        model = Emprunt
        fields = ['emprunteur', 'livre', 'dvd', 'cd']

    # Initialisation du formulaire.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des champs du formulaire.
        self.fields['livre'].empty_label = "Choisir un livre"
        self.fields['dvd'].empty_label = "Choisir un DVD"
        self.fields['cd'].empty_label = "Choisir un CD"

        # Personnalisation de l'affichage des options des champs de sélection.
        self.fields['livre'].label_from_instance = lambda \
                obj: obj.name
        self.fields['dvd'].label_from_instance = lambda obj: obj.name
        self.fields['cd'].label_from_instance = lambda obj: obj.name
