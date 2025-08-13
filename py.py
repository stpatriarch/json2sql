import json

def load(filename: str)-> dict:
	
	with open(f"{filename}", 'r', encoding="utf-8") as file:
		
		data = json.load(file)
	return data
	

		 
		 
def detect_json_structure(js):
    """
    Определяет, с чем мы имеем дело: list[dict],
     dict[str, list[dict]], dict[str, scalar], и т.д.
    """
    if isinstance(js, list):
        if all(isinstance(item, dict) for item in js):
            return 'list_of_dicts'
    elif isinstance(js, dict):
        if all(isinstance(v, list) and all(isinstance(i, dict) for i in v) for v in js.values()):
            return 'dict_of_lists_of_dicts'
        elif all(not isinstance(v, (list, dict)) for v in js.values()):
            return 'flat_dict'
    raise ValueError("Неизвестная структура JSON")
    
    
    
    
def flatten_dict(d, parent_key='', sep='_'):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items
    
# struct_1-> dict

{'name': 'Alice', 'age': 30, 'is_admin': False} #ok flaten_dict

# struct_2-> list

[{'id': 1, 'name': 'Coffee'}, {'id': 2, 'name': 'Tea'}] #ok

# struct_3-> dict

{'order_id': 123, 
'items': [{'name': 'Cola', 'qty': 2}, {'name': 'Chips', 'qty': 1}]} #ok


# struct_4-> list 

['apple', 'banana', 'cherry'] #x

# struct_5-> dict

{'sensor1': {'temp': 21, 'hum': 40}, 
'sensor2': {'temp': 22, 'hum': 38}} #ok my type

# struct_6-> dict

{'user': {'id': 1, 'name': 'Narek', 'roles': ['admin', 'editor'], 
'settings': {'theme': 'dark', 'notifications': True}}} #пиздец

dd = {'sensor1': {'temp': 21, 'hum': 40}, 
'sensor2': {'temp': 22, 'hum': {'temp': 22, 'hum': 38}}} 

# def define_js_struct(js: dict) -> dict:
	
# 	if isinstance(js, dict):
# 		if any(isinstance(val, dict) for val in js.values()):
# 			print('dict_of_dicts')		
# 	if define_js_struct(val for vla in js.values()):
# 				print('dict_of_dicts_of_dicts')

# 	else:
# 		print('None_w')
