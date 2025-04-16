import os
import requests
from celery import shared_task
from .models import Organization, Specification, Nomenclature, Price, Balance


HOST = os.getenv('ONEC_HOST', 'http://localhost:8000')


@shared_task
def sync_db():
    url = HOST + "/accounting_copy/hs/career/data"
    response = requests.get(url)
    if not response.ok:
        raise Exception(f"Failed to sync data from {url}: {response.status_code}")

    data = response.json()




def _sync_organizations(data):
    for org_data in data:
        org, created = Organization.objects.update_or_create(
            uuid=org_data['uuid'],
            defaults={
                'name': org_data['name'],
                'fullname': org_data['fullname'],
                'inn': org_data['inn'],
                'kpp': org_data['kpp'],
            }
        )
        print("Created" if created else "Updated", org)


def _sync_specifications(data):
    for spec_data in data:
        spec, created = Specification.objects.update_or_create(
            uuid=spec_data['uuid'],
            defaults={
                'name': spec_data['name'],
                'delivery_address': spec_data.get('delivery_address', ''),
                'payment_deferment': spec_data.get('payment_deferment', 0),
                'amount_limit': spec_data.get('amount_limit', 0),
            }
        )
        print("Created" if created else "Updated", spec)


def _sync_nomenclatures(data):
    for nom_data in data:
        nom, created = Nomenclature.objects.update_or_create(
            uuid=nom_data['uuid'],
            defaults={
                'name': nom_data['name'],
                'unit': nom_data['unit'],
            }
        )
        print("Created" if created else "Updated", nom)


def _sync_prices(data):
    for price_data in data:
        try:
            nomenclature = Nomenclature.objects.get(uuid=price_data['nomenclature'])
            specification = Specification.objects.get(uuid=price_data['specification'])
        except (Nomenclature.DoesNotExist, Specification.DoesNotExist):
            print("Skipping price update due to missing nomenclature or specification", price_data)
            continue

        price, created = Price.objects.update_or_create(
            nomenclature=nomenclature,
            specification=specification,
            defaults={
                'date': price_data['date'],
                'price': price_data['price'],
            }
        )
        print("Created" if created else "Updated", price)


def _sync_balances(data):
    for balance_data in data:
        try:
            specification = Specification.objects.get(uuid=balance_data['specification'])
        except Specification.DoesNotExist:
            print("Skipping balance update due to missing specification", balance_data)
            continue

        balance, created = Balance.objects.update_or_create(
            specification=specification,
            defaults={
                'balance': balance_data['balance'],
            }
        )
        print("Created" if created else "Updated", balance)
