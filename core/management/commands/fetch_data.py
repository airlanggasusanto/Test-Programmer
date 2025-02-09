import os
import hashlib
import requests
from datetime import datetime, timedelta, timezone
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Kategori, Status, Produk, FetchApi

class Command(BaseCommand):
    help = "3. Simpan produk yang sudah anda dapatkan dari url produk"

    def handle(self, *args, **kwargs):
        self.stdout.write("Fetching data...")

        tz = datetime.now(timezone.utc) + timedelta(hours=9)
        day, month, year = tz.day, tz.month, str(tz.year)[-2:]

        api_url = os.getenv("API_BASE_URL")
        username = self.get_username(api_url)
        password = f"bisacoding-{day:02}-{month:02}-{year}"
        password_md5 = hashlib.md5(password.encode()).hexdigest()

        data = self.fetch_data(username, password_md5, api_url)
        if not data:
            self.stderr.write("No data fetched.")
            return

        try:
            with transaction.atomic():
                for item in data:
                    kategori_obj, _ = Kategori.objects.get_or_create(nama_kategori=item["kategori"])
                    status_obj, _ = Status.objects.get_or_create(nama_status=item["status"])

                    Produk.objects.update_or_create(
                        nama_produk=item["nama_produk"],
                        defaults={"harga": item["harga"], "kategori": kategori_obj, "status": status_obj}
                    )

                FetchApi.objects.create(name="fetch_products", executed=True)
                self.stdout.write(self.style.SUCCESS("Data successfully saved to the database."))

        except Exception as e:
            self.stderr.write(f"Error saving data: {e}")

    def get_username(self, url):
        try:
            response = requests.post(url)
            header_value = response.headers.get("x-credentials-username")
            return header_value.split(" (")[0] if header_value else None
        except requests.exceptions.RequestException as error:
            self.stderr.write(f"Error: {error}")
            return None

    def fetch_data(self, username, password, api_url):
        try:
            form_data = {"username": username, "password": password}
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = requests.post(api_url, data=form_data, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("data", []) if data.get("error") == 0 else None
        except requests.exceptions.RequestException as error:
            self.stderr.write(f"Error fetching data: {error}")
            return None
