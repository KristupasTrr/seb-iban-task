# SEB IBAN Task
SEB homework task for Junior Software Developer position

## Install required packages
```python
pip install -r requirements.txt
```

## Run app
```console
cd app && python app.py
```

## Home Page
http://localhost:5000/

## API Endpoints
Endpoints that handle IBAN validation

## POST

### http://localhost:5000/api/iban/check-single
| Name | Required |  Type  | Description |
|:----:|:--------:|:------:|:-----------:|
| iban |    Yes   | string | Single IBAN |

Response
```json
{
    "SEB": true,
    "iban": "LT517044077788877777",
    "valid": true
}
```

### http://localhost:5000/api/iban/check-list
|  Name | Required |      Type     |      Description     |
|:-----:|:--------:|:-------------:|:--------------------:|
| ibans |    Yes   | List (string) | List of IBAN strings |

Response
```json
{
    "ibans": [{
            "bank": "SEB",
            "iban": "LT517044077788877777",
            "valid": true
        },
        {
            "bank": "SEB",
            "iban": "LT227044077788877777",
            "valid": false
        },
        {
            "bank": "Swedbank",
            "iban": "LT907300010138808540",
            "valid": true
        }
    ]
}
```

### http://localhost:5000/api/iban/check-international
| Name | Required |  Type  | Description |
|:----:|:--------:|:------:|:-----------:|
| iban |    Yes   | string | Single IBAN |

Response
```json
{
    "iban": "LT517044077788877777",
    "valid": true
}
```
