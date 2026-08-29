## Տեղադրում և Շահագործում
---

### Տեղադրում

```bash
## PIP

# Ռեպոզիտորիայի կլոնավորում։ 
git clone https://github.com/stpatriarch/json2sql.git && cd json2sql

# վիրտուալ միջակայքի ստեղծում և ակտիվացում
python3 -m venv venv && source venv/bin/activate

# տեղադրում։
pip install .

## UV

# Ռեպոզիտորիայի կլոնավորում։ 
git clone https://github.com/stpatriarch/json2sql.git && cd json2sql

# տեղադրում։
uv sync
```

### Շահագործում

```bash
# input_file.json -> json ֆայլի ուղին,  sql_table_name -> sql աղյուակի անունը։
json2sql -i input_file.json -t sql_table_name
```
