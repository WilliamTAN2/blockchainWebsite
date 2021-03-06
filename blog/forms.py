from django import forms
from .models import Article

class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse e-mail")
    renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class ScriptInputsOutputsForm(forms.Form):
    height = forms.DecimalField(max_digits=7, decimal_places=0)

class ScriptRecentTransactionForm(forms.Form):
    txid = forms.CharField(max_length=64)

class TestUrlForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    verbe = forms.CharField(max_length=100)
