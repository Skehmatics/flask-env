import os
import json


class MetaFlaskEnv(type):
    def __init__(cls, name, bases, dict):
        """
        MetaFlaskEnv class initializer.

        This function will get called when a new class which utilizes this metaclass is defined,
        as opposed to when it is initialized.
        """
        super(MetaFlaskEnv, cls).__init__(name, bases, dict)

        # Get our internal settings
        prefix = dict.get('ENV_PREFIX', '')
        load_all = dict.get('ENV_LOAD_ALL', False)

        # Override default configuration from environment variables
        for key, value in os.environ.items():
            # Only include environment keys that start with our prefix (if we have one)
            if not key.startswith(prefix):
                continue

            # Strip the prefix from the environment variable name
            key = key[len(prefix):]

            # Unless we specify that we want to load all environment variables
            #   only load variables that we have predefined on our object
            if not load_all and not hasattr(cls, key):
                continue

            # Parse value according to JSON standards
            # If that fails, just keep it a string
            try:
                value = json.loads(value)
            except ValueError:
                pass

            # Update our config with the value from `os.environ`
            setattr(cls, key, value)
