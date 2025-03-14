from ParametersCloud import f_parameters, f_parameters_matplotlib, f_parameters_matplotlib_personalizables
from BackendCloud import (f_read_csv, f_element_pipeline, f_naming, f_write_csv, f_generate_df_stats, f_statistics,
                          f_matplotlib_image, f_naming_jpg)
from datetime import datetime
from os import listdir
from os.path import abspath, basename
from queue import Queue
from sys import argv, exit
from threading import Thread
import matplotlib.pyplot as plt

gcp_input_size: int
gcp_entity_codes: list
gcp_storage_bins: list
gcp_dict_combinations: dict
gcp_norm_list: list
gcp_range_values_tb: list
gcp_code_smart: list
gcp_threshold_list: list
gcp_number_smart: int
gcp_bar_labels: list
gcp_text_indicators: list
gcp_text_x: float
gcp_text_y: float
gcp_spacing: float
gcp_list_colors: list
gcp_format_plt: str
gcp_dpi: int


def f_cheks_empty_batch(f30_input_dir: str, f30_output_dir: str):
    if f30_input_dir == "":
        exit("Por favor ingrese un directorio de entrada.")
    if f30_output_dir == "":
        exit("Por favor ingrese un directorio de salida.")
    return True


def f_processing_batch(f31_file_path: str, f31_model, f31_input_size: int, f31_codes: list, f31_dict:dict,
                       f31_bins:list, f31_norm_list: list, f31_norm_values: list, f31_range_values: list,
                       f31_list_smart: list, f31_treshold_list: list, f31_output_dir: str):
    try:
        f31_array: list = f_read_csv(f31_file_path)
        if not f31_array:
            return None
        f31_array_results: list = []
        for __ in f31_array:
            f31_array_results.append(f_element_pipeline(__, f31_model, f31_input_size, f31_codes, f31_dict,
                                                        f31_bins, f31_norm_list, f31_norm_values,
                                                        f31_range_values, f31_list_smart, f31_treshold_list))
        f31_dest_path: str = f_naming(f31_output_dir, basename(f31_file_path).removesuffix(".csv")
                                      + "_Output.csv")
        f_write_csv(f31_dest_path, f31_array_results)

        f31_dataframes: dict = f_generate_df_stats(f31_array, f31_array_results)
        f31_results_stats: list = []
        for __, ___ in f31_dataframes.items():
            f31_results_stats.append([__] + list(f_statistics(___)))
        f31_results_stats.append([datetime.now()])
        f31_stats_path: str = f_naming(f31_output_dir, basename(f31_file_path).removesuffix(".csv")
                                       +"_Stats.csv")
        f_write_csv(f31_stats_path, f31_results_stats)

        return None
    except Exception as e:
        return e


def f_threading_target(f32_counter2, f32_queue, f32_counter1, f32_model, f32_input_size: int, f32_codes: list,
                       f32_dict:dict, f32_bins:list, f32_norm_list: list, f32_norm_values: list, f32_range_values: list,
                       f32_list_smart: list, f32_treshold_list: list, f32_output_dir: str):
    f32_result: Exception|None = f_processing_batch(f32_counter2, f32_model, f32_input_size, f32_codes, f32_dict,
                                                    f32_bins, f32_norm_list, f32_norm_values, f32_range_values,
                                                    f32_list_smart, f32_treshold_list, f32_output_dir)
    if isinstance(f32_result, Exception):
        with open(f32_output_dir + "/" + basename(f32_counter2).removesuffix(".csv")[0] + "_Exception.txt", "w",
                  encoding="utf-8") as f:
            f.write(str(f32_result))
        f32_queue.put((f32_counter2, f32_result, f32_counter1))
        return None
    f32_queue.put((f32_counter2, f32_result, f32_counter1))
    return None


def f_fetch(f33_number_threads, f33_model, f33_input_size: int, f33_codes: list, f33_dict:dict, f33_bins:list,
            f33_norm_list: list, f33_norm_values: list, f33_range_values: list, f33_list_smart: list,
            f33_treshold_list: list, f33_output_dir: str):
    f33_threads = []
    f33_queue = Queue()
    f33_results = [None] * len(f33_number_threads)

    for _, __ in enumerate(f33_number_threads):
        f33_thread = Thread(target=f_threading_target,
                            args=(__, f33_queue, _, f33_model, f33_input_size, f33_codes, f33_dict, f33_bins,
                                  f33_norm_list, f33_norm_values, f33_range_values, f33_list_smart, f33_treshold_list,
                                  f33_output_dir))
        f33_threads.append(f33_thread)
        f33_thread.start()

    for thread in f33_threads:
        thread.join()

    while not f33_queue.empty():
        f33_file, f33_result, f33_index = f33_queue.get()
        f33_results[f33_index] = (f33_file, f33_result)

    return f33_results


def f_main_batch(f37_input_dir, f37_output_dir, f37_model, f37_input_size: int, f37_codes: list, f37_dict:dict ,
                 f37_bins:list, f37_norm_list: list, f37_norm_values: list, f37_range_values: list,
                 f37_list_smart: list, f37_treshold_list: list, f37_bar_labels: list, f37_text_indicators: list,
                 f37_text_x: float, f37_text_y: float, f37_spacing: float, f37_list_colors: list,
                 f37_plt_params_pers: tuple, f37_format_plt: str, f37_dpi: int):
    try:
        f16_cheks_empty: bool = f_cheks_empty_batch(f37_input_dir, f37_output_dir)
        if not f16_cheks_empty:
            return None
        f37_absolute_paths: list = [f37_input_dir + "/" + file for file in listdir(f37_input_dir)]
        f37_number_threads = [f for f in f37_absolute_paths if f.endswith(".csv")]
        f_fetch(f37_number_threads, f37_model, f37_input_size, f37_codes, f37_dict, f37_bins, f37_norm_list,
        f37_norm_values, f37_range_values, f37_list_smart, f37_treshold_list, f37_output_dir)

        for _ in listdir(f37_output_dir):
            if _.endswith("_Stats.csv"):
                try:
                    f37_results_stats = f_read_csv(f"{f37_output_dir}/{_}")
                    f37_fig = plt.figure(figsize=(8, 3.5*(len(f37_results_stats)-1)))
                    f37_gs = f37_fig.add_gridspec(len(f37_results_stats)-1, 2, width_ratios=[2, 2])
                    for __ in range(len(f37_results_stats)-1):
                        f_matplotlib_image(__, f37_fig, f37_gs, f37_results_stats, f37_bar_labels, f37_text_indicators,
                                           f37_text_x, f37_text_y, f37_spacing, f37_list_colors, f37_plt_params_pers)
                    plt.tight_layout()
                    f37_plt_path = f_naming_jpg(f37_output_dir, basename(_).removesuffix("_Stats.csv")+"_plt")
                    plt.savefig(f37_plt_path, format=f37_format_plt, dpi=f37_dpi)
                    plt.close(f37_fig)
                except Exception as e:
                    print(f"{e}. No se generarán archivos de gráficos para {_}")
                    continue

        print("Completado. Los archivos se ha generado.")
    except Exception as e:
        exit(f"Ocurrió un error. Por favor, inténtelo de nuevo. Si el error persiste, comuníquese con el desarrollador "
             f"con el siguiente código: {e}")
        return None

if __name__ == "__main__":
    if len(argv) != 3:
        exit("Uso: python PredictionsCloud.py <directorio_entrada> <directorio_salida>")

    gcp_input_directory = abspath(argv[1]).replace("\\", "/")
    gcp_output_directory = abspath(argv[2]).replace("\\", "/")

    gcp_bar_labels, gcp_text_indicators, gcp_text_x, gcp_text_y, gcp_spacing, gcp_list_colors, gcp_format_plt, gcp_dpi \
        = f_parameters_matplotlib()
    (gcp_model, gcp_input_size, gcp_entity_codes, gcp_storage_bins, gcp_dict_combinations, gcp_norm_list,
     gcp_range_values_tb, gcp_code_smart, gcp_threshold_list, gcp_number_smart) = f_parameters()
    gcp_plt_params_pers: tuple = f_parameters_matplotlib_personalizables()

    f_main_batch(gcp_input_directory, gcp_output_directory, gcp_model, gcp_input_size, gcp_entity_codes, gcp_dict_combinations,
                 gcp_storage_bins, gcp_norm_list, gcp_norm_list, gcp_range_values_tb, gcp_code_smart,
                 gcp_threshold_list, gcp_bar_labels, gcp_text_indicators, gcp_text_x, gcp_text_y, gcp_spacing,
                 gcp_list_colors, gcp_plt_params_pers, gcp_format_plt, gcp_dpi)
