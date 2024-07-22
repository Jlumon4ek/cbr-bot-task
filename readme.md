# Перед запуском
Для запуска создай папку files в папке app. В папке files создайте папку envs. В envs создайте .env. В .env добавьте строку TOKEN = <токен вашего бота>. Путь должен выглядить так your-path/cbr-bot-task/app/files/envs/.env

# Запуск проекта:
## Без docker-а:
  ### Перейдем в папку с проектом
    cd app 

  ### Установка зависимостей
    pip install -r requirements/requirements.txt 
 
  ### Запуск бота
  
    python bot.py 

## Через docker:
    docker-compose up --build -d 


