from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT ticker_ccl, COUNT(*) as count FROM instrumento_activo GROUP BY ticker_ccl HAVING COUNT(*) > 1;")
            results = cursor.fetchall()
            print(results)