from flask import Blueprint, request, jsonify
from api.service.ibanService import IBANService


iban_api = Blueprint('api', __name__)

"""
Endpoint for Lithuanian IBAN validation (check if it belongs to SEB)
"""
@iban_api.route('/check-single', methods=['POST'])
def validate_single_iban():
    iban_service = IBANService(request_data = request)
    return iban_service.validate_single()

"""
Endpoint for list of Lithuanian IBANs validation (check which bank as well)
"""
@iban_api.route('/check-list', methods=['POST'])
def validate_multiple_iban():
    iban_service = IBANService(request_data = request)
    return iban_service.validate_multiple()

"""
Endpoint for single IBAN validation (54 countries)
"""
@iban_api.route('/check-international', methods=['POST'])
def validate_every_country_iban():
    iban_service = IBANService(request_data = request)
    return iban_service.validate_every_country()