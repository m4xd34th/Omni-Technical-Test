from celery import app  # , Celery
# app = Celery()


@app.shared_task()
def send_email_notification(a, b):
    return a + b
