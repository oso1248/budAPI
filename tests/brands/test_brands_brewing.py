from api.validators import val_brands_brewing


def test_get_all_brands(authorized_client, test_brewing_data):
    res = authorized_client.get('/brands/brewing')
    assert len(res.json()) == len(test_brewing_data)
    assert res.status_code == 200


def test_get_all_brands_empty(authorized_client):
    res = authorized_client.get('/brands/brewing')
    assert res.status_code == 404


def test_get_all_brands_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/brands/brewing')
    assert res.status_code == 403


def test_create_brand(authorized_client):
    data = {
        "name": "BRW3",
        "is_organic": False,
        "is_hop_kettle": True,
        "is_hop_dry": False,
        "is_addition": False,
        "note": "string",
        "is_active": True
    }
    res = authorized_client.post('/brands/brewing', json=data)
    brand = val_brands_brewing.BrandBrewingOut(**res.json())
    assert isinstance(brand.id, int)
    assert brand.name == "BRW3"
    assert brand.is_organic == False
    assert brand.is_hop_kettle == True
    assert brand.is_hop_dry == False
    assert brand.is_addition == False
    assert brand.note == "String"
    assert brand.is_active == True
    assert res.status_code == 201


def test_create_brand_unauthorized(authorized_client_permissions_0):
    data = {
        "name": "BRW3",
        "is_organic": False,
        "is_hop_kettle": True,
        "is_hop_dry": False,
        "is_addition": False,
        "note": "string",
        "is_active": True
    }
    res = authorized_client_permissions_0.post('/brands/brewing', json=data)
    assert res.status_code == 403


def test_get_one_brand(authorized_client, test_brewing_data):
    res = authorized_client.get('/brands/brewing/1')
    brand = val_brands_brewing.BrandBrewingOut(**res.json())
    assert brand.id == 1
    assert res.status_code == 200


def test_get_one_brand_empty(authorized_client, test_brewing_data):
    res = authorized_client.get('/brands/brewing/50')
    assert res.status_code == 404


def test_get_one_brand_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/brands/brewing/1')
    assert res.status_code == 403


def test_update_brand(authorized_client, test_brewing_data):
    data = {
        "name": "BRW3",
        "is_organic": False,
        "is_hop_kettle": True,
        "is_hop_dry": False,
        "is_addition": False,
        "note": "string",
        "is_active": True
    }
    res = authorized_client.put('/brands/brewing/1', json=data)
    brand = val_brands_brewing.BrandBrewingOut(**res.json())
    assert brand.id == 1
    assert brand.name == "BRW3"
    assert brand.is_organic == False
    assert brand.is_hop_kettle == True
    assert brand.is_hop_dry == False
    assert brand.is_addition == False
    assert brand.note == "String"
    assert brand.is_active == True
    assert res.status_code == 200


def test_update_brand_unauthorized(authorized_client_permissions_0):
    data = {
        "name": "BRW3",
        "is_organic": False,
        "is_hop_kettle": True,
        "is_hop_dry": False,
        "is_addition": False,
        "note": "string",
        "is_active": True
    }
    res = authorized_client_permissions_0.put('/brands/brewing/1', json=data)
    assert res.status_code == 403


def test_delete_brand(admin_authorized_client, test_brewing_data):
    res = admin_authorized_client.delete('/brands/brewing/1')
    assert res.status_code == 205


def test_delete_brand_unauthorized(authorized_client, test_brewing_data):
    res = authorized_client.delete('/brands/brewing/1')
    assert res.status_code == 403


def test_update_brand_method_acx(authorized_client, test_brewing_data):
    methods_acx = {
        "methods_acx": {
            "pre": {
                "Vertical_Fermenter": {
                    "method": "test method",
                    "note": "string"
                },
                "ACX_Lines": {
                    "method": "string",
                    "note": "string"
                },
                "Chip_Tank": {
                    "method": "string",
                    "note": "string"
                }
            },
            "post": {
                "Vertical_Fermenter": {
                    "method": "string",
                    "note": "string"
                },
                "ACX_Lines": {
                    "method": "string",
                    "note": "string"
                },
                "Chip_Tank": {
                    "method": "string",
                    "note": "string"
                }
            }
        }
    }
    res = authorized_client.put(
        '/brands/brewing/method/acx/1', json=methods_acx)
    brand = res.json()
    assert brand['methods_acx']['pre']['Vertical_Fermenter']['method'] == "Test Method"
    assert res.status_code == 200


def test_update_brand_method_acx_unauthorized(authorized_client_permissions_0):
    methods_acx = {
        "methods_acx": {
            "pre": {
                "Vertical_Fermenter": {
                    "method": "test method",
                    "note": "string"
                },
                "ACX_Lines": {
                    "method": "string",
                    "note": "string"
                },
                "Chip_Tank": {
                    "method": "string",
                    "note": "string"
                }
            },
            "post": {
                "Vertical_Fermenter": {
                    "method": "string",
                    "note": "string"
                },
                "ACX_Lines": {
                    "method": "string",
                    "note": "string"
                },
                "Chip_Tank": {
                    "method": "string",
                    "note": "string"
                }
            }
        }
    }
    res = authorized_client_permissions_0.put(
        '/brands/brewing/method/acx/1', json=methods_acx)
    assert res.status_code == 403


def test_update_brand_method_csx(authorized_client, test_brewing_data):
    methods_csx = {
        "methods_csx": {
            "pre": {
                "Chip_Tank": {
                    "method": "test method",
                    "note": "string"
                },
                "Uni_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Train": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Receiver": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Fill_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Seperators": {
                    "method": "string",
                    "note": "string"
                },
                "ACP_Addition": {
                    "method": "string",
                    "note": "string"
                },
                "Bypass_Pre_Cooler": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Tank": {
                    "method": "string",
                    "note": "string"
                }
            },
            "post": {
                "Chip_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Uni_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Train": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Receiver": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Fill_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Seperators": {
                    "method": "string",
                    "note": "string"
                },
                "ACP_Addition": {
                    "method": "string",
                    "note": "string"
                },
                "Bypass_Pre_Cooler": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Tank": {
                    "method": "string",
                    "note": "string"
                }
            }
        }
    }
    res = authorized_client.put(
        '/brands/brewing/method/csx/1', json=methods_csx)
    brand = res.json()
    assert brand['methods_csx']['pre']['Chip_Tank']['method'] == "Test Method"
    assert res.status_code == 200


def test_update_brand_method_csx_unauthorized(authorized_client_permissions_0):
    methods_csx = {
        "methods_csx": {
            "pre": {
                "Chip_Tank": {
                    "method": "test method",
                    "note": "string"
                },
                "Uni_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Train": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Receiver": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Fill_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Seperators": {
                    "method": "string",
                    "note": "string"
                },
                "ACP_Addition": {
                    "method": "string",
                    "note": "string"
                },
                "Bypass_Pre_Cooler": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Tank": {
                    "method": "string",
                    "note": "string"
                }
            },
            "post": {
                "Chip_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Uni_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Train": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Receiver": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Fill_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Seperators": {
                    "method": "string",
                    "note": "string"
                },
                "ACP_Addition": {
                    "method": "string",
                    "note": "string"
                },
                "Bypass_Pre_Cooler": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Tank": {
                    "method": "string",
                    "note": "string"
                }
            }
        }
    }
    res = authorized_client_permissions_0.put(
        '/brands/brewing/method/csx/1', json=methods_csx)
    assert res.status_code == 403
