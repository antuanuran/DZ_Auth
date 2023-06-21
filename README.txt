1/ Создание БД в cmd:   	createdb -U postgres auth_token
				пароль: postgres
2/ Подкл. библиотек в cmd: 	pip install -r requirements.txt


3/ Миграция в cmd: 		python manage.py migrate

4/ Создание Юзеров:    		python manage.py createsuperuser
				username:  admin
				email adress: -
				password: admin

5/ Запросы через HTTP: 		requests-examples.http

6/ Запуск программы:		python manage.py runserver
