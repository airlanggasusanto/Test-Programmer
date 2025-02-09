from django import forms
from core.models import Produk

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama_produk', 'kategori', 'harga', 'status']
