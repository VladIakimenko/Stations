from django.core.management.base import BaseCommand
from django.conf import settings
import csv
import sqlite3


class Command(BaseCommand):
    help = 'Load data from CSV and save it to the database'

    def handle(self, *args, **options):
        with open(settings.BUS_STATION_CSV, 'rt', encoding='UTF-8') as sourcefile:
            reader = csv.reader(sourcefile)
            next(reader)
            data = [
                {
                    'name': row[1],
                    'street': row[4],
                    'district': row[6],
                    'organization': row[11],
                } for row in reader
            ]

        conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
        cursor = conn.cursor()

        tablename = 'stations'
        columns = ', '.join(data[0].keys())

        query = f"CREATE TABLE IF NOT EXISTS {tablename} ({columns})"
        cursor.execute(query)

        for line in data:
            columns = ', '.join(line.keys())
            placeholders = ':' + ', :'.join(line.keys())
            query = f"INSERT INTO {tablename} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, line)

        conn.commit()
        cursor.close()
        conn.close()
