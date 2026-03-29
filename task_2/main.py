import os
import logging

from io_utils import load_sdf, load_smi, get_molecule_name
from processing import VinaProcessor
from logging_config import setup_logging


def main(input_path, output_dir):
    setup_logging()

    # Загрузка молекул
    if input_path.endswith(".sdf"):
        mols = load_sdf(input_path)
    elif input_path.endswith(".smi"):
        mols = load_smi(input_path)
    else:
        raise ValueError("Неподдерживаемый формат")
    logging.info(f"[LOAD] Загружено {len(mols)} молекул")
    processor = VinaProcessor()

    # Создание output директории
    os.makedirs(output_dir, exist_ok=True)

    # Счетчики
    success = 0
    failed = 0

    # Итерация по всем молекулам
    for i, mol in enumerate(mols):
        # Получение названия молекулы
        name = get_molecule_name(mol, i)

        logging.info(f"[PROCESS] {name}")

        # Основной пайплайн обработки молекулы
        result = processor.process(mol, name, output_dir)

        # Подсчет удачных/неудачных обработок
        if result:
            success += 1
        else:
            failed += 1

    logging.info(f"[DONE] Успешно: {success}, Пропущено: {failed}")


if __name__ == "__main__":
    main("task_2/input/example.sdf", "task_2/output/")