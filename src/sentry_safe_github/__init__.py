try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-safe-github').version
except Exception, e:
    VERSION = 'unknown'
