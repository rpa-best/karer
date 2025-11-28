import os
import requests
from django.conf import settings
from celery import shared_task
from .models import Organization, Specification, Nomenclature, Price, Balance, Car, Driver, Sender


HOST = os.getenv('ONEC_HOST', 'http://localhost:8000')
USERNAME = os.getenv('ONEC_USERNAME')
PASSWORD = os.getenv('ONEC_PASSWORD')

@shared_task
def sync_db():
    results = {}
    for sender in Sender.objects.all():
        data, status = _request(sender.url)
        _sync_nomenclatures(data.get('ITEMS', {}))
        _sync_organizations(data.get('ORGANIZATIONS', {}))
        _sync_specifications(data.get('SPECIFICATIONS', {}))
        _sync_prices(data.get('PRICE', {}))
        _sync_balances(data.get('BALANCES', {}))
        _sync_cars(data.get('VEHICLES', {}))
        _sync_drivers(data.get('DRIVERS', {}))
        results[sender.name] = status
    return results


def _request(url: str):
    url = HOST + url
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    if not response.ok:
        raise Exception(f"Failed to sync data from {url}: {response.status_code}")

    return response.json(), response.status_code


@shared_task
def send_order_onec(order_id):
    from invoice.models import Order
    
    if settings.DEBUG: return {}
    url = HOST + "/accounting_copy/hs/career/invoice"

    order = Order.objects.get(id=order_id)
    data = {
        "XML_ID": str(order.uuid),
        "DATE": str(order.created_at),
        "SPECIFICATION_ID": str(order.invoice.specification_id),
        "SHIPPER_ID": None,
        "CONSIGNEE_ID": str(order.invoice.org_id),
        "CARRIER_ID": None,
        "PACKAGE": order.desc,
        "DELIVERY": str(order.delivery_id),
        "COMMENT": order.comment,
        "DRIVER_ID": order.driver_id,
        "VEHICLE_ID": order.car_id,
        "DOCUMENTS": None,
        "TRANS_INFO": None,
        "ITEMS": [{
            "ITEM_ID": order.nomenclature_id,
            "QUANTITY": order.fact,
        }]
    }
    response = requests.post(url, json=data, auth=(USERNAME, PASSWORD))
    if not response.ok:
        raise Exception(f"Failed to sync data from {url}: {response.status_code}")
    return response


def _sync_organizations(data):
    for org_data in data.values():
        defaults={
            'name': org_data.get('NAME'),
            'fullname': org_data.get('FULLNAME'),
            'inn': org_data.get('INN'),
            'kpp': org_data.get('KPP'),
            'do_not_display_volume': org_data.get('DO_NOT_DISPLAY_VOLUME')
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
        try:
            organization = Organization.objects.get(uuid=spec_data.get('ORGANIZATION_ID'))
        except Organization.DoesNotExist:
            print("Skipping specification update due to missing organization", spec_data)
            continue
        defaults={
            'name': spec_data.get('NAME'),
            'delivery_address': spec_data.get('DELIVERY_ADDRESS'),
            'payment_deferment': spec_data.get('PAYMENT_DEFERMENT'),
            'amount_limit': spec_data.get('AMOUNT_LIMIT'),
            'organization': organization,
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
        for item in spec_data.get('ITEMS', {}).values():
            if spec.nomenclatures.filter(uuid=item).exists():
                continue
            nomenclature = Nomenclature.objects.filter(uuid=item).first()
            if nomenclature:
                spec.nomenclatures.add(nomenclature)
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
            'price': price_data['PRICE'],
        }
        try:
            price = Price.objects.get(nomenclature=nomenclature, specification=specification, date=price_data['DATE'])
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


def _sync_cars(data):
    for car_data in data.values():
        defaults={
            'name': car_data['NAME'],
            'reg_number': car_data['REG_NUMBER'],
            'brand': car_data['BRAND'],
            'our_prorerty': car_data['OUR_PROPERTY'],
            'trailer_reg_number': car_data['TRAILER_REG_NUMBER'],
            'trailer_brand': car_data['TRAILER_BRAND']
        }
        try:
            car = Car.objects.get(uuid=car_data['XML_ID'])
            Car.objects.filter(uuid=car_data['XML_ID']).update(**{
                key: value for key, value in defaults.items() if value is not None
            })
            created = False
        except Car.DoesNotExist:
            car = Car.objects.create(uuid=car_data['XML_ID'], **defaults)
            created = True
        print("Created" if created else "Updated", car)


def _sync_drivers(data):
    for driver_data in data.values():
        defaults={
            'name': driver_data['NAME'],
            'inn': driver_data['INN'],
            'phone_number': driver_data['PHONE_NUMBER'],
            'job_title': driver_data['JOB_TITLE'],
            'drivers_license_series': driver_data['DRIVERS_LICENSE_SERIES'],
            'drivers_license_number': driver_data['DRIVERS_LICENSE_NUMBER']
        }
        try:
            driver = Driver.objects.get(uuid=driver_data['XML_ID'])
            Driver.objects.filter(uuid=driver_data['XML_ID']).update(**{
                key: value for key, value in defaults.items() if value is not None
            })
            created = False
        except Driver.DoesNotExist:
            driver = Driver.objects.create(uuid=driver_data['XML_ID'], **defaults)
            created = True
        print("Created" if created else "Updated", driver)
