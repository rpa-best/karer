import os
import requests
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
    url = HOST + "/accounting_copy/hs/career/data"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    if not response.ok:
        raise Exception(f"Failed to sync data from {url}: {response.status_code}")

    return response.json()


def _sync_organizations(data):
    for org_data in data.values():
        org, created = Organization.objects.update_or_create(
            uuid=org_data['XML_ID'],
            defaults={
                'name': org_data['NAME'],
                'fullname': org_data['FULLNAME'],
                'inn': org_data['INN'],
                'kpp': org_data['KPP'],
            }
        )
        print("Created" if created else "Updated", org)


def _sync_specifications(data):
    for spec_data in data.values():
        spec, created = Specification.objects.update_or_create(
            uuid=spec_data['XML_ID'],
            defaults={
                'name': spec_data['NAME'],
                'delivery_address': spec_data.get('DELIVERY_ADDRESS', ''),
                'payment_deferment': spec_data.get('PAYMENT_DEFERMENT', 0),
                'amount_limit': spec_data.get('AMOUNT_LIMIT', 0),
            }
        )
        print("Created" if created else "Updated", spec)


def _sync_nomenclatures(data):
    for nom_data in data.values():
        nom, created = Nomenclature.objects.update_or_create(
            uuid=nom_data['XML_ID'],
            defaults={
                'name': nom_data['NAME'],
                'unit': nom_data['UNIT'],
            }
        )
        print("Created" if created else "Updated", nom)


def _sync_prices(data):
    for price_data in data.values():
        try:
            nomenclature = Nomenclature.objects.get(uuid=price_data['ITEM_ID'])
            specification = Specification.objects.get(uuid=price_data['SPECIFICATION_ID'])
        except (Nomenclature.DoesNotExist, Specification.DoesNotExist):
            print("Skipping price update due to missing nomenclature or specification", price_data)
            continue

        price, created = Price.objects.update_or_create(
            nomenclature=nomenclature,
            specification=specification,
            defaults={
                'date': price_data['DATE'],
                'price': price_data['PRICE'],
            }
        )
        print("Created" if created else "Updated", price)


def _sync_balances(data):
    for balance_data in data.values():
        try:
            specification = Specification.objects.get(uuid=balance_data['SPECIFICATION_ID'])
        except Specification.DoesNotExist:
            print("Skipping balance update due to missing specification", balance_data)
            continue

        balance, created = Balance.objects.update_or_create(
            specification=specification,
            defaults={
                'balance': balance_data['BALANCE'],
            }
        )
        print("Created" if created else "Updated", balance)
