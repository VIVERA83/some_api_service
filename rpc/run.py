import logging
from source.core.main import run_server
from source.utils.utils import before_execution

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting RPC server...")
    # неоднократная попытка запуска на случай если с первого раза не запустится, из-за незапущенного rabbitmq
    before_execution()(run_server)()
