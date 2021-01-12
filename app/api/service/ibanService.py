import sys
import traceback
import re
from flask import jsonify
from string import ascii_uppercase


class IBANService:
    def __init__(self, request_data):
        self.data = request_data
        self.banks = {"70440": "SEB", "73000": "Swedbank", "40100": "Luminor"}
        self.every_country_regex = "^(?=[0-9A-Z]{28}$)AL\d{10}[0-9A-Z]{16}$|^(?=[0-9A-Z]{24}$)AD\d{10}[0-9A-Z]{12}$|^(?=[0-9A-Z]{20}$)AT\d{18}$|^(?=[0-9A-Z]{22}$)BH\d{2}[A-Z]{4}[0-9A-Z]{14}$|^(?=[0-9A-Z]{16}$)BE\d{14}$|^(?=[0-9A-Z]{20}$)BA\d{18}$|^(?=[0-9A-Z]{22}$)BG\d{2}[A-Z]{4}\d{6}[0-9A-Z]{8}$|^(?=[0-9A-Z]{21}$)HR\d{19}$|^(?=[0-9A-Z]{28}$)CY\d{10}[0-9A-Z]{16}$|^(?=[0-9A-Z]{24}$)CZ\d{22}$|^(?=[0-9A-Z]{18}$)DK\d{16}$|^FO\d{16}$|^GL\d{16}$|^(?=[0-9A-Z]{28}$)DO\d{2}[0-9A-Z]{4}\d{20}$|^(?=[0-9A-Z]{20}$)EE\d{18}$|^(?=[0-9A-Z]{18}$)FI\d{16}$|^(?=[0-9A-Z]{27}$)FR\d{12}[0-9A-Z]{11}\d{2}$|^(?=[0-9A-Z]{22}$)GE\d{2}[A-Z]{2}\d{16}$|^(?=[0-9A-Z]{22}$)DE\d{20}$|^(?=[0-9A-Z]{23}$)GI\d{2}[A-Z]{4}[0-9A-Z]{15}$|^(?=[0-9A-Z]{27}$)GR\d{9}[0-9A-Z]{16}$|^(?=[0-9A-Z]{28}$)HU\d{26}$|^(?=[0-9A-Z]{26}$)IS\d{24}$|^(?=[0-9A-Z]{22}$)IE\d{2}[A-Z]{4}\d{14}$|^(?=[0-9A-Z]{23}$)IL\d{21}$|^(?=[0-9A-Z]{27}$)IT\d{2}[A-Z]\d{10}[0-9A-Z]{12}$|^(?=[0-9A-Z]{20}$)[A-Z]{2}\d{5}[0-9A-Z]{13}$|^(?=[0-9A-Z]{30}$)KW\d{2}[A-Z]{4}22!$|^(?=[0-9A-Z]{21}$)LV\d{2}[A-Z]{4}[0-9A-Z]{13}$|^(?=[0-9A-Z]{,28}$)LB\d{6}[0-9A-Z]{20}$|^(?=[0-9A-Z]{21}$)LI\d{7}[0-9A-Z]{12}$|^(?=[0-9A-Z]{20}$)LT\d{18}$|^(?=[0-9A-Z]{20}$)LU\d{5}[0-9A-Z]{13}$|^(?=[0-9A-Z]{19}$)MK\d{5}[0-9A-Z]{10}\d{2}$|^(?=[0-9A-Z]{31}$)MT\d{2}[A-Z]{4}\d{5}[0-9A-Z]{18}$|^(?=[0-9A-Z]{27}$)MR13\d{23}$|^(?=[0-9A-Z]{30}$)MU\d{2}[A-Z]{4}\d{19}[A-Z]{3}$|^(?=[0-9A-Z]{27}$)MC\d{12}[0-9A-Z]{11}\d{2}$|^(?=[0-9A-Z]{22}$)ME\d{20}$|^(?=[0-9A-Z]{18}$)NL\d{2}[A-Z]{4}\d{10}$|^(?=[0-9A-Z]{15}$)NO\d{13}$|^(?=[0-9A-Z]{28}$)PL\d{10}[0-9A-Z]{,16}n$|^(?=[0-9A-Z]{25}$)PT\d{23}$|^(?=[0-9A-Z]{24}$)RO\d{2}[A-Z]{4}[0-9A-Z]{16}$|^(?=[0-9A-Z]{27}$)SM\d{2}[A-Z]\d{10}[0-9A-Z]{12}$|^(?=[0-9A-Z]{,24}$)SA\d{4}[0-9A-Z]{18}$|^(?=[0-9A-Z]{22}$)RS\d{20}$|^(?=[0-9A-Z]{24}$)SK\d{22}$|^(?=[0-9A-Z]{19}$)SI\d{17}$|^(?=[0-9A-Z]{24}$)ES\d{22}$|^(?=[0-9A-Z]{24}$)SE\d{22}$|^(?=[0-9A-Z]{21}$)CH\d{7}[0-9A-Z]{12}$|^(?=[0-9A-Z]{24}$)TN59\d{20}$|^(?=[0-9A-Z]{26}$)TR\d{7}[0-9A-Z]{17}$|^(?=[0-9A-Z]{,23}$)AE\d{21}$|^(?=[0-9A-Z]{22}$)GB\d{2}[A-Z]{4}\d{14}$"

    """
    Validate every country IBAN with provided Regex for 54 countries.
    """
    def validate_every_country(self):
        try:
            data = self.data.get_json()
            if ('iban' in data and len(data) == 1):
                
                # check if iban format is valid using regex
                if re.match(self.every_country_regex, data["iban"]):
                    valid = self.validate_iban(data["iban"].strip())

                    if valid:
                        return jsonify({"valid": True, "iban": data["iban"]}), 200
                    else:
                        return jsonify({"valid": False, "iban": data["iban"]}), 200
                else:
                    return jsonify({"valid": False, "iban": data["iban"]}), 200

            else:
                return jsonify({"error":"Wrong arguments"}), 400
        except:
            return jsonify({"error":"Bad JSON format"}), 400

    """
    Validate IBAN 
    """
    def validate_iban(self, iban):
        letters_with_index = {}

        # create character and index dictionary (A: 10, B:11, ...)
        index = 10
        for c in ascii_uppercase:
            letters_with_index[c] = str(index)
            index += 1

        # rearrange iban 
        try:
            changed_iban = int(iban[4:] + letters_with_index[iban[0]] + letters_with_index[iban[1]] + iban[2:4])
        except:
            return False

        # calculate mod and return True if valid
        if (changed_iban % 97 == 1):
            return True

        return False

    """
    Validate single IBAN and check if it belongs to SEB 
    """
    def validate_single(self):
        try:
            data = self.data.get_json()
            valid = False
            if ('iban' in data and len(data) == 1):
                data["iban"] = data["iban"].strip()
                # validate iban
                valid = self.validate_iban(data["iban"])
                # check if bank is SEB
                is_seb = False
                if data["iban"][4:9] == "70440":
                    is_seb = True

                # return json response
                if valid:
                    return jsonify({"iban": data["iban"], "valid": True, "SEB": is_seb}), 200
                else:
                    return jsonify({"iban": data["iban"], "valid": False, "SEB": is_seb}), 200
            else:
                return jsonify({"error":"Wrong arguments"}), 401
        except:
            return jsonify({"error":"Bad JSON format"}), 400
     
    """
    Validate list of IBANs and check which bank it belongs to 
    """
    def validate_multiple(self):
        try:
            data = self.data.get_json()
            valid = False
            if ('ibans' in data and len(data) == 1 ):
                
                validated_ibans = []

                # validate every given iban
                for iban in data["ibans"]:
                    iban = iban.strip()
                    bank = ""
                    valid = self.validate_iban(iban)

                    # check for bank
                    if (iban[4:9] in self.banks):
                        bank = self.banks[iban[4:9]]

                    if valid:
                        validated_ibans.append({"iban": iban, "valid": True, "bank": bank})
                    else:
                        validated_ibans.append({"iban": iban, "valid": False, "bank": bank})

                return jsonify({"ibans": validated_ibans})
            else:
                return jsonify({"error":"Wrong arguments"}), 400
        except:
            return jsonify({"error":"Bad JSON format"}), 400

