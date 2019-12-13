import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f86cfj&0t2lg3+orn$_t5fyr=f_5mzk_a99q%qp-f&xyhgu)b#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web.apps.WebConfig',
    'rbac.apps.RbacConfig',
    'stark.apps.StarkConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rbac.middlewares.rbac.RbacMiddleware',
]

ROOT_URLCONF = 'CompanyQuiry.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CompanyQuiry.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 连接数据库类型 在末尾写入mysql即可
        'ENGINE': 'django.db.backends.mysql',
        # 数据库地址
        'HOST': '127.0.0.1',
        # 端口
        'PORT': 3306,
        # 数据库名
        'NAME': 'Company',
        # 用户
        'USER': 'root',
        # 密码
        'PASSWORD': 'Kunzhi_1130'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# admin后台改为中文
# 如果表单名改完自定义中文，在model下的init中设置默认配置 default_app_config = 'apps.blog.apps.BlogConfig'
LANGUAGE_CODE = 'zh-Hans'

# 时区设置到上海
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 时间过滤 month 不好用时候，改为False   （Mysql才会出现）


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')  # 把新增加的添加到内置的STATICFILES_DIRS内
]

# STATIC_ROOT = os.path.join(BASE_DIR, "static")  # 生产环境下比较配置否则static找不到

# 配置用户上传静态文件 media
# 还需要在url.py中进行配置才生效
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 做别名
MEDIA_URL = '/media/'


RBAC_USER_MODEL_CLASS = 'web.models.UserInfo'

# 权限 key
PERMISSION_SESSION_KEY = "company_permission_url_list_key"  # 名字根据项目更改
# 菜单 key
MENU_SESSION_KEY = 'company_menu_list_key'  # 名字根据项目更改

# 访问白名单
VALID_URL_LIST = [
    '/login/',
    '/admin/.*',
    # '',
]

# 需要登录但无需权限的URL
NO_PERMISSION_LIST = [
    '/logout/',
    '/index/',
]

# 自动收录路由白名单,自动忽略的名单
AUTO_DISCOVER_EXCLUDE = [
    '/admin/.*',
    '/login/',
    '/logout/',
    '/index/',
    # '',
]