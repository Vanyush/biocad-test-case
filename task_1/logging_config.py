import logging

def setup_logging(log_file: str = "task_1/pipeline.log"):
    """
    Настройка системы логирования.

    :param log_file: Путь к файлу для записи логов. По умолчанию используется 'pipeline.log'.
    """

    # Настройка базовых параметров логирования
    logging.basicConfig(
        level=logging.INFO,                               # Уровень логирования
        format="%(asctime)s [%(levelname)s] %(message)s", # Формат сообщений лога
        handlers=[
            logging.FileHandler(log_file),                # Обработчик для записи в файл
            logging.StreamHandler()                       # Обработчик для вывода в консоль
        ]
    )