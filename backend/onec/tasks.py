import os
from django.db import IntegrityError
import requests
from django.conf import settings
from celery import shared_task
from .models import Organization, Specification, Nomenclature, Price, Balance


HOST = os.getenv('ONEC_HOST', 'http://localhost:8000')
USERNAME = os.getenv('ONEC_USERNAME')
PASSWORD = os.getenv('ONEC_PASSWORD')

@shared_task
def sync_db():
    data = _request()
    _sync_organizations(data.get('ORGANIZATIONS', {}))
    _sync_specifications(data.get('SPECIFICATIONS', {}))
    _sync_nomenclatures(data.get('ITEMS', {}))
    _sync_prices(data.get('PRICE', {}))
    _sync_balances(data.get('BALANCES', {}))


def _request():
    if settings.DEBUG: return {}
    url = HOST + "/accounting_copy/hs/career/data"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    if not response.ok:
        raise Exception(f"Failed to sync data from {url}: {response.status_code}")

    return response.json()


def _sync_organizations(data):
    for org_data in data.values():
        defaults={
            'name': org_data.get('NAME'),
            'fullname': org_data.get('FULLNAME'),
            'inn': org_data.get('INN'),
            'kpp': org_data.get('KPP'),
        }
        try:
            org = Organization.objects.get(uuid=org_data['XML_ID'])
            Organization.objects.filter(uuid=org_data['XML_ID']).update(**{
                key: value for key, value in defaults.items() if value is not None
            })
            created = False
        except Organization.DoesNotExist:
            org = Organization.objects.create(uuid=org_data['XML_ID'], **defaults)
            created = True
        print("Created" if created else "Updated", org)


def _sync_specifications(data):
    for spec_data in data.values():
        defaults={
            'name': spec_data.get('NAME'),
            'delivery_address': spec_data.get('DELIVERY_ADDRESS'),
            'payment_deferment': spec_data.get('PAYMENT_DEFERMENT'),
            'amount_limit': spec_data.get('AMOUNT_LIMIT'),
        }
        try:
            spec = Specification.objects.get(uuid=spec_data['XML_ID'])
            Specification.objects.filter(uuid=spec_data['XML_ID']).update(**{
                key: value for key, value in defaults.items() if value is not None
            })
            created = False
        except Specification.DoesNotExist:
            spec = Specification.objects.create(uuid=spec_data['XML_ID'], **defaults)
            created = True
        print("Created" if created else "Updated", spec)


def _sync_nomenclatures(data):
    for nom_data in data.values():
        defaults={
            'name': nom_data['NAME'],
            'unit': nom_data['UNIT'],
        }
        try:
            nom = Nomenclature.objects.get(uuid=nom_data['XML_ID'])
            Nomenclature.objects.filter(uuid=nom_data['XML_ID']).update(**{
                key: value for key, value in defaults.items() if value is not None
            })
            created = False
        except Nomenclature.DoesNotExist:
            nom = Nomenclature.objects.create(uuid=nom_data['XML_ID'], **defaults)
            created = True
        print("Created" if created else "Updated", nom)


def _sync_prices(data):
    for price_data in data.values():
        try:
            nomenclature = Nomenclature.objects.get(uuid=price_data['ITEM_ID'])
            specification = Specification.objects.get(uuid=price_data['SPECIFICATION_ID'])
        except (Nomenclature.DoesNotExist, Specification.DoesNotExist):
            print("Skipping price update due to missing nomenclature or specification", price_data)
            continue

        defaults={
            'date': price_data['DATE'],
            'price': price_data['PRICE'],
        }
        try:
            price = Price.objects.get(nomenclature=nomenclature, specification=specification)
            Price.objects.filter(nomenclature=nomenclature, specification=specification).update(**{
                key: value for key, value in defaults.items() if value is not None
            })
            created = False
        except Price.DoesNotExist:
            price = Price.objects.create(nomenclature=nomenclature, specification=specification, **defaults)
            created = True
        print("Created" if created else "Updated", price)


def _sync_balances(data):
    for balance_data in data.values():
        try:
            specification = Specification.objects.get(uuid=balance_data['SPECIFICATION_ID'])
        except Specification.DoesNotExist:
            print("Skipping balance update due to missing specification", balance_data)
            continue

        defaults={
            'balance': balance_data['BALANCE'],
        }
        try:
            balance = Balance.objects.get(specification=specification)
            Balance.objects.filter(specification=specification).update(**{
                key: value for key, value in defaults.items() if value is not None
            })
            created = False
        except Balance.DoesNotExist:
            balance = Balance.objects.create(specification=specification, **defaults)
            created = True
        print("Created" if created else "Updated", balance)
