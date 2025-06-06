from keys import USER_DB, PASSWORD_DB, DB_NAME
import subprocess
import logging



def restore_db(file_path):
                                                            # postgres  localhost
    terminate_command = f'PGPASSWORD={PASSWORD_DB} psql -h postgres -p 5432 -U {USER_DB} -d {DB_NAME} -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname=\'{DB_NAME}\';"'

    clear_command = f'PGPASSWORD={PASSWORD_DB} psql -h postgres -p 5432 -U {USER_DB} -d {DB_NAME} -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"'

    pg_restore_command = f'PGPASSWORD={PASSWORD_DB} pg_restore -h postgres -p 5432 -U {USER_DB} -d {DB_NAME} {file_path}'
    
    try:
        subprocess.run(terminate_command, shell=True) # Формирование команды для завершения активных сеансов

        subprocess.run(clear_command, shell=True) # Формирование команды для удаления базы данных

        subprocess.run(pg_restore_command, shell=True) # Восстановления базы данных из резервной копии с помощью pg_restore, выполнение команды через subprocess
        
        logging.info("Database restore completed successfully.")
        return True


    except Exception as e:
        logging.error(f"An error occurred restore_db : {e}")
        return False


#
# Очищает имеющуюся базу и восстанавливает из копии находящейся на сервере по адресу переданному по адресу и имени файла - file_path
# У меня чет на Linux pg_dump не обновляется выше 15.5, потому я поставил в docker-compose.yml
# версию 15.5 PostgreSQL, если на сервере будет выше, то в файле просто поставить Last img Postgres.
#