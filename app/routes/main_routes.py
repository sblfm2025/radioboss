from flask import Blueprint, render_template

# Definisikan blueprint untuk rute utama stasiun radio
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Merender antarmuka dashboard Web UI stasiun radio."""
    return render_template('index.html')
