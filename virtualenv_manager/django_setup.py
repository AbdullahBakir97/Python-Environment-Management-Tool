import os
import subprocess

class DjangoSetup:
    @staticmethod
    def create_django_project(project_name, env_path):
        env_bin = os.path.join(env_path, 'Scripts' if os.name == 'nt' else 'bin')
        django_admin = os.path.join(env_bin, 'django-admin.exe' if os.name == 'nt' else 'django-admin')
        
        # Check if django-admin exists
        if not os.path.exists(django_admin):
            print(f"'{django_admin}' not found. Installing Django in the virtual environment.")
            # Install Django
            subprocess.check_call([os.path.join(env_bin, 'pip'), 'install', 'django'])
        
        # Recheck if django-admin exists after attempting installation
        if not os.path.exists(django_admin):
            raise FileNotFoundError(f"'{django_admin}' not found even after attempting to install Django. Please ensure Django is installed in the virtual environment.")
        
        # Run django-admin startproject command
        try:
            subprocess.check_call([django_admin, 'startproject', project_name], cwd=env_path)
            print(f"Django project '{project_name}' created successfully in '{env_path}'.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to create Django project: {e}")

    @staticmethod
    def setup_django_settings(project_name):
        project_dir = os.path.join(os.getcwd(), project_name)
        settings_path = os.path.join(project_dir, project_name, 'settings.py')
        
        # Additional setup for Django settings
        with open(settings_path, 'a') as settings_file:
            settings_file.write("\n# Additional settings for Whitenoise, Celery, Channels\n")
            settings_file.write("INSTALLED_APPS += ['rest_framework', 'channels', 'django_celery_beat', 'django_celery_results']\n")
            settings_file.write("MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']\n")
            settings_file.write("CELERY_BROKER_URL = 'redis://localhost:6379/0'\n")
            settings_file.write("CELERY_RESULT_BACKEND = 'django-db'\n")
            settings_file.write("STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'\n")
        
        print(f"Settings configured for Django project '{project_name}'.")

    @staticmethod
    def add_app_to_settings(project_name, app_name):
        project_dir = os.path.join(os.getcwd(), project_name)
        settings_path = os.path.join(project_dir, project_name, 'settings.py')

        try:
            with open(settings_path, 'a') as settings_file:
                settings_file.write(f"\nINSTALLED_APPS += ['{app_name}']\n")
        
            print(f"App '{app_name}' added to INSTALLED_APPS in '{project_name}' settings.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Settings file '{settings_path}' not found. Please ensure the Django project '{project_name}' is created correctly.")

    @staticmethod
    def add_middleware_to_settings(project_name, middleware_name):
        project_dir = os.path.join(os.getcwd(), project_name)
        settings_path = os.path.join(project_dir, project_name, 'settings.py')
        
        with open(settings_path, 'a') as settings_file:
            settings_file.write(f"\nMIDDLEWARE += ['{middleware_name}']\n")
        
        print(f"Middleware '{middleware_name}' added to MIDDLEWARE in '{project_name}' settings.")

    @staticmethod
    def update_staticfiles_storage(project_name, storage_setting):
        project_dir = os.path.join(os.getcwd(), project_name)
        settings_path = os.path.join(project_dir, project_name, 'settings.py')
        
        with open(settings_path, 'a') as settings_file:
            settings_file.write(f"\nSTATICFILES_STORAGE = '{storage_setting}'\n")
        
        print(f"STATICFILES_STORAGE updated to '{storage_setting}' in '{project_name}' settings.")

    @staticmethod
    def update_celery_settings(project_name, broker_url, result_backend):
        project_dir = os.path.join(os.getcwd(), project_name)
        settings_path = os.path.join(project_dir, project_name, 'settings.py')
        
        with open(settings_path, 'a') as settings_file:
            settings_file.write(f"\nCELERY_BROKER_URL = '{broker_url}'\n")
            settings_file.write(f"CELERY_RESULT_BACKEND = '{result_backend}'\n")
        
        print(f"CELERY settings updated with broker_url '{broker_url}' and result_backend '{result_backend}' in '{project_name}' settings.")

    
    @staticmethod
    def add_django_app(project_name, app_name):
        """
        Add a new Django app to the project.
        """
        project_dir = os.path.join(os.getcwd(), project_name)
        app_path = os.path.join(project_dir, app_name)
        
        # Ensure the full path exists
        os.makedirs(app_path, exist_ok=True)
        
        subprocess.check_call(['django-admin', 'startapp', app_name, app_path])
        print(f"Django app '{app_name}' added to project '{project_name}'.")

