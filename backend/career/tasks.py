import requests
from requests.exceptions import RequestException
from celery import shared_task
from notification.consumers import send_notification
from notification.models import Notification, SEVERITY_DANGER, SEVERITY_SUCCESS
from oauth.models import User, ROLE_LOGIST


ORDER_URL = '/order/{order_id}/'
ORDER_SEND_MESSAGE = 'Заказ отправлена в карерь'
ORDER_ACCEPTED_MESSAGE = 'Карерь получил заказ'
ORDER_ERROR_MESSAGE = 'Заказ не отправлен. Попробуйте позже.'
ORDER_LABEL_MESSAGE = 'Информация о заказе'

def _send_notifications(order_id, users, message, severity):
    notifications = []
    for user in users:
        notifications.append(Notification(
            user=user, label=ORDER_LABEL_MESSAGE,
            redirect_url=ORDER_URL.format(order_id=order_id),
            message=message,
            severity=severity
        ))
    notifications = Notification.objects.bulk_create(notifications)
    for notification in notifications:
        send_notification(notification)


@shared_task
def send_order_career(order_id, delete=False):
    from invoice.serializers import OrderShowSerializer
    from invoice.models import Order

    if delete:
        order = Order.objects.get(pk=order_id)
        data = OrderShowSerializer(order).data
    else:
        data = {'uuid': order_id}

    data['delete'] = delete
    users = User.objects.filter(
        role=ROLE_LOGIST
    )
    _send_notifications(order_id, users, ORDER_SEND_MESSAGE, SEVERITY_SUCCESS)
    try:
        url = ''
        response = requests.post(url, json=data)
        if response.ok:
            _send_notifications(order_id, users, ORDER_ACCEPTED_MESSAGE, SEVERITY_SUCCESS)
        else:
            _send_notifications(order_id, users, ORDER_ERROR_MESSAGE, SEVERITY_DANGER)
        return response
    except Exception as e:
        print(e)
        _send_notifications(order_id, users, ORDER_ERROR_MESSAGE, SEVERITY_DANGER)
    return None
