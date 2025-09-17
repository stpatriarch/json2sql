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
[
    {"id": 1, "name": "Coffee"},
    {"id": 2, "name": "Tea"}
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
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "active": true
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "age": 25,
    "active": false
  },
  {
    "id": 3,
    "name": "Bob Johnson",
    "email": "bob@example.com",
    "age": 35,
    "active": true
  }
]
```

###### output.db

id | name | email | age | active
--- | --- | --- | --- | ---
1 | John Doe | john@example.com | 30 | true
2 | Jane Smith | jane@example.com | 25 | false
3 | Bob Johnson | bob@example.com | 35 | true

---

###### input.json (in progress now...)

```json
[{
  "order_id": 123,
  "items": [
    {"name": "Cola", "qty": 2},
    {"name": "Chips", "qty": 1}
  ]},
  {"order_id": 456,
  "items": [
    {"name": "Pekro", "qty": 2},
    {"name": "Tuna", "qty": 1}
  ]}
]

```

###### output.db

order_id | items_name | items_qty
--- | --- | ---
123 | Cola, Chips | 2, 1
456 | Pekro, Tuna | 2, 1

---
