from keys import USER_DB, PASSWORD_DB, DB_NAME
import subprocess
import datetime
import logging

# Параметры подключения к базе данных PostgreSQL
backup_path = "./backup_db/"

def backup_db():
    
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f'{DB_NAME}_backup_{current_datetime}.sql'

    # Формирование команды для создания резервной копии с помощью pg_dump
    pg_dump_command = f'PGPASSWORD={PASSWORD_DB} pg_dump -h postgres -p 5432 -U {USER_DB} -d {DB_NAME} -F c -f {backup_path}{backup_filename}' # В бинарный формат
                                                            # postgres localhost

    try:
        subprocess.run(pg_dump_command, shell=True) # Выполнение команды через subprocess
        logging.info("Backup Data Base is Completed.")
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"Error when creating a backup: {e}")
        return False


#
# У меня чет на Linux pg_dump не обновляется выше 15.5, потому я поставил в docker-compose.yml
# версию 15.5 PostgreSQL, если на сервере будет выше, то в файле просто поставить Last img Postgres.
#