from pathlib import Path
from formulation import BMIPython

class LSTM(BMIPython):
    """_summary_

    Args:
        BMIParams (_type_): _description_
        BMIPython (_type_): _description_
    """

    def __init__(self, config_prefix: Path = None, python_module: str=None, config=r'{{id}}.yml', name_map={}, model_params={}):
        super().__init__(config_prefix=config_prefix, config=config, allow_exceed_end_time=True)
        #super(BMIParams).__init__(library, config, name_map, model_params)
        if python_module is None:
            self._python_module = "bmi_lstm.bmi_LSTM"
        self._main_output_variable = "land_surface_water__runoff_depth"
        self._variable_names_map =  {
            "atmosphere_water__time_integral_of_precipitation_mass_flux":"RAINRATE"
        }
        #Update the default name map based on names_map
        self._variable_names_map.update( name_map )

    @property
    def params(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        params = super().params
        #don't allow model_params in lstm config
        params.pop('model_params')
        #add extra param for python module
        params.update({"python_type":self._python_module})
        return params

    #BMI Properties
    @property
    def model_name(self):
        return "LSTM"
    
    @property
    def model_params(self):
        #don't allow model_params in lstm config
        return {}

    @property
    def main_output_variable(self):
        return self._main_output_variable

    @property
    def variables_names_map(self):
        return self._variable_names_map