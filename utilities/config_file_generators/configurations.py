from enum import Enum
from pathlib import Path
from formulation import MultiBMI

class Forcing:
    """_summary_

    """

    class Provider(str, Enum):
        CSV = "csvPerFeature"
        NetCDF = "FIXME"
    
    def __init__(self, pattern: str = '', path: str=None, provider: Provider = Provider.CSV):
        self._pattern = pattern
        self._path = Path(path)
        self._provider = provider.value
    
    def __repr__(self):
        return str( {"forcing": self.to_dict()} )

    def to_dict(self) -> dict:
        return {
            "file_pattern":self._pattern,
            "path": str(self._path),
            "provider": self._provider
        }


class Time():
    """_summary_

    """

    def __init__(self, start: str, end: str, interval: int =3600):
        self._start = start
        self._end = end
        self._interval = interval

    def __repr__(self):
        return str( {"time": self.to_dict()})
    
    def to_dict(self) -> str:
        return {
            "start_time": self._start,
            "end_time": self._end,
            "output_interval": self._interval
        }

class Routing():
    """_summary_

    """

    def __init__(self, path: str, conf: str):
        self._path = Path(path)
        self._conf = Path(conf)

    def __repr__(self):
        return str( {"routing": self.to_dict()})

    def to_dict(self) -> dict:
        return {
            "t_route_connection_path": str( self._path ),
            "t_route_config_file_with_path": str( self._conf )
        }

class Formulation():
    """_summary_

    """

    def __init__(self, formulation, forcing):
        self._formulations = [formulation]
        self._forcing = forcing
    
    def __repr__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return str( { "formulations": str(self._formulations),
                      "forcing": str( self._forcing )
                    })
    def to_dict(self) -> dict:
        return { "formulations": [ f.to_dict() for f in self._formulations ],
                      "forcing": self._forcing.to_dict()
                    }

class MultiFormulation():
    """_summary_

    """

    def __init__(self, formulations, forcing, **kwargs):
        self._formulations = [MultiBMI(formulations, **kwargs)]
        self._forcing = forcing
    
    def __repr__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return str( { "formulations": str(self._formulations),
                      "forcing": str( self._forcing )
                    })
    def to_dict(self) -> dict:
        return { "formulations": [ f.to_dict() for f in self._formulations ],
                      "forcing": self._forcing.to_dict()
                    }