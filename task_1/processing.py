import logging
import os
from rdkit import Chem
from openff.toolkit.topology import Molecule as OFFMolecule
from openff.toolkit.typing.engines.smirnoff import ForceField
import parmed as pmd


class LigandProcessor:
    """
    Класс для обработки малых молекул:
    - валидация структуры
    - конвертация в OpenFF формат
    - назначение частичных зарядов
    - параметризация
    - экспорт в формат GROMACS
    """
    def __init__(self, forcefield="openff_unconstrained-2.0.0.offxml"):
        # Загрузка "силового поля" OpenFF
        self.ff = ForceField(forcefield)
        logging.info(f"[INIT] ForceField loaded: {forcefield}")
    
    
    def validate_molecule(self, mol):
        """
        Проверка корректности молекулы:
        - санитаризация (RDKit)
        - наличие 3D-конформера
        """
        try:
            Chem.SanitizeMol(mol)
            conf = mol.GetConformer()
            return conf.Is3D()
        except Exception as e:
            logging.warning(f"[VALIDATION] Failed: {e}")
            return False
    
    
    def to_openff(self, mol):
        """
        Конвертация молекулы из RDKit в формат OpenFF
        """
        return OFFMolecule.from_rdkit(
            mol,
            allow_undefined_stereo=True # Допускаем неопределенную стереохимию
        )
    
    
    def parameterize(self, off_mol):
        topology = off_mol.to_topology()
        system = self.ff.create_openmm_system(
            topology, 
            charge_from_molecules=[off_mol] # Использовать заренее рассчитанные заряды
        )
        return topology, system
    
    
    def export_gromacs(self, topology, system, positions, output_prefix):
        """
        Экспорт параметризованной системы в формат GROMACS:
        - .gro (координаты)
        - .top (топология)
        """
        structure = pmd.openmm.load_topology(
            topology.to_openmm(),
            system,
            positions
        )
        
        # Сохранение файлов
        structure.save(f"{output_prefix}.gro")
        structure.save(f"{output_prefix}.top")
    
    def assign_charges(self, off_mol):
        """
        Назначение частичных зарядов.

        Используется метод Gasteiger (доступен без AmberTools),
        что обеспечивает переносимость пайплайна.
        """
        off_mol.assign_partial_charges("gasteiger")

    
    def process(self, mol, name, output_dir):
        """
        Полный цикл обработки одной молекулы:
        1. Валидация
        2. Конвертация в OpenFF
        3. Назначение зарядов
        4. Параметризация
        5. Экспорт в GROMACS
        """
        try:
            if not self.validate_molecule(mol):
                logging.warning(f"[SKIP] Invalid molecule: {name}")
                return False
            
            off_mol = self.to_openff(mol)
            self.assign_charges(off_mol)
            topology, system = self.parameterize(off_mol)
            
            positions = off_mol.conformers[0]
            
            mol_dir = os.path.join(output_dir, name)
            os.makedirs(mol_dir, exist_ok=True)
            
            output_prefix = os.path.join(mol_dir, name)
            
            self.export_gromacs(
                topology,
                system,
                positions,
                output_prefix
            )
            
            logging.info(f"[SUCCESS] {name}")
            return True
        
        except Exception as e:
            logging.error(f"[ERROR] {name}: {e}")
            return False