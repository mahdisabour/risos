from risos.celery import app
import requests

@app.task
def aiConnection(image_url, ai_url="http://ai:4557"):
    print(f"http://risos:8000{image_url}")
    data = {
        "url": f"http://risos:8000{image_url}",
    }
    response = requests.post(ai_url,json=data)
    return response
