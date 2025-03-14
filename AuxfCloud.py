from ParametersCloud import f_error_code
from re import match

def f_regex_code(f27_value: str):
    if f27_value != "0":
        f27_match = match(r"^\d{3}", f27_value)
        return f27_match.group(0) if f27_match else None
    return None

def f_typecast_element(f23_list: list, f23_storage: str, f23_time: str):
    try:
        f23_aux_list: list = []
        for _ in f23_list:
            f23_aux_list.append(float(_))
        f23_storage: float = float(f23_storage)
        f23_time: float = float(f23_time)
    except (ValueError, TypeError, NameError):
        return "T"
    return f23_aux_list, f23_storage, f23_time


def f_checks_element(f22_list_vars: list, f22_sc: str, f22_storage:float, f22_time: float,
                     f22_codes: list, f22_norm_values: list, f22_range_values: list, f22_list_smart: list):
    list_dc: list = f22_codes
    f22_smart: list = f22_list_smart
    for _ in range(len(f22_list_vars)):
        if (f22_list_vars[_] < f22_norm_values[_][0]) or (f22_list_vars[_] > f22_norm_values[_][1]):
            return f22_smart[_]
    if f22_sc not in list_dc:
        return "SC"
    if (f22_storage < f22_range_values[0]) or (f22_storage > f22_range_values[1]):
        return "TB"
    if f22_time<0:
        return "T"
    return ""


def f_streetlight_element(f24_preds: float, f24_list_vars: list, f24_ttf: float, f24_threshold_list: list):
    if f24_preds<=f24_threshold_list[0]:
        return "N", 0, "0"
    if f24_preds<=f24_threshold_list[1]:
        return "A", f24_ttf, "187.194.3"
    else:
        return "F", 0, f_error_code(f24_list_vars)


def f_normalization(f10_list_vars: list, f10_sc: str, f11_norm_list: list):
    f10_normalization_values: list = f11_norm_list
    for i in range(len(f10_list_vars)):
        f10_list_vars[i] = ((f10_list_vars[i] - f10_normalization_values[i][0]) /
                       (f10_normalization_values[i][1] - f10_normalization_values[i][0]))
    f10_sc: int = f10_normalization_values[-1][0][f10_sc]
    return f10_list_vars, f10_sc


def f_storage_bins(f11_storage: float, f11_bins: list):
    f11_ranges: list = f11_bins
    for i, value in enumerate(f11_ranges):
        if f11_storage < value:
            return i
        elif f11_storage > f11_ranges[-1]:
            return len(f11_ranges)


def f_sc_tb_value(f12_sc: int, f12_tb: int, f12_dict: dict):
    dict_combinations: dict = f12_dict
    f12_combination: str = f"{str(f12_sc)}_{str(f12_tb)}"
    return dict_combinations[f12_combination]
