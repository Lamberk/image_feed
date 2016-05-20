# image_feed

- git clone https://github.com/Lamberk/image_feed.git
- virtualenv flask
- . flask/bin/activate
- pip install -r requirements.txt
- python db_create.py
- python db_migrate.py
- python fill_database.py
- python run.py

# API

* http://127.0.0.1:5000/api/get_image/sku/
* http://127.0.0.1:5000/api/get_image/random/
