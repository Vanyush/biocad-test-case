import os
import logging

from io_utils import load_sdf, get_molecule_name
from processing import LigandProcessor
from logging_config import setup_logging


def main(sdf_path, output_dir):
    # Инициализация логирования
    setup_logging()
    
    logging.info("[START] Пайплайн запущен")
    
    # Загрузка малекулы из SDF файла
    mols = load_sdf(sdf_path)
    processor = LigandProcessor()
    
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
    
    logging.info(f"[DONE] Успешно: {success}, Провалено: {failed}")


if __name__ == "__main__":
    sdf_path = "task_1/input/example.sdf"
    output_dir = "task_1/output"
    
    os.makedirs(output_dir, exist_ok=True)
    main(sdf_path, output_dir)