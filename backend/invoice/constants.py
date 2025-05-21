
TYPE_PREPAYMENT = 'prepayment'
TYPE_DEFERMENT_PAYMENT = 'deferment_payment'
TYPE_LIMIT = 'limit'
TYPES = (
    (TYPE_PREPAYMENT, 'Предоплата'),
    (TYPE_DEFERMENT_PAYMENT, 'Отсрочка платежа'),
    (TYPE_LIMIT, 'Лимит')
)

STATUS_CREATED = 'created'
STATUS_PROCESS = 'process'
STATUS_DONE = 'done'
STATUS_CANCELED = 'canceled'
STATUSES = (
    (STATUS_CREATED, 'Принято'),
    (STATUS_PROCESS, 'В обработке'),
    (STATUS_DONE, 'Успешно'),
    (STATUS_CANCELED, 'Отклонено')
)

COMMENT_STATUS_LOADING = 'loading'
COMMENT_STATUS_OK = 'ok'
COMMENT_STATUS_ERROR = 'error'
COMMENT_STATUSES = (
    (COMMENT_STATUS_LOADING, 'Загрузка'),
    (COMMENT_STATUS_OK, 'Успешно'),
    (COMMENT_STATUS_ERROR, 'Ошибка')
)

ORDER_URL = '/order/{order_id}/'
ORDER_DRIVER_COMMENT_ERROR_MESSAGE = 'Заказ не отправлен. Попробуйте позже.'
ORDER_LABEL_MESSAGE = 'Информация о отправке коментария'