# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
venv\Scripts\activate

# 3. Install project dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 5. Run the development server
python manage.py runserver

# admin username and password:
* admin
* admin123

# user name : 
roy1
# password:
admin@roy

