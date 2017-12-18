from django import forms
from django.contrib.auth.models import User

from .models import Album, Song
from .models import RFId, RFIdDet, ItemIn, ItemOut


class RFIdForm(forms.ModelForm):

    class Meta:
        model = RFId
        fields = ['rf_id', 'mfr_date', 'mfr_firm']


class RFIdDetForm(forms.ModelForm):

    class Meta:
        model = RFIdDet
        fields = ['RFId', 'out_date', 'in_date']


class ItemOutForm(forms.ModelForm):
    class Meta:
        model = ItemOut
        fields = ['Item', 'out_date', 'out_firm', 'out_qty', 'message']


class ItemInForm(forms.ModelForm):
    class Meta:
        model = ItemIn
        fields = ['Item', 'in_date', 'in_firm', 'in_qty', 'message']


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
