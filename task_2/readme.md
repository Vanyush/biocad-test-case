# Задание 2. Подготовка лигандов для докинга в Autodock Vina
## Структура проекта

- [main.py](https://github.com/Vanyush/biocad-test-case/blob/main/task_2/main.py) - основной срипт для запуска пайплайна 
- [processing.py](https://github.com/Vanyush/biocad-test-case/blob/main/task_2/processing.py) - функции обработки молекул
- [io_utils.py](https://github.com/Vanyush/biocad-test-case/blob/main/task_2/io_utils.py) - набор функций для чтения исходных данных
- [logging_config.py](https://github.com/Vanyush/biocad-test-case/blob/main/task_2/logging_config.py) - конфигурация логирования
- [input](https://github.com/Vanyush/biocad-test-case/tree/main/task_2/input) - папка со входными данными из [репозитория с заданием](https://github.com/biocad/chemnext-trainee-test-case/blob/main/vina_data):
    - файл [example.sdf](https://github.com/Vanyush/biocad-test-case/blob/main/task_2/input/example.sdf)
    - файл [example.smi](https://github.com/Vanyush/biocad-test-case/blob/main/task_2/input/example.smi)
- [output](https://github.com/Vanyush/biocad-test-case/tree/main/task_2/output) - папка с выходными данными. Выходные данные содержат .pdbqt файлы, чьи имена соответствуют названиям молекул
- [pipeline.log](https://github.com/Vanyush/biocad-test-case/blob/main/task_2/pipeline.log) - файл логирования

## Установка зависимостей

Для установки необходимых пакетов и зависимостей был использован пакетный менеджер conda. Следующим скриптом было создано и запущено окружение, а также установлены необходимые пакеты:
``` bash
conda create -n vina_env python=3.11
conda activate vina_env
conda install -c conda-forge rdkit meeko
```

## Описание и результаты работы
Скрипт выполняет конвертацию малых молекул из форматов SDF и SMILES в формат PDBQT для использования в AutoDock Vina.

Основные этапы:
1. загрузка молекул из SDF или SMI файла
2. добавление атомов водорода
3. генерация 3D координат (если отсутствуют)
4. оптимизация геометрии (UFF)
5. конвертация в формат PDBQT с использованием библиотеки Meeko
6. сохранение файлов

В результате работы пайплайна было создано 16 файлов для молекул. Было пропущено 14 молекул, так как библотека RDKit не смогла обработать геометрию молекул. 