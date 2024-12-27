"""
Django settings for spms project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

from ckeditor_demo.settings import CKEDITOR_CONFIGS
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',
    'unfold.contrib.import_export',
    'unfold.contrib.guardian',
    'unfold.contrib.simple_history',
    'ckeditor',
    'ckeditor_uploader',
    'wkhtmltopdf',
    'settings.apps.SettingsConfig',
    'accounts.apps.AccountsConfig',
    'projects.apps.ProjectsConfig',
    'reviews.apps.ReviewsConfig',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "spms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "spms.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = False

LANGUAGES = [('zh-hans', '中文简体')]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CKEDITOR_UPLOAD_PATH = "uploads/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Unfold Settings
UNFOLD = {
    'SITE_TITLE': '广西师范大学学科数据分析中心',
    'SITE_HEADER': '学科数据分析中心',
    'SITE_URL': '/',
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "#eff6ff",
            "100": "#dbeafe",
            "200": "#bfdbfe",
            "300": "#93c5fd",
            "400": "#60a5fa",
            "500": "#3b82f6",
            "600": "#2563eb",
            "700": "#1d4ed8",
            "800": "#1e40af",
            "900": "#1e3a8a",
            "950": "#172554",
        },
    },
    'SIDEBAR': {
        'show_search': False,
        'show_all_applications': False,
        'navigation': [
            {
                'title': '用户管理',
                'separator': True,
                'collapsible': False,
                'items': [
                    {
                        'title': '用户资料',
                        'icon': 'person',
                        'link': reverse_lazy('admin:profile_list')
                        # 'link': reverse_lazy('admin:accounts_profile_changelist'),
                        # 'permission': lambda request: request.user.has_perm('accounts.view_profile')
                    },
                    {
                        'title': '用户',
                        'icon': 'manage_accounts',
                        'link': reverse_lazy('admin:auth_user_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    },
                    {
                        'title': '用户组',
                        'icon': 'group',
                        'link': reverse_lazy('admin:auth_group_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    },
                    {
                        'title': '评审组',
                        'icon': 'groups',
                        'link': reverse_lazy('admin:accounts_team_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    }
                ]
            },
            {
                'title': '项目管理',
                'separator': True,
                'collapsible': False,
                'items': [
                    {
                        'title': '项目信息列表',
                        'icon': 'tactic',
                        'link': reverse_lazy('admin:project_list'),
                        'permission': lambda request: request.user.has_perm('informations.view_information')
                    }
                ]
            },
            {
                'title': '项目评审管理',
                'separator': True,
                'collapsible': False,
                'items': [
                    {
                        'title': '项目评审列表',
                        'icon': 'planner_review',
                        'link': reverse_lazy('admin:reviews_review_changelist'),
                        'permission': lambda request: request.user.has_perm('reviews.view_review')
                    }
                ]
            },
            {
                'title': '系统管理',
                'separator': True,
                'collapsible': True,
                'items': [
                    {
                        'title': '性别',
                        'icon': 'man',
                        'link': reverse_lazy('admin:settings_gender_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    },
                    {
                        'title': '身份证件类型',
                        'icon': 'id_card',
                        'link': reverse_lazy('admin:settings_idtype_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    },
                    {
                        'title': '学历',
                        'icon': 'history_edu',
                        'link': reverse_lazy('admin:settings_education_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    },
                    {
                        'title': '学位',
                        'icon': 'school',
                        'link': reverse_lazy('admin:settings_degree_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    },
                    {
                        'title': '职称',
                        'icon': 'work',
                        'link': reverse_lazy('admin:settings_title_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    },
                    {
                        'title': '学科',
                        'icon': 'subject',
                        'link': reverse_lazy('admin:settings_subject_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    },
                    {
                        'title': '研究类型',
                        'icon': 'science',
                        'link': reverse_lazy('admin:settings_type_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    },
                    {
                        'title': '单位',
                        'icon': 'house',
                        'link': reverse_lazy('admin:settings_department_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    },
                    {
                        'title': '项目系列',
                        'icon': 'newsstand',
                        'link': reverse_lazy('admin:settings_series_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    },
                    {
                        'title': '项目阶段',
                        'icon': 'floor',
                        'link': reverse_lazy('admin:settings_phase_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    },
                    {
                        'title': '系统设置',
                        'icon': 'settings',
                        'link': reverse_lazy('admin:settings_setting_changelist'),
                        'permission': lambda request: request.user.is_superuser
                    }
                ]
            }
        ]
    }
}

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full'
    }
}

G_SCHOOL = 1
G_COLLEGE = 2
G_PANELIST = 3
G_APPLICANT = 4

try:
    from .local_settings import *
except ImportError:
    pass
