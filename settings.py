import os

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
ALLOWED_HOSTS  = [open("/etc/hostname").read().strip()]
STATIC_URL     = "/static/"
PARITY_URL     = "http://127.0.0.1:8545"
ROOT_URLCONF   = "urls"
SECRET_KEY     = os.environ["SECRET_KEY"]
TEMPLATES      = [{"BACKEND" :
                      "django.template.backends.django.DjangoTemplates",
                   "DIRS"    : [os.path.join(BASE_DIR, "etcplanet/views")],
                   "OPTIONS" :
                      {"context_processors" :
                          ["django.template.context_processors.request",
                           "django.template.context_processors.debug",
                           "django.contrib.auth.context_processors.auth"]}}]
MIDDLEWARE     = ["django.middleware.security.SecurityMiddleware",
                  "django.contrib.sessions.middleware.SessionMiddleware",
                  "django.middleware.common.CommonMiddleware",
                  "django.middleware.csrf.CsrfViewMiddleware",
                  "django.contrib.auth.middleware.AuthenticationMiddleware",
                  "django.contrib.messages.middleware.MessageMiddleware",
                  "django.middleware.clickjacking.XFrameOptionsMiddleware"]
INSTALLED_APPS = ["etcplanet",
                  "django.contrib.admin",
                  "django.contrib.auth",
                  "django.contrib.contenttypes",
                  "django.contrib.messages",
                  "django.contrib.sessions",
                  "django.contrib.staticfiles"]
