import custom_logger
import dotenv
import server

if __name__ == '__main__':
    custom_logger.init_logger()
    dotenv.load_dotenv()
    server.serve()
