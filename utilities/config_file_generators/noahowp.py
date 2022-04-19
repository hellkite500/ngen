from pathlib import Path
from formulation import BMIFortran
from typing import Dict, Union

class NoahOWP(BMIFortran):
    """_summary_

    Args:
        BMIParams (_type_): _description_
        BMIFortran (_type_): _description_
    """

    def __init__(self, config_prefix: Path=None, config='{{id}}.namelist.input', 
                library_prefix: Path=None, library: Union[Path, str]="libsurfacebmi", 
                name_map: Dict[str, str]={}, model_params: Dict[str, str]={}, **kwargs):
        super().__init__(config_prefix=config_prefix, config=config, allow_exceed_end_time=True, library_prefix=library_prefix, library=library, **kwargs)

        self._model_params = model_params
        self._main_output_variable = 'QINSUR'
        self._variable_names_map =  {
            "PRCPNONC": "atmosphere_water__liquid_equivalent_precipitation_rate",
            "Q2": "atmosphere_air_water~vapor__relative_saturation",
            "SFCTMP": "land_surface_air__temperature",
            "UU": "land_surface_wind__x_component_of_velocity",
            "VV": "land_surface_wind__y_component_of_velocity",
            "LWDN": "land_surface_radiation~incoming~longwave__energy_flux",
            "SOLDN": "land_surface_radiation~incoming~shortwave__energy_flux",
            "SFCPRS": "land_surface_air__pressure"
        }
        #Update the default name map based on names_map
        self._variable_names_map.update( name_map )

    #BMI Properties
    @property
    def model_name(self):
        return "NoahOWP"
    
    @property
    def model_params(self):
        return self._model_params

    @property
    def main_output_variable(self):
        return self._main_output_variable

    @property
    def variables_names_map(self):
        return self._variable_names_map
