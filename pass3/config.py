import inspect
import os
import json

_cfg = {}
_last_config_path = None

def get_config(path=None):
    """
    Load a configuration from a specified path, or one of the default paths:
        - ~/.pass3.json

    The config is only ever loaded once, all return values from this method
    are a singleton.

    :param str path: Use this file before looking in the default paths
    :returns: Configuration dictionary
    """
    global _cfg
    global _last_config_path
    if _cfg :
        return _cfg

    default_paths = [
        os.path.abspath(os.path.join(os.path.expanduser('~'), '.pass3.json')),
        os.path.abspath(os.path.join(os.path.dirname(inspect.stack()[0][1]), 'etc', 'pass3.json'))
    ]
    if ( path ):
        default_paths = [path] + default_paths

    for path in (default_paths):
        if path is None:
            continue
        try:
            ifile = open(path, 'r')
            _cfg = json.loads(ifile.read())
            ifile.close()
            _last_config_path = path
            return _cfg
        except IOError, e:
            continue
        except Exception, e:
            if ( ifile ):
                ifile.close()
            raise Exception("While reading config in {} : {}".format(path, str(e)))
    raise IOError("No config file found in any of the following locations: \n\t{}".format("\n\t".join(default_paths)))

def save(path=None):
    """
    Save the configuration as it currently stands. If no filename
    is provided, the file from which it was loaded it used.

    :param str path: Alternate path to save the config
    """
    global _cfg
    global _last_config_path
    if not path:
        path = _last_config_path
    ofile = open(path, 'w')
    ofile.write(json.dumps(_cfg, indent=4, sort_keys=True))
    ofile.close()
