import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Default directories
DEFAULT_DATA_DIR = os.path.join(BASE_DIR, 'data')
DEFAULT_LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Default settings for the tool
TOOL_SETTINGS = {
    'default_data_dir': DEFAULT_DATA_DIR,
    'default_logs_dir': DEFAULT_LOGS_DIR,
}

# API configurations
API_URL = 'https://api.example.com'
API_TOKEN = os.getenv('API_TOKEN', 'default_token')

# Database configurations
DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Django settings encapsulated in a class
class DjangoSettings:
    def __init__(self):
        self.settings = {
            'INSTALLED_APPS': [
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                'rest_framework',
                'channels',
                'django_celery_beat',
                'django_celery_results',
            ],
            'MIDDLEWARE': [
                'django.middleware.security.SecurityMiddleware',
                'whitenoise.middleware.WhiteNoiseMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.middleware.clickjacking.XFrameOptionsMiddleware',
            ],
            'STATICFILES_STORAGE': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
            'CELERY_BROKER_URL': 'redis://localhost:6379/0',
            'CELERY_RESULT_BACKEND': 'django-db',
        }

    def get_settings(self):
        return self.settings

    def add_app(self, app_name):
        self.settings['INSTALLED_APPS'].append(app_name)

    def add_middleware(self, middleware_name):
        self.settings['MIDDLEWARE'].append(middleware_name)

    def update_staticfiles_storage(self, storage_setting):
        self.settings['STATICFILES_STORAGE'] = storage_setting

    def update_celery_settings(self, broker_url, result_backend):
        self.settings['CELERY_BROKER_URL'] = broker_url
        self.settings['CELERY_RESULT_BACKEND'] = result_backend

    def save_settings_to_file(self, project_name):
        settings_path = os.path.join(BASE_DIR, project_name, project_name, 'settings.py')
        with open(settings_path, 'a') as settings_file:
            settings_file.write("\n# Additional settings for Django\n")
            for key, value in self.settings.items():
                if isinstance(value, list):
                    settings_file.write(f"{key} += {value}\n")
                else:
                    settings_file.write(f"{key} = '{value}'\n")
        print(f"Settings configured for Django project '{project_name}'.")
        


# Example usage of tool settings
if __name__ == "__main__":
    print(f"Default data directory: {TOOL_SETTINGS['default_data_dir']}")
    print(f"API URL: {API_URL}")
    print(f"Database settings: {DATABASE['default']}")
