from django import forms


class JumpForm(forms.Form):
    team = None
    date = forms.DateField()
    pool = None
    url = forms.URLField()
    points = forms.IntegerField()
    busts = forms.IntegerField()
    results = None
