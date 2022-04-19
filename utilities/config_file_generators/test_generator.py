from configurations import *
from cfe import CFE
from noahowp import NoahOWP
from lstm import LSTM
import json

time = Time("2015-12-01 00:00:00", "2015-12-30 23:00:00")
libpath=Path("./extern")
routing = Routing( "extern/t-route/src/ngen_routing/src", "extern/t-route/test/input/yaml/ngen.yaml" )

cfe = CFE(config_prefix=Path("CFE"), config="{{id}}_bmi_config_cfe_pass.txt", library_prefix=libpath)
noahowp = NoahOWP(library_prefix=libpath,  
                 config_prefix=Path("NOAH"), config="{{id}}.input")
lstm = LSTM(config_prefix=Path('test'))

#Share forcing for all formulations
forcing = Forcing(pattern=".*{{id}}.*..csv", path="./data/forcing/", provider=Forcing.Provider.CSV)

cfe_formulation = Formulation( cfe, forcing )

configs = {}
configs['cfe'] = { "global": cfe_formulation.to_dict(),
                     "time": time.to_dict(),
                     "routing": routing.to_dict()}


multi = MultiFormulation( [noahowp, cfe], forcing, output_variables={'QINSUR':'precip_in', 'Q_OUT':'flow_out'},)

configs['multi'] = { "global": multi.to_dict(),
                     "time": time.to_dict(),
                     "routing": routing.to_dict()}

lstm_formulation = Formulation(lstm, forcing)

configs['lstm'] = { "global": lstm_formulation.to_dict(),
                    "time": time.to_dict(),
                    "routing": routing.to_dict()}

for name, config in configs.items():
    with open(f'{name}_realization_config.json', 'w') as f:
        f.write( json.dumps(config, indent=4) )


catchment_map = {'cat-2':multi, 'cat-6':lstm}

override = { "global": cfe.to_dict(),
             "time": time.to_dict(),
             "routing": routing.to_dict(),
             "catchments": { k:v.to_dict() for k,v in catchment_map.items()}
            }

print( json.dumps(override, indent=4) )