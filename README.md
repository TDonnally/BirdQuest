# BirdQuest

## Environment Setup

Follow these steps to set up your development environment for BirdQuest.

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root or replace environment variables in `settings.py` directly.

#### Database Configuration

Set your `DATABASE_URL` or connect your local PostgreSQL database with the following configuration in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'BirdQuest',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### Secret Key

Generate a secret key and set it in your `.env` file:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Add the generated key to your `.env` file:

```
SECRET_KEY=your_generated_secret_key
```

#### Debug Mode and Allowed Hosts

For development, set the following in your `.env` file:

```
DEBUG=True
ALLOWED_HOSTS=127.0.0.1
```

### 3. Database Migration

Run the following commands to create and apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run Tests

Ensure all tests pass by running:

```bash
python manage.py test
```

### 5. Start the Development Server

Launch the local development server:

```bash
python manage.py runserver
```

Your BirdQuest application should now be running at `http://127.0.0.1:8000/`.

