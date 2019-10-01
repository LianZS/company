import os
from celery import Celery
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company.settings')  # 将celery加载到全局-----非常重要的一步

BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/2"
# 添加需要加载的任务模块
CELERY_IMPORTS = ("monitoring.monitoring_goods",)
# 生成任务队列
CELERY_QUEUES = (
    Queue('PinDuoDuo', routing_key='monitoring.monitoring_goods.#', exchange=Exchange('PinDuoDuo', type='direct')),

)
# 任务路由器
CELERY_ROUTES = {
    "monitoring.tasmonitoring_goodsks.#": {'queue': "PinDuoDuo"},

}
CELERYD_CONCURRENCY = 10  # 设置并发的worker数量

CELERYD_MAX_TASKS_PER_CHILD = 1  # 每个worker最多执行1个任务被销毁，可以防止内存泄漏
CELERY_TASK_ACKS_LATE = True  # 允许重试
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['application/x-python-serialize']
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
app = Celery("celery")
