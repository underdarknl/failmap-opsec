from pkg_resources import get_distribution

import failmap.signals  # noqa

__version__ = get_distribution(__name__.split('.', 1)[0]).version
