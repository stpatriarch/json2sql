###### input.json

```json
{
    "4850001006466": [
        {
            "drink_name": "Արարատ 5 տարեկան (1L)",
            "bottle_weight": 624,
            "difference": 0.91,
            "type": "drink"
        }
    ],
    "485000100646600": [
        {
            "drink_name": "Արարատ 5 տարեկան (0.7L)",
            "bottle_weight": null,
            "difference": 0.94,
            "type": "drink"
        }
    ],
```

###### output.db

id | drink_name | bottle_weight | difference | type
--- | --- | --- | --- | --- | 
4850001006466 | Արարատ 5 տարեկան (1L) | 624 | 0.91 | drink
485000100646600 | Արարատ 5 տարեկան (0.7L) | null | 0.94 | drink

---

###### input.json

```json
{
    "name": "Alice", 
    "age": 30, 
    "is_admin": false
    }
```

###### output.db

name | age | is_admin
--- | --- | ---
Alice | 30 | 624

---

###### input.json

```json
[
    {"id": 1, 
    "name": "Coffee"},
    {"id": 2, 
    "name": "Tea"}
] 
```

###### output.db

id | name
--- | ---
1 | Coffee
2 | Tea

---

###### input.json

```json
{
"sensor1": {"temp": 21, "hum": 40}, 
"sensor2": {"temp": 22, "hum": 38}
}
```

###### output.db

id | temp | hum
--- | --- | ---
sensor1 | 21 | 40
sensor2 | 22 | 38

---

###### input.json

```json
{

"user": {
    "id": 1, 
    "name": "Narek", 
    "roles": ["admin", "editor"], 
    "settings": {
        "theme": "dark", 
        "notifications": true}}

}
```

###### output.db

user_id | user_name | user_roles | user_settings_theme | user_settings_notifications
--- | --- | --- | --- | ---
1 | patrick | admin, editor | dark | true

---

###### input.json

```json
{
  "order_id": 123,
  "items": [
    {"name": "Cola", "qty": 2},
    {"name": "Chips", "qty": 1}
  ]
}
```

###### output.db

order_id | name | qty
--- | --- | ---
123 | cola | 2
123 | chips | 1

---
