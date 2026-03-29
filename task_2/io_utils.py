from rdkit import Chem
import logging


def load_sdf(sdf_path):
    """Загрузка молекул из SDF-файла, отсев ошибочный записей"""

    # Создается объект, который позволяет последовательно загружать молекулы из файла SD, сохраняя исходную конфигурацию
    supplier = Chem.SDMolSupplier(sdf_path, removeHs=False) 
    
    molecules = []
    for i, mol in enumerate(supplier):
        # Отсев ошибочных записей с сообщением
        if mol is None:
            logging.warning(f"[LOAD] Не удалось прочитать молекулу №{i}")
            continue 
        molecules.append(mol)
    
    return molecules


def load_smi(path):
    """Загрузка молекул из SMI-файла"""
    molecules = []

    with open(path) as f:
        for i, line in enumerate(f):

            # пропуск пустых строк
            if not line.strip():
                continue

            parts = line.strip().split()

            # пропуск заголовка
            if i == 0 and parts[0].lower() == "smiles":
                continue

            if len(parts) < 1:
                logging.warning(f"[LOAD] Не удалось прочитать строку #{i}")
                continue

            smi = parts[0]
            name = parts[1] if len(parts) > 1 else f"mol_{i}"

            molecule = Chem.MolFromSmiles(smi)

            if molecule is None:
                logging.warning(f"[LOAD] Не удалось прочитать молекулу: {smi}")
                continue

            molecule.SetProp("_Name", name)
            molecules.append(molecule)
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