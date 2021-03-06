# Accelerator for pip, the Python package manager.
#
# Author: Peter Odding <peter.odding@paylogic.com>
# Last Change: October 31, 2015
# URL: https://github.com/paylogic/pip-accel

"""
Exceptions for structured error handling.

This module defines named exceptions raised by pip-accel when it encounters
error conditions that:

1. Already require structured handling inside pip-accel
2. May require structured handling by callers of pip-accel

Yes, I know, I just made your lovely and elegant Python look a whole lot like
Java! I guess the message to take away here is that (in my opinion) structured
error handling helps to build robust software that acknowledges failures exist
and tries to deal with them (even if only by clearly recognizing a problem and
giving up when there's nothing useful to do!).

Hierarchy of exceptions
-----------------------

If you're interested in implementing structured handling of exceptions reported
by pip-accel the following diagram may help by visualizing the hierarchy:

.. inheritance-diagram:: EnvironmentMismatchError UnknownDistributionFormat InvalidSourceDistribution \
                         BuildFailed NoBuildOutput CacheBackendError CacheBackendDisabledError \
                         DependencyInstallationRefused DependencyInstallationFailed
   :parts: 1

----
"""

from pip_accel.utils import compact


class PipAcceleratorError(Exception):

    """Base exception for all exception types explicitly raised by :mod:`pip_accel`."""

    def __init__(self, text, **kw):
        """
        Initialize a :class:`PipAcceleratorError` object.

        Accepts the same arguments as :func:`.compact()`.
        """
        super(PipAcceleratorError, self).__init__(compact(text, **kw))


class NothingToDoError(PipAcceleratorError):

    """
    Custom exception raised on empty requirement sets.

    Raised by :func:`~pip_accel.PipAccelerator.get_pip_requirement_set()`
    when pip doesn't report an error but also doesn't generate a requirement
    set (this happens when the user specifies an empty requirements file).
    """


class EnvironmentMismatchError(PipAcceleratorError):

    """
    Custom exception raised when a cross-environment action is attempted.

    Raised by :func:`~pip_accel.PipAccelerator.validate_environment()` when
    it detects a mismatch between :data:`sys.prefix` and ``$VIRTUAL_ENV``.
    """


class UnknownDistributionFormat(PipAcceleratorError):

    """
    Custom exception raised on unrecognized distribution archives.

    Raised by :attr:`~pip_accel.req.Requirement.is_wheel` when it cannot
    discern whether a given unpacked distribution is a source distribution or a
    wheel distribution.
    """


class BinaryDistributionError(PipAcceleratorError):

    """Base class for exceptions related to the generation of binary distributions."""


class InvalidSourceDistribution(BinaryDistributionError):

    """
    Custom exception raised when a source distribution's setup script is missing.

    Raised by :func:`~pip_accel.bdist.BinaryDistributionManager.build_binary_dist()`
    when the given directory doesn't contain a Python source distribution.
    """


class BuildFailed(BinaryDistributionError):

    """
    Custom exception raised when a binary distribution build fails.

    Raised by :func:`~pip_accel.bdist.BinaryDistributionManager.build_binary_dist()`
    when a binary distribution build fails.
    """


class NoBuildOutput(BinaryDistributionError):

    """
    Custom exception raised when binary distribution builds don't generate an archive.

    Raised by :func:`~pip_accel.bdist.BinaryDistributionManager.build_binary_dist()`
    when a binary distribution build fails to produce the expected binary
    distribution archive.
    """


class CacheBackendError(PipAcceleratorError):

    """Custom exception raised by cache backends when they fail in a controlled manner."""


class CacheBackendDisabledError(CacheBackendError):

    """Custom exception raised by cache backends when they require configuration."""


class SystemDependencyError(PipAcceleratorError):

    """Base class for exceptions related to missing system packages."""


class DependencyInstallationRefused(SystemDependencyError):

    """
    Custom exception raised when installation of dependencies is refused.

    Raised by :class:`.SystemPackageManager` when one or more known to be
    required system packages are missing and automatic installation of missing
    dependencies is disabled by the operator.
    """


class DependencyInstallationFailed(SystemDependencyError):

    """
    Custom exception raised when installation of dependencies fails.

    Raised by :class:`.SystemPackageManager` when the installation of
    missing system packages fails.
    """
