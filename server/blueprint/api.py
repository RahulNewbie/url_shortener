from flask import Blueprint, current_app, request
from url_shortener.url_shortener import url_shortener
import logging
from flask_api import status


api = Blueprint('api', __name__)


@api.route('/url/', methods=['POST'])
def shorten_url():
    url = request.get_data().decode("utf-8")
    try:
        url_id = current_app.config['DB'].insert_movie_data(url)
        shortened_url = url_shortener(url_id)
        return shortened_url, status.HTTP_200_OK
    except OSError:
        logging.error('Error occurred while storing the url into database')
        return "Error", status.HTTP_500_INTERNAL_SERVER_ERROR


