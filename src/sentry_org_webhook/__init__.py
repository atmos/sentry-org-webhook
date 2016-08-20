try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry_org_webhook').version
except Exception, e:
    VERSION = 'unknown'
