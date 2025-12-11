from app import create_app
from app.tasks import init_celery

app = create_app()
celery = init_celery(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
