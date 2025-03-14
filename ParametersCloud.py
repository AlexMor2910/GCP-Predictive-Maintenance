from keras import models
from sys import exit


def f_error_code(f14_list_vars: list):
    f14_sut: float
    f14_rue: float
    f14_temp: float

    f14_sut, f14_rue, f14_temp = f14_list_vars

    if f14_rue < 0.3:
        return "187"
    if f14_rue < 0.4:
        if f14_temp > 0.1:
            if f14_sut > 0.95:
                return "3.194.187"
            return "194.187"
        return "187"
    if f14_rue < 0.5:
        if f14_temp > 0.2:
            return "194.187"
        return "187"
    if f14_rue < 0.6:
        if f14_temp > 0.2:
            if f14_sut > 0.95:
                return "3.194.187"
            return "194.187"
        return "187"
    if f14_rue < 0.7:
        if f14_temp > 0.3:
            return "194.187"
        return "187"
    if f14_rue < 0.8:
        if f14_temp > 0.4:
            return "194.187"
        return "187"
    if f14_rue < 0.9:
        if f14_temp > 0.4:
            return "194.187"
        return "187"
    if f14_rue < 0.95:
        if f14_temp > 0.5:
            return "194.187"
        return "187"

    if f14_temp > 0.5:
        if (f14_sut > 0.1) and (f14_sut < 0.8):
            return "3.194.187"
        return "194.187"

    if (f14_sut < 0.1) or (f14_sut > 0.8):
        return "3.187"

    return "187"


def f_parameters():
    try:
        f27_model = models.load_model("model.keras", compile=False)
        f27_config = f27_model.get_config()
        f27_input_size: int = f27_config["layers"][0]["config"]["batch_shape"][1]

        f27_entity_codes: list[str] = ["ams5", "iad1", "phx1", "sac0", "sac2"]
        f27_storage_bins: list[float] = [4.4, 8.3, 12.2, 16.1]
        f27_code_combinations: dict = {
            "0_0": 49.72, "0_1": 8.09, "0_2": 7.17, "0_3": 2.10, "0_4": 15.01,
            "1_0": 25.92, "1_1": 4.24, "1_2": 2.41, "1_3": 0.60, "1_4": 9.71,
            "2_0": 10.12, "2_1": 0.51, "2_2": 0.66, "2_3": 0.56, "2_4": 0.31,
            "3_0": 1.06, "3_1": 0.89, "3_2": 0.48, "3_3": 1.43, "3_4": 1.03,
            "4_0": 42.78, "4_1": 6.36, "4_2": 2.68, "4_3": 1.17, "4_4": 6.52}
        if (len(f27_entity_codes)*(len(f27_storage_bins)+1)) != len(f27_code_combinations):
            exit("El diccionario de combinaciones no tiene el tamaño correcto.")
            return None

        f27_number_smart: int = 3
        f27_code_smart: list[str] = ["3", "187", "194"]
        if (f27_number_smart != f27_input_size) or (len(f27_code_smart) != f27_input_size):
            exit("Favor de verificar que el número de nodos de entrada sea el mismo que el número de variables SMART, e "
                 "igual al número de códigos SMART.")
            return None

        f27_normalization_values: list = [[0, 255], [0, 100], [0, 255],
                                      [{'ams5': 0, "iad1": 1, "phx1": 2, "sac0": 3, "sac2": 4}]]
        f27_range_values_tb: list[float] = [0.5, 20]
        if len(f27_normalization_values) != (f27_number_smart+1):
            exit("La lista de valores de normalización no tiene el tamaño correcto.")
            return None

        f27_treshold_list: list[float] = [35, 85]
        if len(f27_treshold_list) != 2:
            exit("Favor de insertar al menos dos parámetros como delimitadores.")
            return None

        return (f27_model, f27_input_size, f27_entity_codes, f27_storage_bins, f27_code_combinations,
                f27_normalization_values, f27_range_values_tb, f27_code_smart, f27_treshold_list, f27_number_smart)
    except Exception as e:
        exit(f"Por favor verifique que todos los datos sean correctos en el archivo Parameters.py. Código de error: "
             f"{e}")
        return None


def f_parameters_matplotlib():
    f35_bar_labels: list[str] = ['N', 'A', 'F']
    f35_text_indicators: list[str] = ["Promedio errores reportados no corregibles:", "Promedio temperatura [°C]:",
                       "Promedio tiempo spin-up [ms]:", "Posibilidad de fallo promedio:", "Código más común:"]
    f35_text_x: float = 0.02
    f35_text_y: float = 0.9
    f35_spacing: float = 0.25
    f35_list_colors: list[str] = ['green', 'yellow', 'red']
    f35_format: str = "jpg"
    f35_dpi: int = 300
    if len(f35_list_colors) != len(f35_bar_labels):
        exit("Favor de ingresar un número correcto de colores para la gráfica de barras.")

    return (f35_bar_labels, f35_text_indicators, f35_text_x, f35_text_y, f35_spacing, f35_list_colors, f35_format,
            f35_dpi)


def f_parameters_matplotlib_personalizables():
    f50_ha1: str = "left"
    f50_va1: str = "center"
    f50_fontsize1: int = 12
    f50_fontweight1: str = "bold"
    f50_facecolor: str = "cyan"
    f50_edgecolor: str = "black"
    f50_ha2: str = "left"
    f50_va2: str = "center"
    f50_fontsize2: int = 10
    f50_title: str = "Proporción"
    f50_fontsize3: int = 12
    f50_fontweight2: str = "bold"
    f50_axis: str = "y"
    f50_linestyle: str = "-"
    f50_alpha: float = 0.4

    if (f50_fontsize1 < 1) or (f50_fontsize2 < 1) or (f50_fontsize3 < 1):
        exit("Favor de ingresar tamaños de letra válidos para los gráficos en matplotlib.")

    if (f50_alpha < 0) or (f50_alpha > 1):
        exit("Favor de ingresar un valor de alpha válido para los gráficos en matplotlib.")

    return (f50_ha1, f50_va1, f50_fontsize1, f50_fontweight1, f50_facecolor, f50_edgecolor, f50_ha2, f50_va2,
            f50_fontsize2, f50_title, f50_fontsize3, f50_fontweight2, f50_axis, f50_linestyle, f50_alpha)
