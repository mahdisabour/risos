import requests
from risos.celery import app


@app.task
def pushNotification(msg, devices_ids, notif_inatance):
    TOKEN = 'YOUR_TOKEN'

    headers = {
        'Authorization': 'Token ' + TOKEN,
        'Content-Type': 'application/json'
    }

    data = {
        'app_ids': ['5dn6jvvkzomyl0je', ],
        'data': {
            'title': 'test title',
            'content': 'test content',
        },
        'filters': {
            'device_id': [id for id in devices_ids]
        },
    }

    response = requests.post(
        'https://api.pushe.co/v2/messaging/notifications/web/',
        json=data,
        headers=headers,
    )


    if response.status_code == 201:
        data = response.json()
        # hashed_id only generated for Non-Free plan
        if data['hashed_id']:
            report_url = 'https://pushe.co/report?id=%s' % data['hashed_id']
        else:
            report_url = 'no report url for your plan'

        notif_id = data['wrapper_id']
        notif_inatance.status = "success"
        notif_inatance.report_url = report_url
        notif_inatance.notif_id = notif_id
        notif_inatance.save()

    else:
        notif_inatance.status = "failed"
        notif_inatance.save()

