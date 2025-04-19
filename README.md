
# Package for Ferrea application

[![Python formatting](https://github.com/Grimoldi/pyferrea-chassis/actions/workflows/format.yaml/badge.svg)](https://github.com/Grimoldi/pyferrea-chassis/actions/workflows/format.yaml)
[![Docstrings](https://github.com/Grimoldi/pyferrea-chassis/actions/workflows/docstrings.yaml/badge.svg)](https://github.com/Grimoldi/pyferrea-chassis/actions/workflows/docstrings.yaml)
[![Testing](https://github.com/Grimoldi/pyferrea-chassis/actions/workflows/testing.yaml/badge.svg)](https://github.com/Grimoldi/pyferrea-chassis/actions/workflows/testing.yaml)

This package contains some helpers classes or functions.

It's main focus is towards granting a standard:

- application observability (logger, performance monitoring, tracing) -> ferrea.observability module.
- python classes (mainly models) -> ferrea.models module.
- initialization for the FastApi webserver -> ferrea.api module.
- db interface -> ferrea.db_engine module.
- versioning with the help of the pyproject.toml Poetry file -> ferrea.pyproject module.

## How to install

``` python
pip install git+https://github.com/Grimoldi/pyferrea-chassis.git --upgrade
```

## How to use

For the chassis, you can directly import the `observability` module and call from it any function you need to init the appropriate helper.

``` python
from ferrea import observability
logger = observability.init_logger()
```

For the models, in the same way, you can import the _models_ module and refer to any of its class.

``` python
from ferrea. import models
author = models.Author("EG")
rating = models.Rating(5)
```

And so on...
