from api.validators import val_brands_finishing


def test_get_all_brands(authorized_client, test_finishing_data):
    res = authorized_client.get('/brands/finishing')
    assert len(res.json()) == len(test_finishing_data)
    assert res.status_code == 200


def test_get_all_brands_empty(authorized_client):
    res = authorized_client.get('/brands/finishing')
    assert res.status_code == 404


def test_get_all_brands_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/brands/finishing')
    assert res.status_code == 403


def test_create_brand(authorized_client, test_finishing_data):
    data = {
        "name": "FIN5",
        "is_pre_injection": False,
        "is_post_injection": False,
        "is_bypass": False,
        "is_organic": False,
        "note": "string",
        "is_active": True,
        "id_brewing": 1
    }
    res = authorized_client.post('/brands/finishing', json=data)
    brand = val_brands_finishing.BrandFinishingOut(**res.json())
    assert isinstance(brand.id, int)
    assert brand.name == "FIN5"
    assert brand.is_pre_injection == False
    assert brand.is_post_injection == False
    assert brand.is_bypass == False
    assert brand.is_organic == False
    assert brand.note == "String"
    assert brand.is_active == True
    assert res.status_code == 201


def test_create_brand_unauthorized(authorized_client_permissions_0):
    data = {
        "name": "FIN5",
        "is_pre_injection": False,
        "is_post_injection": False,
        "is_bypass": False,
        "is_organic": False,
        "note": "string",
        "is_active": True,
        "id_brewing": 1
    }
    res = authorized_client_permissions_0.post('/brands/finishing', json=data)
    assert res.status_code == 403


def test_get_one_brand(authorized_client, test_finishing_data):
    res = authorized_client.get('/brands/finishing/1')
    brand = val_brands_finishing.BrandFinishingOut(**res.json())
    assert brand.id == 1
    assert res.status_code == 200


def test_get_one_brand_empty(authorized_client, test_finishing_data):
    res = authorized_client.get('/brands/finishing/50')
    assert res.status_code == 404


def test_get_one_brand_unauthorized(authorized_client_permissions_0):
    res = authorized_client_permissions_0.get('/brands/finishing/1')
    assert res.status_code == 403


def test_update_brand(authorized_client, test_finishing_data):
    data = {
        "name": "FIN6",
        "is_pre_injection": False,
        "is_post_injection": False,
        "is_bypass": False,
        "is_organic": False,
        "note": "string",
        "is_active": True,
        "id_brewing": 1
    }
    res = authorized_client.put('/brands/finishing/1', json=data)
    brand = val_brands_finishing.BrandFinishingOut(**res.json())
    assert brand.id == 1
    assert brand.name == "FIN6"
    assert brand.is_pre_injection == False
    assert brand.is_post_injection == False
    assert brand.is_bypass == False
    assert brand.is_organic == False
    assert brand.note == "String"
    assert brand.is_active == True
    assert res.status_code == 200


def test_update_brand_unauthorized(authorized_client_permissions_0):
    data = {
        "name": "FIN6",
        "is_pre_injection": False,
        "is_post_injection": False,
        "is_bypass": False,
        "is_organic": False,
        "note": "string",
        "is_active": True,
        "id_brewing": 1
    }
    res = authorized_client_permissions_0.put('/brands/finishing/1', json=data)
    assert res.status_code == 403


def test_delete_brand(admin_authorized_client, test_finishing_data):
    res = admin_authorized_client.delete('/brands/finishing/1')
    assert res.status_code == 205


def test_delete_brand_unauthorized(authorized_client):
    res = authorized_client.delete('/brands/finishing/1')
    assert res.status_code == 403


def test_update_brand_method_filters(authorized_client, test_finishing_data):
    methods_filters = {
        "methods_filters": {
            "pre": {
                "Schoene_Tank": {
                    "method": "test method",
                    "note": "string"
                },
                "Schoene_Release_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Filter": {
                    "method": "string",
                    "note": "string"
                },
                "Balance_Tanks": {
                    "method": "string",
                    "note": "string"
                },
                "Trap_Filter": {
                    "method": "string",
                    "note": "string"
                },
                "Filter_Beer_Supply_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Filter_Beer_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Filter_Control": {
                    "method": "string",
                    "note": "string"
                },
                "Brand_Changes": {
                    "method": "string",
                    "note": "string"
                },
                "Pre_Injection": [
                    {
                        "Ingredient_1": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_2": {
                            "method": "string",
                            "note": "string"
                        }
                    }
                ],
                "Post_Injection": [
                    {
                        "Ingredient_1": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_2": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_3": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_4": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_5": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_6": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_7": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_8": {
                            "method": "string",
                            "note": "string"
                        }
                    }
                ],
                "Beer_recovery": {
                    "method": "string",
                    "note": "string"
                }
            },
            "post": {
                "Schoene_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Release_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Filter": {
                    "method": "string",
                    "note": "string"
                },
                "Balance_Tanks": {
                    "method": "string",
                    "note": "string"
                },
                "Trap_Filter": {
                    "method": "string",
                    "note": "string"
                },
                "Filter_Beer_Supply_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Filter_Beer_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Filter_Control": {
                    "method": "string",
                    "note": "string"
                },
                "Brand_Changes": {
                    "method": "string",
                    "note": "string"
                },
                "Pre_Injection": [
                    {
                        "Ingredient_1": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_2": {
                            "method": "string",
                            "note": "string"
                        }
                    }
                ],
                "Post_Injection": [
                    {
                        "Ingredient_1": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_2": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_3": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_4": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_5": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_6": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_7": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_8": {
                            "method": "string",
                            "note": "string"
                        }
                    }
                ],
                "Beer_recovery": {
                    "method": "string",
                    "note": "string"
                }
            }
        }
    }
    res = authorized_client.put(
        '/brands/finishing/method/filters/1', json=methods_filters)
    brand = res.json()
    assert brand['methods_filters']['pre']['Schoene_Tank']['method'] == "Test Method"
    assert res.status_code == 200


def test_update_brand_method_filters_unauthorized(authorized_client_permissions_0):
    methods_filters = {
        "methods_filters": {
            "pre": {
                "Schoene_Tank": {
                    "method": "test method",
                    "note": "string"
                },
                "Schoene_Release_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Filter": {
                    "method": "string",
                    "note": "string"
                },
                "Balance_Tanks": {
                    "method": "string",
                    "note": "string"
                },
                "Trap_Filter": {
                    "method": "string",
                    "note": "string"
                },
                "Filter_Beer_Supply_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Filter_Beer_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Filter_Control": {
                    "method": "string",
                    "note": "string"
                },
                "Brand_Changes": {
                    "method": "string",
                    "note": "string"
                },
                "Pre_Injection": [
                    {
                        "Ingredient_1": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_2": {
                            "method": "string",
                            "note": "string"
                        }
                    }
                ],
                "Post_Injection": [
                    {
                        "Ingredient_1": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_2": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_3": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_4": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_5": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_6": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_7": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_8": {
                            "method": "string",
                            "note": "string"
                        }
                    }
                ],
                "Beer_recovery": {
                    "method": "string",
                    "note": "string"
                }
            },
            "post": {
                "Schoene_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Schoene_Release_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Filter": {
                    "method": "string",
                    "note": "string"
                },
                "Balance_Tanks": {
                    "method": "string",
                    "note": "string"
                },
                "Trap_Filter": {
                    "method": "string",
                    "note": "string"
                },
                "Filter_Beer_Supply_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Filter_Beer_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Filter_Control": {
                    "method": "string",
                    "note": "string"
                },
                "Brand_Changes": {
                    "method": "string",
                    "note": "string"
                },
                "Pre_Injection": [
                    {
                        "Ingredient_1": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_2": {
                            "method": "string",
                            "note": "string"
                        }
                    }
                ],
                "Post_Injection": [
                    {
                        "Ingredient_1": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_2": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_3": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_4": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_5": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_6": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_7": {
                            "method": "string",
                            "note": "string"
                        },
                        "Ingredient_8": {
                            "method": "string",
                            "note": "string"
                        }
                    }
                ],
                "Beer_recovery": {
                    "method": "string",
                    "note": "string"
                }
            }
        }
    }
    res = authorized_client_permissions_0.put(
        '/brands/finishing/method/filters/1', json=methods_filters)
    assert res.status_code == 403


def test_update_brand_method_releasing(authorized_client, test_finishing_data):
    methods_releasing = {
        "methods_releasing": {
            "pre": {
                "Filter_Beer_Tank": {
                    "method": "test method",
                    "note": "string"
                },
                "Release_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Package_Line": {
                    "method": "string",
                    "note": "string"
                },
                "Draught_Line": {
                    "method": "string",
                    "note": "string"
                },
                "Release_Control": {
                    "method": "string",
                    "note": "string"
                },
                "Beer_Recovery": {
                    "method": "string",
                    "note": "string"
                }
            },
            "post": {
                "Filter_Beer_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Release_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Package_Line": {
                    "method": "string",
                    "note": "string"
                },
                "Draught_Line": {
                    "method": "string",
                    "note": "string"
                },
                "Release_Control": {
                    "method": "string",
                    "note": "string"
                },
                "Beer_Recovery": {
                    "method": "string",
                    "note": "string"
                }
            }
        }
    }
    res = authorized_client.put(
        '/brands/finishing/method/releasing/1', json=methods_releasing)
    brand = res.json()
    assert brand['methods_releasing']['pre']['Filter_Beer_Tank']['method'] == "Test Method"
    assert res.status_code == 200


def test_update_brand_method_releasing_unauthorized(authorized_client_permissions_0):
    methods_releasing = {
        "methods_releasing": {
            "pre": {
                "Filter_Beer_Tank": {
                    "method": "test method",
                    "note": "string"
                },
                "Release_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Package_Line": {
                    "method": "string",
                    "note": "string"
                },
                "Draught_Line": {
                    "method": "string",
                    "note": "string"
                },
                "Release_Control": {
                    "method": "string",
                    "note": "string"
                },
                "Beer_Recovery": {
                    "method": "string",
                    "note": "string"
                }
            },
            "post": {
                "Filter_Beer_Tank": {
                    "method": "string",
                    "note": "string"
                },
                "Release_Bank": {
                    "method": "string",
                    "note": "string"
                },
                "Package_Line": {
                    "method": "string",
                    "note": "string"
                },
                "Draught_Line": {
                    "method": "string",
                    "note": "string"
                },
                "Release_Control": {
                    "method": "string",
                    "note": "string"
                },
                "Beer_Recovery": {
                    "method": "string",
                    "note": "string"
                }
            }
        }
    }
    res = authorized_client_permissions_0.put(
        '/brands/finishing/method/releasing/1', json=methods_releasing)
    assert res.status_code == 403
