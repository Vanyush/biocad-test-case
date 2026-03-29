# Задание 1. Параметризация малой молекулы полем OpenFF
## Структура проекта

- [main.py](https://github.com/Vanyush/biocad-test-case/blob/main/task_1/main.py) - основной срипт для запуска пайплайна 
- [processing.py](https://github.com/Vanyush/biocad-test-case/blob/main/task_1/processing.py) - функции обработки молекул
- [io_utils.py](https://github.com/Vanyush/biocad-test-case/blob/main/task_1/io_utils.py) - набор функций для чтения исходных данных
- [logging_config.py](https://github.com/Vanyush/biocad-test-case/blob/main/task_1/logging_config.py) - конфигурация логирования
- [input](https://github.com/Vanyush/biocad-test-case/tree/main/task_1/input) - папка со входными данными (файл [example.sdf](https://github.com/Vanyush/biocad-test-case/blob/main/task_1/input/example.sdf) из [репозитория с заданием](https://github.com/biocad/chemnext-trainee-test-case/tree/main))
- [output](https://github.com/Vanyush/biocad-test-case/tree/main/task_1/output) - папка с выходными данными. Выходные данные содержат папки, чьи имена соответствуют названиям молекул, в папках:   
    - Файл со структурой лиганда
    - Файл с топологией Gromacs
- [pipeline.log](https://github.com/Vanyush/biocad-test-case/blob/main/task_1/pipeline.log) - файл логирования

## Установка зависимостей

Для установки необходимых пакетов и зависимостей был использован пакетный менеджер conda. Следующим скриптом было создано и запущено окружение, а также установлены необходимые пакеты:
``` bash
conda create -n openff_env python=3.11
conda activate openff_env
conda install -c conda-forge -c bioconda rdkit openff-toolkit parmed openmm
```

## Описание и результаты работы

Скрипт выполняет параметризацию малых молекул из SDF-файла с использованием OpenFF и экспортирует результаты в формат GROMACS (.gro и .top).

Основные этапы:
1. загрузка молекул из SDF 
2. валидация структуры
3. генерация частичных зарядов
4. параметризация полем OpenFF
5. экспорт в формат GROMACS

Для генерации частичных зарядов использовался метод gastieger, так как метод установленный по умолчанию (am1bcc) оказался неработоспособным на устройстве, выполнявшем вычисления.

В результате работы пайплайна была получена выходная структура, описанная в разделе [структура проекта](#структура-проекта). Было создано 52 набора данных для каждой молекулы. Названия двух молекул из входного файла совпадали с названиями существующих и были пропущены, что отражено в логах. 
