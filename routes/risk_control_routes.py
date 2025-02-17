from flask import Blueprint, request
import requests

risk_control_bp = Blueprint('risk_control', __name__, url_prefix='/risk_control')

@risk_control_bp.route('/submit', methods=['POST'])
def submit():
    url = "http://120.77.248.212:9090/drms/risk_management/white/add"
    headers = {
        'Content-Type': 'application/json'
    }
    phones_data = request.get_json()
    response = requests.post(url, headers=headers, json=phones_data)
    return response.json()

@risk_control_bp.route('/submit_market', methods=['POST'])
def submit_market():
    url = "http://120.77.248.212:9090/drms/risk_management/market_hl/add"
    headers = {
        'Content-Type': 'application/json'
    }
    market_data = request.get_json()
    response = requests.post(url, headers=headers, json=market_data)
    return response.json() 