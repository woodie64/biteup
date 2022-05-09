from flask import Blueprint, url_for
from werkzeug.utils import redirect
from django.views.decorators.csrf import csrf_exempt
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    return redirect(url_for('index.trade'))


@csrf_exempt
def my_view(request):
    return HttpResponse('Hello world')