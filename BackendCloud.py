from AuxfCloud import (f_regex_code, f_typecast_element, f_checks_element, f_normalization, f_storage_bins,
                       f_sc_tb_value, f_streetlight_element)
from csv import reader, writer
from numpy import array
from numpy import round as npround
from os.path import exists
from statistics import multimode, StatisticsError
import pandas as pd

def f_read_csv(f19_arch: str):
    try:
        f19_array: list = []

        with open(f19_arch, "r", encoding="utf-8-sig", newline="") as f19_f:
            f19_reader = reader(f19_f)
            for _ in f19_reader:
                f19_array.append([value for value in _ if value.strip()])

        return f19_array
    except Exception as e:
        return e


def f_element_pipeline(f20_element: list, f20_model, f20_input_size: int, f20_codes: list, f20_dict: dict,
                       f20_bins: list, f20_norm_list: list, f20_norm_values: list, f20_range_values: list,
                       f20_list_smart: list, f20_treshold_list: list):
    try:
        f20_sc: str
        f20_storage: str
        f20_time: str
        f20_storage_float: float
        f20_time_float: float
        f20_sc_norm: int
        f20_situation: str
        f20_error_code: str

        f20_list_variables: list = ["" for _ in range(f20_input_size)]
        if (len(f20_element) != f20_input_size+3) or (len(f20_element)<4):
            return "SIZE"
        for _ in range(len(f20_list_variables)):
            f20_list_variables[_] = f20_element[_]

        f20_sc, f20_storage, f20_time = f20_element[-3], f20_element[-2], f20_element[-1]
        f20_typecasting: tuple = f_typecast_element(f20_list_variables, f20_storage, f20_time)
        if f20_typecasting == "T":
            return "TYPE"

        f20_list_variables, f20_storage_float, f20_time_float = f20_typecasting
        f20_check_range: str = f_checks_element(f20_list_variables, f20_sc, f20_storage_float, f20_time_float,
                                                f20_codes, f20_norm_values, f20_range_values, f20_list_smart)
        if f20_check_range:
            return f"RANGE_{f20_check_range}"

        f20_list_variables, f20_sc_norm = f_normalization(f20_list_variables, f20_sc, f20_norm_list)
        f20_numpy_array = array(f20_list_variables).reshape(1, -1)
        f20_preds: float = float(npround(f20_model.predict(f20_numpy_array, verbose=0), 4)[0][0] * 100)
        f20_preds: float = round(f20_preds, 2)
        f20_storage_int: int = f_storage_bins(f20_storage_float, f20_bins)
        f20_combination: float = f_sc_tb_value(f20_sc_norm, f20_storage_int, f20_dict)
        if f20_combination == 0:
            return f"ZERO"
        f20_ttf: float = round(f20_combination-(f20_time_float % f20_combination), 2)
        f20_result_array: tuple = f_streetlight_element(f20_preds, f20_list_variables, f20_ttf, f20_treshold_list)

        f20_situation, f20_ttf, f20_error_code = f20_result_array
        return f20_situation, f20_preds, f20_ttf, f20_error_code
    except Exception as e:
        return f"ERROR_{e}"


def f_naming(f18_direc: str, f18_name: str):
    f18_name: str = f18_name.split(".")[0]

    counter: int = 1
    if exists(f"{f18_direc}/{f18_name}.csv"):
        name_pdf: str = f"{f18_direc}/{f18_name}.csv"
        while exists(name_pdf):
            name_pdf: str = f"{f18_direc}/{f18_name}_{str(counter)}.csv"
            counter += 1
    else:
        name_pdf: str = f18_direc + "/" + f18_name + ".csv"

    return name_pdf


def f_write_csv(f21_dest_path: str, f21_array_results: list):
    with open(f21_dest_path, "w", newline="") as f16_f:
        f16_writer = writer(f16_f)
        for _ in f21_array_results:
            if isinstance(_, str):
                f16_writer.writerow([_])
            else:
                f16_writer.writerow(_)


def f_generate_df_stats(f25_array_input: list, f25_array_output: list):
    try:
        f25_joined_array: list = []
        for _ in range(len(f25_array_output)):
            # Problemas con la lectura de csv. Por eso se debe de hacer esta declaración previa.
            if (f25_array_output[_][0] == "F") or (f25_array_output[_][0] == "A") or (f25_array_output[_][0] == "N"):
                f25_aux = []
                for __ in range(len(f25_array_input[_])-2):
                    f25_aux.append(f25_array_input[_][__])
                f25_aux.append(f25_array_output[_][0])
                f25_aux.append(f25_array_output[_][1])
                f25_aux.append(f25_array_output[_][3])
                f25_joined_array.append(f25_aux)
        f25_unique_codes: set = set(_[3] for _ in f25_joined_array)
        f25_classified_data: dict = {_: [] for _ in sorted(f25_unique_codes)}
        for _ in f25_joined_array:
            f25_classified_data[_[3]].append(_)
        f25_dataframes: dict = {}
        for _, __ in f25_classified_data.items():
            f25_dataframes[_] = pd.DataFrame(__)

        return f25_dataframes
    except Exception as e:
        print(e)
        return None


def f_statistics(f26_df):
    f26_avgs: list = []
    for _ in range(f26_df.shape[1] - 4):
        f26_df.iloc[:, _] = pd.to_numeric(f26_df.iloc[:, _], errors="coerce")
        f26_avgs.append(round(f26_df.iloc[:, _].mean(), 1))

    f26_df.iloc[:, -2] = pd.to_numeric(f26_df.iloc[:, -2], errors="coerce")
    f26_promedio_probabilidad: float = round(f26_df.iloc[:, -2].mean(), 1)

    f26_counts = f26_df.iloc[:, -3].value_counts(normalize=True)

    f26_df["Character_Extraction"] = f26_df.iloc[:, -1].apply(f_regex_code)
    f26_df_codes= f26_df[["Character_Extraction"]].copy()
    f26_df_codes = f26_df_codes[f26_df_codes["Character_Extraction"].notna()]
    f26_df_codes = f26_df_codes[f26_df_codes["Character_Extraction"] != "0"]

    try:
        f26_moda_codigo: list = multimode(f26_df_codes["Character_Extraction"])
    except StatisticsError:
        f26_moda_codigo: list = []

    return (*f26_avgs, round(f26_counts.get("N", 0), 2), round(f26_counts.get("A", 0), 2),
            round(f26_counts.get("F", 0), 2), f26_promedio_probabilidad, f26_moda_codigo)


def f_matplotlib_image(f34_df_values, f34_fig, f34_gs, f34_stats_list: list, f34_bar_labels: list,
                       f34_text_indicators: list, f34_text_x: float, f34_text_y: float,  f34_spacing: float,
                       f34_list_colors: list, f16_plt_params_pers: tuple):
    f34_ha1: str
    f34_va1: str
    f34_fontsize1: int
    f34_fontweight1: str
    f34_facecolor: str
    f34_edgecolor: str
    f34_ha2: str
    f34_va2: str
    f34_fontsize2: int
    f34_title: str
    f34_fontsize3: int
    f34_fontweight2: str
    f34_axis: str
    f34_linestyle: str
    f34_alpha: float

    (f34_ha1, f34_va1, f34_fontsize1, f34_fontweight1, f34_facecolor, f34_edgecolor, f34_ha2, f34_va2, f34_fontsize2,
     f34_title, f34_fontsize3, f34_fontweight2, f34_axis, f34_linestyle, f34_alpha) = f16_plt_params_pers

    f34_array: list = f34_stats_list[f34_df_values]
    f34_label: str = f34_array[0]
    f34_bar_values: list = list(map(float, f34_array[-5:-2]))

    f34_ax_text = f34_fig.add_subplot(f34_gs[f34_df_values*2])
    f34_ax_text.axis("off")
    f34_texts: list = []
    for __ in range(1, len(f34_array)-5):
        f34_texts.append(f"{f34_text_indicators[__-1]} {f34_array[__]}")
    f34_texts.append(f"{f34_text_indicators[-2]} {f34_array[-2]}")
    f34_texts.append(f"{f34_text_indicators[-1]} {', '.join(f'{item}' for item in f34_array[-1])}")
    f34_ax_text.text(f34_text_x, f34_text_y, f34_label, ha=f34_ha1, va=f34_va1, fontsize=f34_fontsize1,
                     fontweight=f34_fontweight1,
                 bbox=dict(facecolor=f34_facecolor, edgecolor=f34_edgecolor))
    for __, ___ in enumerate(f34_texts):
        f34_ax_text.text(f34_text_x, f34_text_y-(__+1)*f34_spacing, ___, ha=f34_ha2, va=f34_va2, fontsize=f34_fontsize2)

    f34_ax_bar = f34_fig.add_subplot(f34_gs[1+f34_df_values*2])
    f34_ax_bar.bar(f34_bar_labels, f34_bar_values, color=f34_list_colors)
    f34_ax_bar.set_ylim(0, max(f34_bar_values)*1)
    f34_ax_bar.set_title(f34_title, fontsize=f34_fontsize3, fontweight=f34_fontweight2)
    f34_ax_bar.grid(axis=f34_axis, linestyle=f34_linestyle, alpha=f34_alpha)


def f_naming_jpg(f36_direc: str, f36_name: str):
    f36_name: str = f36_name.split(".")[0]

    f36_counter: int = 1
    if exists(f"{f36_direc}/{f36_name}.jpg"):
        f36_name_jpg: str = f"{f36_direc}/{f36_name}.jpg"
        while exists(f36_name_jpg):
            f36_name_jpg: str = f"{f36_direc}/{f36_name}_{str(f36_counter)}.jpg"
            f36_counter += 1
    else:
        f36_name_jpg: str = f36_direc + "/" + f36_name + ".jpg"

    return f36_name_jpg
