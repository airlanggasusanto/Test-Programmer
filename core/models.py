from django.db import models

class Kategori(models.Model):
    nama_kategori = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_kategori

class Status(models.Model):
    nama_status = models.CharField(max_length=50)

    def __str__(self):
        return self.nama_kategori

class Produk(models.Model):
    nama_produk = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.nama_produk

class FetchApi(models.Model):
    name = models.CharField(max_length=255, unique=True)
    executed = models.BooleanField(default=False)
