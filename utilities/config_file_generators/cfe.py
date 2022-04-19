from pathlib import Path
from formulation import BMIC
from typing import Dict, Union

class CFE(BMIC):
    """_summary_

    Args:
        BMIParams (_type_): _description_
        BMIC (_type_): _description_
    """

    def __init__(self, config_prefix: Path=None, config='{{id}}_bmi_config.ini', 
                library_prefix: Path=None, library: Union[Path, str]="libbmicfe", 
                name_map: Dict[str, str]={}, model_params: Dict[str, str]={}):
        super().__init__(config_prefix=config_prefix, config=config, allow_exceed_end_time=True, library_prefix=library_prefix, library=library)

        self._model_params = model_params
        self._main_output_variable = 'Q_OUT'
        self._registration_function = "register_bmi_cfe"

        self._variable_names_map =  {
           "water_potential_evaporation_flux": "EVAPOTRANS",
                                    "atmosphere_water__liquid_equivalent_precipitation_rate": "QINSUR"
        }
        #Update the default name map based on names_map
        self._variable_names_map.update( name_map )

    #BMI Properties
    @property
    def registration_function(self) -> str:
        return self._registration_function

    @property
    def model_name(self):
        return "CFE"
    
    @property
    def model_params(self):
        return self._model_params

    @property
    def registration_function(self) -> str:
        return self._registration_function

    @property
    def main_output_variable(self):
        return self._main_output_variable

    @property
    def variables_names_map(self):
        return self._variable_names_map
