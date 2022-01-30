
description = """
#### Bud Brewing API Brews Up Some Awesome Stuff 》 
## (͡• ͜ʖ ͡•) 🍺🍺🍺 
## Authentication
Options:
* **Login**

## Users 》
#### Options:
* Retrieve All Brewers
* **Perm 6** Create A Brewer
* Get A Single Brewer
* **Perm 6** Update A Brewer
* **Perm 5** Reset Brewer Password
* Change A Reset Password
* **Admin** Delete A Brewer

## Jobs 》
#### Options:
* **Perm 6** Add Skill To Brewer
* **Perm 6** Update Brewer SKAP
* **Perm 6** Delete A Skill From Brewer
* Retrieve A Skill With All Brewers
* Retrieve A Brewer And Their Skills
* Retrieve All Skills
* **Perm 6** Create Skill
* Retrieve Single Skill
* **Perm 6** Update A Skill
* **Admin** Delete A Skill

## Suppliers 》
#### Options:
* Retrieve All Suppliers
* **Perm 3** Create A Supplier
* Get A Single Supplier
* **Perm 3** Update A Suppliers
* **Admin** Delete A Suppliers

## Commodities 》
#### Options:
* Retrieve All Commodities (Search By: active, type, sap)
* **Perm 3** Create A Commodity
* Get A Single Commodity
* **Perm 3** Update A Commodities
* **Admin** Delete A Commodities

## Brands 》
#### Options Brewing Brands:
* Get Brands (Search By: active)
* **Perm 6** Create Brand
* Get Brand
* **Perm 6** Update Brand
* **Perm 6** Update Brand Method ACX
* **Perm 6** Update Brand Method CSX
* Get Brand Methods
* **Admin** Delete Brand

#### Options Finishing Brands:
* Get Brands (Search By: active)
* **Perm 6** Create Brand
* Get Brand
* **Perm 6** Update Brand
* **Perm 6** Update Brand Method ACX
* **Perm 6** Update Brand Method CSX
* Get Brand Methods
* **Admin** Delete Brand

#### Options Packaging Brands:
* Get Brands (Search By: active)
* **Perm 6** Create Brand
* Get Brand
* **Perm 6** Update Brand
* **Admin** Delete Brand

## Options Material Inventory 》
* **Perm 3** Create Entry To Inventory
* **Perm 3** Delete Entry From Inventory
* Retrieve Summed Inventory By UUID
* Retrieve Complete Inventory By UUID
* Retrieve Inventory Dates

## Options Hop Inventory 》
* **Perm 1** Create Last Brew Entry To Inventory
* **Perm 1** Delete Last Brew Entry From Inventory (Cascades To Delete Adjacent Hop Inventory)
* **Perm 1** Create Entry To Inventory
* **Perm 1** Delete Entry From Inventory
* Retrieve Summed Inventory By UUID
* Retrieve Complete Inventory By UUID
* Retrieve Inventory Dates

## Options Combined Inventory 》
* Get Combined Hop And Material Inventories

## Options Manpower 》
* **Perm 5** Create Individual Entry
* Get Individual Entries
* **Perm 5** Delete Individual Entry
* **Perm 5** Create Group Entry
* Get Group Entries
* **Perm 5** Delete Group Entry

## Schemas 》
* **Create**, **Update** and **In** schemas show the structure and data required for input
* **Out** schemas show the structure and data provided in the output
* **Include** schemas show the structure and data provided when appended to other outputs


"""

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Authentication Endpoints",
        "externalDocs": {
            "description": "External Docs",
            "url": "https://shorturl.at/cmwBS",
        },
    },
    {
        "name": "Users",
        "description": "Users Endpoints",
        "externalDocs": {
            "description": "External Docs",
            "url": "https://shorturl.at/bzJ15",
        },
    },
    {
        "name": "Jobs",
        "description": "Skill Endpoints",
        "externalDocs": {
            "description": "External Docs",
            "url": "https://shorturl.at/doOUY",
        },
    },
    {
        "name": "Suppliers",
        "description": "Supplier Endpoints",
        "externalDocs": {
            "description": "External Docs",
            "url": "https://shorturl.at/oHU29",
        },
    },
    {
        "name": "Commodities",
        "description": "Commodity Endpoints",
        "externalDocs": {
            "description": "External Docs",
            "url": "https://shorturl.at/ahyK1",
        },
    },
    {
        "name": "Brands",
        "description": "Brand Endpoints",
        "externalDocs": {
            "description": "External Docs",
            "url": "https://shorturl.at/zGPQR",
        },
    },
    {
        "name": "Material Inventory",
        "description": "Material Inventory Endpoints",
        "externalDocs": {
            "description": "External Docs",
            "url": "https://shorturl.at/zGPQR",
        },
    },
    {
        "name": "Hop Inventory",
        "description": "Hop Inventory Endpoints",
        "externalDocs": {
            "description": "External Docs",
            "url": "https://shorturl.at/zGPQR",
        },
    },
    {
        "name": "Combined Inventory",
        "description": "Combined Inventory Endpoints",
        "externalDocs": {
            "description": "External Docs",
            "url": "https://shorturl.at/zGPQR",
        },
    },
    {
        "name": "Manpower",
        "description": "Manpower Endpoints",
        "externalDocs": {
            "description": "External Docs",
            "url": "https://shorturl.at/zGPQR",
        },
    },
]
