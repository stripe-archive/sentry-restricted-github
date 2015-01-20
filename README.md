# sentry-restricted-github

A limited alternative to sentry-github which doesn't require write access to
repos. It allows creating tickets but doesn't link them to the sentry error
group.


# Install

`pip install -e git://github.com/stripe/sentry-restricted-github.git@0.4#egg=sentry-restricted-github`


# Local Development

```
workon your-virtual-env # optional
python setup.py develop
```

Then install & run sentry.


# Licence

MIT. See LICENSE.txt for details.
