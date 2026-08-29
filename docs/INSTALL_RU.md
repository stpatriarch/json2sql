## Установка и Использование

---

### Установка

```sh
## PIP 

# Клонирование репозитории.
git clone https://github.com/stpatriarch/json2sql.git && cd json2sql

# Создание виртуальной окружения и активация.
python3 -m venv venv && source venv/bin/activate

# Установка.
pip install .

## UV

# Клонирование репозитории.
git clone https://github.com/stpatriarch/json2sql.git && cd json2sql

# Установка.
uv sync
```

### Использование

```bash
# input_file.json ->  путь json файла  sql_table_name -> имя sql таблицы.
json2sql -i input_file.json -t sql_table_name
```
