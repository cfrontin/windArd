import os
import yaml

import numpy as np


def create_FLORIS_yamlfile(
    filename_turbine_spec,
    filename_turbine_FLORIS,
):

    # load generic spec
    with open(filename_turbine_spec, "r") as file_turbine_spec:
        turbine_spec = yaml.safe_load(file_turbine_spec)

    # load speed/power/thrust file
    filename_power_thrust = os.path.join(
        os.path.split(os.path.abspath(filename_turbine_spec))[0],
        turbine_spec["performance_data_ccblade"]["power_thrust_csv"],
    )
    pt_raw = np.genfromtxt(filename_power_thrust, delimiter=",").T.tolist()

    # create FLORIS config dict
    turbine_FLORIS = dict()
    turbine_FLORIS["turbine_type"] = turbine_spec["description"]["name"]
    turbine_FLORIS["hub_height"] = turbine_spec["geometry"]["height_hub"]
    turbine_FLORIS["rotor_diameter"] = turbine_spec["geometry"]["diameter_rotor"]
    turbine_FLORIS["TSR"] = turbine_spec["nameplate"]["TSR"]
    # turbine_FLORIS["multi_dimensional_cp_ct"] = True
    # turbine_FLORIS["power_thrust_data_file"] = filename_power_thrust
    turbine_FLORIS["power_thrust_table"] = {
        "cosine_loss_exponent_yaw": turbine_spec["model_specifications"]["FLORIS"][
            "exponent_penalty_yaw"
        ],
        "cosine_loss_exponent_tilt": turbine_spec["model_specifications"]["FLORIS"][
            "exponent_penalty_tilt"
        ],
        "peak_shaving_fraction": turbine_spec["model_specifications"]["FLORIS"][
            "fraction_peak_shaving"
        ],
        "peak_shaving_TI_threshold": 0.0,
        "ref_air_density": turbine_spec["performance_data_ccblade"][
            "density_ref_cp_ct"
        ],
        "ref_tilt": turbine_spec["performance_data_ccblade"]["tilt_ref_cp_ct"],
        "wind_speed": pt_raw[0],
        "power": (
            0.5
            * turbine_spec["performance_data_ccblade"]["density_ref_cp_ct"]
            * (np.pi / 4.0 * turbine_spec["geometry"]["diameter_rotor"] ** 2)
            * np.array(pt_raw[0]) ** 3
            * pt_raw[1]
            / 1e3
        ).tolist(),
        "thrust_coefficient": pt_raw[2],
    }

    # write FLORIS config file
    with open(filename_turbine_FLORIS, "w") as file_turbine_FLORIS:
        yaml.safe_dump(turbine_FLORIS, file_turbine_FLORIS)

    return filename_turbine_FLORIS
