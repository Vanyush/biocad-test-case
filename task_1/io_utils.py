from rdkit import Chem
import logging


def load_sdf(sdf_path):
    """Загрузка молекул из файла, отсев ошибочный записей"""

    # Создается объект, который позволяет последовательно загружать молекулы из файла SD, сохраняя исходную конфигурацию
    supplier = Chem.SDMolSupplier(sdf_path, removeHs=False) 
    
    molecules = []
    for i, mol in enumerate(supplier):
        # Отсев ошибочных записей с сообщением
        if mol is None:
            logging.warning(f"[LOAD] Не удалось прочитать молекулу №{i}")
            continue 
        molecules.append(mol)
    
    # Вывод информации о количестве загруженных молекул
    logging.info(f"[LOAD] Загружено {len(molecules)} молекул")
    return molecules


def get_molecule_name(mol, idx):
    """Получение названия молекулы"""

    # Проверка свойства "Molecule Name"
    if mol.HasProp("Molecule Name"):
        return mol.GetProp("Molecule Name")

    # Если свойство "Molecule Name" не существует, проверка свойства "_Name"
    elif mol.HasProp("_Name"):
        return mol.GetProp("_Name")

    # Если свойство "_Name" тоже не существует, возврат названия молекулы в формате "mol_{idx}"
    else:
        return f"mol_{idx}"
