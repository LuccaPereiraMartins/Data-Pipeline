
'''
Mapping dictionary can come from a .csv, .json, manually assigned etc.
Include all the columns you'd expect to see and their desired datatypes
Consider also adding a format key to further map each column to desired format
'''

mapping_dict = {
    'nt_description':{
        'name': 'ticker',
        'data_type': 'str'
    },
    'nt_price':{
        'name': 'price',
        'data_type': 'float'
    },
    'nt_exchange_name':{
        'name': 'exchange_name',
        'data_type': 'str'
    },
    'nt_date':{
        'name': 'date',
        'data_type': 'str'
    },
}