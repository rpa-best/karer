from celery import shared_task
from notification.consumers import send_notification
from notification.models import Notification, SEVERITY_DANGER

from invoice.constants import (
    ORDER_DRIVER_COMMENT_ERROR_MESSAGE, 
    ORDER_LABEL_MESSAGE, ORDER_URL, 
    COMMENT_STATUS_OK, COMMENT_STATUS_ERROR, COMMENT_STATUS_LOADING
)


@shared_task
def send_driver_comment(comment_id, user_id):
    from invoice.models import DriverComment
    
    comment = DriverComment.objects.select_related('order', 'order__driver').get(pk=comment_id)
    comment.status = COMMENT_STATUS_LOADING
    comment.save()
    try:
        comment.order.driver.send_comment(comment.text)
        comment.status = COMMENT_STATUS_OK
    except ConnectionError:
        comment.status = COMMENT_STATUS_ERROR
        send_notification(Notification.objects.create(
            user_id=user_id, label=ORDER_LABEL_MESSAGE,
            redirect_url=ORDER_URL.format(order_id=comment.order.id),
            message=ORDER_DRIVER_COMMENT_ERROR_MESSAGE,
            severity=SEVERITY_DANGER
        ))
    comment.save()