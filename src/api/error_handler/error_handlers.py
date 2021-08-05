from httpcats import cat_by_code
from PIL import Image
from io import BytesIO

from flask import Flask, request, jsonify, render_template, Blueprint

# templates = Blueprint('templates', __name__, template_folder='templates')

app = Flask(__name__)

class ErrorHandlers:
    def APIErrorHandler(self, error_code):
        http_cat_image = cat_by_code(error_code)

        return http_cat_image

    def not_found(self, error_description, error_code):
        http_cat_image = self.APIErrorHandler(error_code)

        return render_template('public/error/error_template.html', cat_image=http_cat_image, error_message_description=error_description), error_code
