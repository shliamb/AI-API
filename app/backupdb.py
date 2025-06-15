from keys import USER_DB, PASSWORD_DB, DB_NAME
from config import LOG_CONFIG_DB, HOST, BACKUP_DB, setup_logger
import subprocess
import datetime
logger_db = setup_logger('db', LOG_CONFIG_DB)


def backup_db():
    
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f'{DB_NAME}_backup_{current_datetime}.sql'

    # Формирование команды для создания резервной копии с помощью pg_dump
    pg_dump_command = f'PGPASSWORD={PASSWORD_DB} pg_dump -h {HOST} -p 5432 -U {USER_DB} -d {DB_NAME} -F c -f {BACKUP_DB}{backup_filename}' # В бинарный формат
                                                        

    try:
        subprocess.run(pg_dump_command, shell=True) # Выполнение команды через subprocess
        logger_db.info("Backup Data Base is Completed.")
        return True

    except subprocess.CalledProcessError as e:
        logger_db.error(f"Error when creating a backup: {e}")
        return False


#
# У меня чет на Linux pg_dump не обновляется выше 15.5, потому я поставил в docker-compose.yml
# версию 15.5 PostgreSQL, если на сервере будет выше, то в файле просто поставить Last img Postgres.
#