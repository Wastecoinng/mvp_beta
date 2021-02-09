def barcode_owner(barcode):
    owners = {"502586":"Amstel Malta",
             "544900":"Sprite",
             "603400":"Mirinda/Pepsi",
             }
    barcode_owner = owners[barcode]
    
    return barcode_owner

def barcode_coin(barcode):
    amount = {"502586":"0.5",
             "544900":"0.5",
             "603400":"0.5",
             }
    barcode_amount = amount[barcode]
    
    return barcode_amount
    