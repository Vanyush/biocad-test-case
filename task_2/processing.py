import os
import logging
from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation


class VinaProcessor:
    """
    Класс для обработки малых молекул:
    - подготовка молекулы для дальнейшего анализа
    - конвертация в формат .pdbqt
    """
    def prepare_molecule(self, mol, name):
        """
        Подготовка молекулы:
        - добавление атомов водорода
        - генерация 3D-координат (если их нет)
        - оптимизация геометрии
        """
        logging.info(f"[PREP] Подготовка молекулы: {name}")

        # Добавление водородов
        mol = Chem.AddHs(mol)
        logging.info(f"[PREP] Добавлены водороды: {name}")

        # Генерация 3D
        if mol.GetNumConformers() == 0:
            logging.info(f"[PREP] Генерация 3D координат: {name}")
            AllChem.EmbedMolecule(mol, AllChem.ETKDG())

        # Оптимизация
        logging.info(f"[PREP] Оптимизация геометрии: {name}")
        AllChem.UFFOptimizeMolecule(mol)

        return mol

    def convert_to_pdbqt(self, mol, name, output_dir):
        """
        Конвертация молекулы в формат PDBQT с использованием Meeko
        """
        logging.info(f"[CONVERT] Конвертация в PDBQT: {name}")

        # Обьект подготовки молекулы
        preparator = MoleculePreparation()
        preparator.prepare(mol)

        pdbqt_str = preparator.write_pdbqt_string()

        output_path = os.path.join(output_dir, f"{name}.pdbqt")

        # Пропуск существующих файлов
        if os.path.exists(output_path):
            logging.warning(f"[SKIP] Файл уже существует: {output_path}")
            return False

        with open(output_path, "w") as f:
            f.write(pdbqt_str)

        logging.info(f"[SAVE] Сохранён файл: {output_path}")
        return True

    def process(self, mol, name, output_dir):
        """
        Полный пайплайн обработки одной молекулы:
        1. Подготовка (H, 3D, оптимизация)
        2. Конвертация в PDBQT
        """
        try:
            mol = self.prepare_molecule(mol, name)

            result = self.convert_to_pdbqt(mol, name, output_dir)

            if result:
                logging.info(f"[SUCCESS] {name}")
                return True
            else:
                return False

        except Exception as e:
            logging.error(f"[ERROR] {name}: {e}")
            return False