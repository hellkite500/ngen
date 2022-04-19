from abc import ABC, abstractmethod
from sys import platform
from pathlib import Path
from typing import List, Dict

class AbstractFormulation(ABC):
    """_summary_

    Args:
        abc (_type_): _description_
    """

    @property
    @abstractmethod
    def params(self):
        """_summary_

        """
        pass

    @property
    @abstractmethod
    def name(self):
        """_summary_

        """
        pass
    
    # def __str__(self) -> str:
    #     """_summary_

    #     Returns:
    #         str: _description_
    #     """
    #     return str(self.__dict__)
    def __repr__(self) -> str:
        return str( self.to_dict() )

    def to_dict(self) -> dict:
        return {"name": self.name,
                "params": self.params
                }

class BMIParams(ABC):
    """_summary_

    """

    def __init__(self, config_prefix: Path = None, config: str = '', 
                allow_exceed_end_time: bool=False, fixed_time_step: bool=True,
                output_variables: Dict[str, str]={},
                library_prefix: Path=None, library: Path='lib',
                ):

        #If we need to initialize a library, do so here
        self._library_file = Path(library)
        if library_prefix:
            self._library_file = library_prefix.joinpath(self._library_file)

        #adjust the extension if needed for the system this is being run on
        #TODO might want to make this user configurable
        self._library_file = self._library_file.with_suffix( self.get_system_lib_extension() )
        
        if config_prefix:
            config = config_prefix.joinpath(config)
        self._init_config = config

        self._allow_exceed_end_time = allow_exceed_end_time
        self._fixed_time_step = fixed_time_step

        self._output_vars = []
        self._output_headers = []

        for k,v in output_variables.items():
            self._output_vars.append(k)
            if v != '':
                self._output_headers.append(v)
            else:
                self._output_headers.append(k)

    @property
    @abstractmethod
    def model_name(self):
        """_summary_

        """
        pass

    @property
    def library_file(self):
        """_summary_

        """
        return self._library_file

    @property
    @abstractmethod
    def model_params(self):
        """_summary_

        Returns:
            _type_: _description_
        """

    @property
    def init_config(self):
        """_summary_

        """
        return self._init_config

    @property
    @abstractmethod
    def main_output_variable(self):
        """_summary_

        """
        pass

    @property
    def uses_forcing_file(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return False
    
    @property
    @abstractmethod
    def variables_names_map(self):
        """_summary_

        """
        pass

    @property
    def output_variables(self) -> List[str]:
        """_summary_

        Returns:
            List[str]: _description_
        """
        return self._output_vars

    @property
    def output_header_fields(self) -> List[str]:
        """_summary_

        Returns:
            List[str]: _description_
        """
        return self._output_headers

    @property
    def allow_exceed_end_time(self) -> bool:
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._allow_exceed_end_time
    
    @property
    def fixed_time_step(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return self._fixed_time_step
    

    #AbstractFormulation Properties
    @property
    def params(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        params = {
                "model_type_name": self.model_name,
                "init_config": str( self.init_config ),
                "main_output_variable":self.main_output_variable,
                "variables_name_map": self.variables_names_map,
                "model_params": self.model_params,
                "uses_forcing_file": self.uses_forcing_file,
                "allow_exceed_end_time": self.allow_exceed_end_time,
                "fixed_time_step": self.fixed_time_step
                }
        if self.output_variables:
            params.update({'output_variables':self.output_variables})
        if self.output_header_fields:
            params.update({'output_header_fields':self.output_header_fields})
        if self.library_file is not None:
            params.update({'library_file':str( self.library_file )})

        return params

    @classmethod
    def get_system_lib_extension(cls) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        if platform == "linux":
            return '.so'
        elif platform == "darwin":
            return '.dylib'

class BMIC(BMIParams, AbstractFormulation):
    """_summary_
        MRO is important here, since BMIParams implements the base `params` for AbstractFormulation
        and this type extends these pararams by calling super().params.update
        the BMIParams should be first in the MRO list (hence the first paraent of this class)
    Args:
        AbstractFormulation (_type_): _description_

    Returns:
        _type_: _description_
    """

    @property
    def name(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return "bmi_c"
    
    @property
    def registration_function(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return "register_bmi"
    
    @property
    def params(self) -> dict:
        params = super().params
        params.update({'registration_function':self.registration_function})
        return params

class BMIFortran(BMIParams, AbstractFormulation):
    """_summary_

    Args:
        AbstractFormulation (_type_): _description_

    Returns:
        _type_: _description_
    """
    @property
    def name(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return "bmi_fortran"

class BMIPython(BMIParams, AbstractFormulation):
    """_summary_

    Args:
        AbstractFormulation (_type_): _description_

    Returns:
        _type_: _description_
    """
    @property
    def name(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return "bmi_python"

    @property
    def python_type(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return self.python_type
    
    #Python modules don't use library file...
    @property
    def library_file(self):
        """_summary_

        """
        return None

class BMICxx(BMIParams, AbstractFormulation):
    """_summary_

    Args:
        AbstractFormulation (_type_): _description_

    Returns:
        _type_: _description_
    """
    @property
    def name(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return "bmi_c++"
    
    @property
    @abstractmethod
    def library_file(self):
        """_summary_

        """
        pass

    @property
    def params(self) -> dict:
        params = super().params
        params.update({'library_file':self.library_file})
        return params

class BMIMulti(AbstractFormulation):
    """_summary_

    Args:
        AbstractFormulation (_type_): _description_

    Returns:
        _type_: _description_
    """
    @property
    def name(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return "bmi_multi"



class MultiBMI(BMIParams, AbstractFormulation):
    """_summary_

    Args:
        AbstractFormulation (_type_): _description_

    Returns:
        _type_: _description_
    """
    def __init__(self, modules: List[AbstractFormulation], **kwargs):
        """_summary_

        Args:
            modules (List[AbstractFormulation]): _description_

        Returns:
            _type_: _description_
        """
        super().__init__(config='', **kwargs)
        self._modules = modules

    #bmiparam properties
    @property
    def main_output_variable(self):
        return self.modules[-1].params['main_output_variable']

    @property
    def model_name(self):
        return '_'.join( [m.params['model_type_name'] for m in self.modules ] )

    @property
    def model_params(self):
        #not relevant for multi-bmi
        return {}
    
    @property
    def variables_names_map(self):
        #not relevant for multi-bmi
        return {}

    @property
    def name(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return "bmi_multi"
    
    @property
    def modules(self) -> List[AbstractFormulation]:
        """_summary_

        Returns:
            List[Formulation]: _description_
        """
        return self._modules

    @property
    def params(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        params = super().params
        #Override params
        params.update( {"modules": [ m.params for m in self.modules ] } )
        #Is this always true???
        params.update( {"allow_exceed_end_time": True} )
        #TODO is this one really required???
        params.update({"forcing_file":""})

        #pop super params that don't apply
        params.pop("variables_name_map")
        params.pop("model_params")
        params.pop("uses_forcing_file")
        params.pop("fixed_time_step")
        params.pop("library_file")
        return params
