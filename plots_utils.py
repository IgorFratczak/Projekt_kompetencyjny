import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Funkcja zapisująca wykres jako obraz

time_col - kolumna z czasem symulacji (oś x)
value_col - kolumna z daną wartością (oś y)
title - tytuł wykresu, domyślnie None
xaxis_label - nazwa dla osi x, domyślnie None
yaxis_label - nazwa dla osi y, domyślnie None
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
"""
def save_plot_as_image(time_col, value_col, title=None, xaxis_label=None, yaxis_label=None, filename : str = None, directory_name : str = ""):
    if filename is None:
        raise TypeError("filename cannot be empty!")

    plt.figure(figsize=(10, 5))
    plt.plot(time_col, value_col, linestyle='-', color='b')

    plt.xticks(np.linspace(time_col.min(), time_col.max(), 10))
    plt.yticks(np.linspace(value_col.min(), value_col.max(), 10))

    plt.xlabel(xaxis_label)
    plt.ylabel(yaxis_label)
    plt.grid(True)
    plt.tight_layout()
    full_path = os.path.join(directory_name, f"{filename}.png")
    plt.savefig(full_path)
    plt.close()
"""
Funkcja zapisująca wykresy dla poziomu zamknięcia lewego i prawego oka

data : pd.DataFrame - zbiór danych, musi zawierać unityGameTime, leftEyeClosedValue i rightEyeClosedValue
directory_name : str - nazwa katalogu, gdzie zostaną zapisane obrazy z wykresemami, domyślnie jest pusta (obecny katalog)
"""
def save_eye_closed_plots(data : pd.DataFrame, directory_name : str = ""):
    save_plot_as_image(data['unityGameTime'], data['leftEyeClosedValue'], "Zamknięcie lewego oka", "Czas [s]",
              "Zamknięcie lewego oka [%]", "left_eye_closed", directory_name)
    save_plot_as_image(data['unityGameTime'], data['rightEyeClosedValue'], 'Zamknięcie prawego oka', "Czas [s]",
              "Zamknięcie prawego oka [%]", "right_eye_closed", directory_name)

"""
Funkcja zapisująca wykresy dla poziomu uniesienia lewego i prawego policzka

data : pd.DataFrame - zbiór danych, musi zawierać unityGameTime, leftCheekRiseValue i rightCheekRiseValue
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
"""
def save_chicks_risen_plot(data : pd.DataFrame, directory_name : str = ""):
    save_plot_as_image(data['unityGameTime'], data['leftCheekRiseValue'], "Uniesienie lewego polika", "Czas [s]",
              "Uniesienie lewego polika [%]","left_cheek_rise", directory_name)
    save_plot_as_image(data['unityGameTime'], data['rightCheekRiseValue'], 'Uniesienie prawego polika', "Czas [s]",
              "Uniesienie prawego polika [%]", "right_cheek_rise", directory_name)

"""
Funkcja zapisująca wykresy dla poziomu uniesienia lewego i prawego kącika ust

data : pd.DataFrame - zbiór danych, musi zawierać unityGameTime, leftSmileValue i rightSmileValue
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
"""
def save_smile_plot(data : pd.DataFrame, directory_name : str = ""):
    save_plot_as_image(data['unityGameTime'], data['leftSmileValue'], "Uniesienie lewego koncika ust", "Czas [s]",
              "Uniesienie lewego koncika ust [%]", "left_smile", directory_name)
    save_plot_as_image(data['unityGameTime'], data['rightSmileValue'], 'Uniesienie prawego koncika ust', "Czas [s]",
              "Uniesienie prawego koncika ust [%]", "right_smile", directory_name)

"""
Funkcja zapisująca wykresy dla poziomu obniżenia lewego i prawego kącika ust

data : pd.DataFrame - zbiór danych, musi zawierać unityGameTime, leftLipCornerDepressor i rightLipCornerDepressor
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
"""
def save_lip_corner_depressor_plot(data : pd.DataFrame, directory_name : str = ""):
    save_plot_as_image(data['unityGameTime'], data['leftLipCornerDepressor'], "Obniżenie lewego koncika ust", "Czas [s]",
              "Obniżenie lewego koncika ust [%]", "left_lip_depressor", directory_name)
    save_plot_as_image(data['unityGameTime'], data['rightLipCornerDepressor'], 'Obniżenie prawego koncika ust', "Czas [s]",
              "Obniżenie prawego koncika ust [%]", "right_lip_depressor", directory_name)

"""
Funkcja zapisująca wykresy dla poziomu cofnięcia lewego i prawego kącika ust

data : pd.DataFrame - zbiór danych, musi zawierać unityGameTime, leftDimplerValue i rightDimplerValue
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
"""
def save_dimpler_plot(data : pd.DataFrame, directory_name : str = ""):
    save_plot_as_image(data['unityGameTime'], data['leftDimplerValue'], "Cofnięcie lewego koncika ust", "Czas [s]",
              "Cofnięcie lewego koncika ust [%]","left_dimpler", directory_name)
    save_plot_as_image(data['unityGameTime'], data['rightDimplerValue'], 'Cofnięcie prawego koncika ust', "Czas [s]",
              "Cofnięcie prawego koncika ust [%]", "right_dimpler", directory_name)

"""
Funkcja zapisująca wykresy dla poziomu uniesienia  lewej i prawej brwi

data : pd.DataFrame - zbiór danych, musi zawierać unityGameTime, leftInnerBrowRiseValue i rightInnerBrowRiseValue
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
"""
def save_inner_brow_rise_plot(data : pd.DataFrame, directory_name : str = ""):
    save_plot_as_image(data['unityGameTime'], data['leftInnerBrowRiseValue'], "Uniesienie lewej brwi", "Czas [s]",
              "Uniesienie lewej brwi [%]", "right_inner_brow_rise", directory_name)
    save_plot_as_image(data['unityGameTime'], data['rightInnerBrowRiseValue'], 'Uniesienie prawej brwi', "Czas [s]",
              "Uniesienie prawej brwi [%]", "left_inner_brow_rise", directory_name)

"""
Funkcja zapisująca wykresy dla poziomu zniżenia lewej i prawej

data : pd.DataFrame - zbiór danych, musi zawierać unityGameTime, leftBrowLowerValue i rightBrowLowerValue
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
"""
def save_lower_brow_plot(data : pd.DataFrame, directory_name : str = ""):
    save_plot_as_image(data['unityGameTime'], data['leftBrowLowerValue'], "Zniżenie wewnętrznej częsci lewej brwi", "Czas [s]",
              "Zniżenie wewnętrznej częsci lewej brwi [%]", "left_brow_lower", directory_name)
    save_plot_as_image(data['unityGameTime'], data['rightBrowLowerValue'], 'Zniżenie wewnętrznej częsci prawej brwi', "Czas [s]",
              "Zniżenie wewnętrznej częsci prawej brwi [%]", "right_brow_lower", directory_name)

"""
Funkcja zapisująca wykresy dla poziomu zmrużenia lewego i prawego oka

data : pd.DataFrame - zbiór danych, musi zawierać unityGameTime, leftLidTightnerValue i rightLidTightnerValue
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
"""
def save_lid_tightener_plot(data : pd.DataFrame, directory_name : str = ""):
    save_plot_as_image(data['unityGameTime'], data['leftLidTightnerValue'], "Zmrużenie lewego oka", "Czas [s]",
              "Zmrużenie lewego oka [%]", "left_lid_tightner", directory_name)
    save_plot_as_image(data['unityGameTime'], data['rightLidTightnerValue'], 'Zmrużenie prawego oka', "Czas [s]",
              "Zmrużenie prawego oka [%]", "right_lid_tightner", directory_name)

"""
Funkcja zapisująca wykresy dla poziomu rozszerzenia lewego i prawego oka

data : pd.DataFrame - zbiór danych, musi zawierać unityGameTime, leftLidRiserValue i rightLidRiserValue
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
"""
def save_lid_rise_plot(data : pd.DataFrame, directory_name : str = ""):
    save_plot_as_image(data['unityGameTime'], data['leftLidRiserValue'], "Rozszerzenie lewego oka", "Czas [s]",
              "Rozszerzenie lewego oka [%]", "left_lid_riser", directory_name)
    save_plot_as_image(data['unityGameTime'], data['rightLidRiserValue'], 'Rozszerzenie prawego oka', "Czas [s]",
              "Rozszerzenie prawego oka [%]", "right_lid_riser", directory_name)

"""
Funkcja zapisująca wykresy dla poziomu opuszczenia szczęki

data : pd.DataFrame - zbiór danych, musi zawierać unityGameTime i jawDropValue
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
"""
def save_jaw_drop_plot(data : pd.DataFrame, directory_name : str = ""):
    save_plot_as_image(data['unityGameTime'], data['jawDropValue'], "Opuszczenie szczęki", "Czas [s]",
              "Opuszczenie szczęki [%]", "jaw_drop", directory_name)

"""
Funkcja zapisująca wykres kołowy występowania emocji

data : pd.DataFrame - słownik z danymi o emocjach
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
title : str - nazwa wykresu, domyślnie brak
filename : str - nazwa dla zdjęcia wykresu
"""
def save_emotion_plot(data, directory_name : str = "", title : str = "", filename : str = ""):
    label_translation = {
        'natural': 'naturalny',
        'happy': 'wesoły',
        'sad': 'smutny',
        'surprised': 'zaskoczony',
        'disturbed': 'wystraszony'
    }

    emotions_filtered = {k: v for k, v in data.items() if v > 0}
    labels_en = list(emotions_filtered.keys())
    sizes = list(emotions_filtered.values())
    total = sum(sizes)

    legend_labels = [
        f"{label_translation[k]} ({emotions_filtered[k] / total:.1%})"
        for k in labels_en
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, _ = ax.pie(
        sizes,
        startangle=140,
        labels=None,
    )

    ax.legend(wedges, legend_labels, title="Emocje", loc="center left", bbox_to_anchor=(1, 0.5))

    plt.tight_layout()
    full_path = os.path.join(directory_name, f"{filename}.png")
    plt.savefig(full_path)
    plt.close()

"""
Funckja zapisująca wszystkie wykresy kołowe emocji dla każdej z procedur i dla całej symulacji

data : pd.DataFrame - słownik z danymi o emocjach
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
"""
def save_all_emotions_plots(data, directory_name : str = ""):
    save_emotion_plot(data['normal'], directory_name, "Wykres emocji podczas spokojnego lotu", "flight_normal")
    save_emotion_plot(data['starting'], directory_name, "Wykres emocji podczas procedury startu", "flight_start")
    save_emotion_plot(data['turbulence'], directory_name, "Wykres emocji podczas turbulencji", "flight_turbulence")
    save_emotion_plot(data['landing'], directory_name, "Wykres emocji podczas procedury lądowania", "flight_landing")
    save_emotion_plot(data['all'], directory_name, "Wykres emocji podczas całego lotu", "flight")

"""
Funkcja zapisująca wykresy dla danych

data : pd.DataFrame - data
directory_name : str - nazwa katalogu, gdzie zostanie zapisany obraz z wykresem, domyślnie jest pusta (obecny katalog)
"""
def save_all_plots(data : pd.DataFrame, directory_name : str = ""):
    save_eye_closed_plots(data, directory_name)
    save_chicks_risen_plot(data, directory_name)
    save_smile_plot(data, directory_name)
    save_dimpler_plot(data, directory_name)
    save_inner_brow_rise_plot(data, directory_name)
    save_lower_brow_plot(data, directory_name)
    save_lid_tightener_plot(data, directory_name)
    save_lid_rise_plot(data, directory_name)
    save_jaw_drop_plot(data, directory_name)
    save_lip_corner_depressor_plot(data, directory_name)

