import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import HttpResponse

from django.conf import settings


def extract_data():
    conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM stations;"
    cursor.execute(query)
    rows = cursor.fetchall()

    data = []
    for row in rows:
        row_dict = dict(row)
        data.append(row_dict)

    cursor.close()
    conn.close()
    return data


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    search_term = request.GET.get('search', '')

    filtered_data = [station for station in extract_data() if any(search_term.lower() in value.lower() for value in station.values())]

    page_num = request.GET.get('page', 1)
    try:
        page_num = int(page_num)
        assert page_num > 0
    except (ValueError, AssertionError):
        return HttpResponse(f'Incorrect page {page_num}!<br>Must be a positive integer.')

    paginator = Paginator(filtered_data, 10)
    page = paginator.get_page(page_num)

    context = {
        'page': page,
        'search_term': search_term
    }
    return render(request, 'stations/index.html', context)
