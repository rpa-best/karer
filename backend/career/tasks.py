import requests
from celery import shared_task


@shared_task
def send_to_career(order_id):
    from invoice.serializers import OrderShowSerializer
    from invoice.models import Order

    order = Order.objects.get(pk=order_id)
    data = OrderShowSerializer(order).data
    url = ''
    response = requests.post(url, json=data)
    return response.json()
