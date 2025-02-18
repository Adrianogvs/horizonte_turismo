import logging

def setup_logger():
    """
    Configura o logger para registrar as ações do programa.
    O arquivo de log será salvo em 'app.log'.
    """
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.DEBUG)

    # Criando um manipulador de arquivo
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)

    # Criando um formatador e configurando o manipulador
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Adicionando o manipulador ao logger
    logger.addHandler(file_handler)

    return logger
