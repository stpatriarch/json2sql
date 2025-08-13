import argparse
import sys
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Пример скрипта с ключами для работы с файлами и библиотеками.")
    
    # Входной и выходной файл
    parser.add_argument('--input', '-i', required=True, help='Путь к входному файлу (например, data.xlsx)')
    parser.add_argument('--output', '-o', required=True, help='Путь к выходному файлу (например, result.csv)')
    
    # Выбор библиотеки
    parser.add_argument('--lib', choices=['openpyxl', 'csv'], default='csv', help='Выбор библиотеки для обработки файла')
    
    # Флаг перезаписи
    parser.add_argument('--overwrite', action='store_true', help='Перезаписать выходной файл, если он уже существует')

    return parser.parse_args()

def main():
    args = parse_args()

    if os.path.exists(args.output) and not args.overwrite:
        print(f"Файл {args.output} уже существует. Используй --overwrite, чтобы перезаписать.")
        sys.exit(1)

    print(f"Обработка файла {args.input} с помощью {args.lib}...")
    print(f"Результат будет сохранён в {args.output}")

    # # Пример использования библиотеки
    # if args.lib == 'csv':
    #     import csv
    #     # ... логика работы с CSV
    # elif args.lib == 'openpyxl':
    #     import openpyxl
    #     # ... логика работы с Excel

if __name__ == "__main__":
    main()
