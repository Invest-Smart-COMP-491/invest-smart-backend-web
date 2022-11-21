# invest-smart-backend




versions and libraries: requirements.txt

to start django: python manage.py runserver


PostGreDB
database: investsmart
user:postgres
password:0

<br/><br/>
**Redis:** <br/>
https://redis.io/docs/getting-started/installation/ <br/>

curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg <br/>
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list <br/>

sudo apt-get update <br/>
sudo apt-get install redis <br/>

to run: redis-server


**Celery:** <br/>

**Windows:** <br/>
python -m celery -A investsmart worker -l info -P gevent <br/>
python -m celery -A investsmart beat --loglevel=info <br/>
<br/>
Clear Task Queue: <br/>
python -m celery -A investsmart purge <br/>

**Linux:** <br/>
pkill -f "celery worker" <br/>
celery -A simpletask worker -l info --logfile=celery.log <br/>
celery -A simpletask beat -l info --logfile=celery.beat.log <br/>

