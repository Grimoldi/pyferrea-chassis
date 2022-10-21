# Package for Ferrea application

This package contains some helpers class or function.

It's main focus it towards:

- granting a standard for application observability (logger, performance monitoring, tracing) -> chassis.helpers module.
- granting a standard for python classes (mainly models) -> models.models module.

## How to install

``` python
pip install git+https://github.com/Grimoldi/pyferrea-chassis.git --upgrade
```

## How to use

For the chassis, you can directly import the _helpers_ module and call from it any function you need to init the appropriate helper.

``` python
from ferrea.chassis import helpers
logger = helpers.init_logger()
```

For the models, in the same way, you can import the _models_ module and refer to any of its class.

``` python
from ferrea.models import models  # I know, short on fantasy for name
author = models.Author("EG")
rating = models.Rating(5)
```
