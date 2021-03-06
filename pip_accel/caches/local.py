# Accelerator for pip, the Python package manager.
#
# Author: Peter Odding <peter.odding@paylogic.com>
# Last Change: October 31, 2015
# URL: https://github.com/paylogic/pip-accel

"""
Local file system cache backend.

This module implements the local cache backend which stores distribution
archives on the local file system. This is a very simple cache backend, all it
does is create directories and write local files. The only trick here is that
new binary distribution archives are written to temporary files which are
then moved into place atomically using :func:`os.rename()` to avoid partial
reads caused by running multiple invocations of pip-accel at the same time
(which happened in `issue 25`_).

.. _issue 25: https://github.com/paylogic/pip-accel/issues/25
"""

# Standard library modules.
import logging
import os
import shutil

# Modules included in our package.
from pip_accel.caches import AbstractCacheBackend
from pip_accel.utils import AtomicReplace, makedirs

# Initialize a logger for this module.
logger = logging.getLogger(__name__)


class LocalCacheBackend(AbstractCacheBackend):

    """The local cache backend stores Python distribution archives on the local file system."""

    PRIORITY = 10

    def get(self, filename):
        """
        Check if a distribution archive exists in the local cache.

        :param filename: The filename of the distribution archive (a string).
        :returns: The pathname of a distribution archive on the local file
                  system or :data:`None`.
        """
        pathname = os.path.join(self.config.binary_cache, filename)
        if os.path.isfile(pathname):
            logger.debug("Distribution archive exists in local cache (%s).", pathname)
            return pathname
        else:
            logger.debug("Distribution archive doesn't exist in local cache (%s).", pathname)
            return None

    def put(self, filename, handle):
        """
        Store a distribution archive in the local cache.

        :param filename: The filename of the distribution archive (a string).
        :param handle: A file-like object that provides access to the
                       distribution archive.
        """
        file_in_cache = os.path.join(self.config.binary_cache, filename)
        logger.debug("Storing distribution archive in local cache: %s", file_in_cache)
        makedirs(os.path.dirname(file_in_cache))
        # Stream the contents of the distribution archive to a temporary file
        # to avoid race conditions (e.g. partial reads) between multiple
        # processes that are using the local cache at the same time.
        with AtomicReplace(file_in_cache) as temporary_file:
            with open(temporary_file, 'wb') as temporary_file_handle:
                shutil.copyfileobj(handle, temporary_file_handle)
        logger.debug("Finished caching distribution archive in local cache.")
