import json
import os

import joblib
import pandas as pd

from generate_report.content_html import generate_index_html
from generate_report.plots_utils import save_all_plots, save_all_emotions_plots

"""
Funkcja tworząca katalog, jeżeli nie istnieje

directory_name : str - nazwa katalogu
"""
def create_directory(directory_name : str):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Stworzono katalog: {directory_name}")
    else:
        print(f"Katalog: {directory_name} już istnieje")

"""
Funkcja analizująca ilość mrugnięć, ilość mrugnięć na minute dla całej symulacji i dla poszczególnych procedur.
Zlicza i zapisuje okresy czasu kiedy oczy były zamknięte.

data - dane
time_stats - słownik z danymi na temat procedr i ich okresach występowania
"""
def analyze_eye_movements(data: pd.DataFrame, time_stats: dict):
    """
    Inicjalizacja pustego słownika
    """
    results = {
        'blinking': {
            'count': 0,
            "mean": 0.0,
            "mean_per_minute_start": 0.0,
            "mean_per_minute_landing": 0.0,
            "mean_per_minute_turbulence": 0.0,
            "mean_per_minute_normal": 0.0
        },
        'closed_eyes': {
            'count': 0,
            'time_stamps': []
        }
    }
    """
    Sprawdzenie czy dane istnieją
    """
    if data.empty:
        return results

    """
    Warunek na zamknięcie oka
    """
    is_closed = (data['rightEyeClosedValue'] > 0.5) | (data['leftEyeClosedValue'] > 0.5)

    """
    Przypisanie początkwych wartości przed analizą
    """
    eye_state = 'OPEN'
    closure_start_time = 0.0
    closure_start_index = 0
    all_closure_events = []

    """
    Wyszukiwanie przedziałów czasu, w ktorych oczy były zamknięte i zapisanie ich początku, końca, 
    czasu trwania i w jakiej procedurze się wydarzyły
    """
    for i in range(len(data)):
        is_closed_now = is_closed.iloc[i]
        current_time = data['unityGameTime'].iloc[i]

        if eye_state == 'OPEN' and is_closed_now:
            eye_state = 'CLOSED'
            closure_start_time = current_time
            closure_start_index = i
        elif eye_state == 'CLOSED' and not is_closed_now:
            eye_state = 'OPEN'
            end_time = current_time
            duration = end_time - closure_start_time
            flag = data['flag'].iloc[closure_start_index]

            all_closure_events.append({
                'start': closure_start_time,
                'end': end_time,
                'duration': duration,
                'flag': flag
            })

    """
    Sprawdzenie czy przy zakończeniu symulacji oczy nie były zamkniete, jeżeli były
    to dodaje kolejny przedział czasu
    """
    if eye_state == 'CLOSED':
        end_time = data['unityGameTime'].iloc[-1]
        duration = end_time - closure_start_time
        flag = data['flag'].iloc[closure_start_index]
        all_closure_events.append({
            'start': closure_start_time,
            'end': end_time,
            'duration': duration,
            'flag': flag
        })

    """
    Inicjalizacja słownika do zliczania mrugnięć dla danej procedury
    """
    blink_counts_by_phase = {0: 0, 1: 0, 2: 0, 3: 0}

    """
    Sprawdzenie dla każdego z przedziału czy były zamknięte oczy (przedziały z ponad 1 sekundowym okresem czasu),
    czy może to samo mrugnięcie. I zapisanie do głownego słownika w przypadku zamkniętych oczu,
    albo do tymczasowego słownika z ilością mrugnięć dla procedur, oraz inkrementowanie licznika mrugnięć w głównym słowniku.
    """
    for event in all_closure_events:
        if event['duration'] > 1.0:
            results['closed_eyes']['count'] += 1
            results['closed_eyes']['time_stamps'].append({
                'start': round(event['start'], 3),
                'end': round(event['end'], 3),
                'duration': round(event['duration'], 3)
            })
        else:
            results['blinking']['count'] += 1
            flag = event['flag']
            if flag in blink_counts_by_phase:
                blink_counts_by_phase[flag] += 1

    """
    Słownik z nazwami key dla głównego słownika w celu szybkiego przypisania wartości z tymczasowego słownika z zbiorem mrugnięć.
    """
    flag_map = {1: 'start', 3: 'landing', 2: 'turbulence', 0: 'normal'}

    """
    Zapisanie ilości mrugnięć dla danej procedury oraz wyliczenie, oraz wyliczanie mrugnięć na minute dla każdej z procedur
    """
    for flag_code, phase_name in flag_map.items():
        phase_duration_sec = time_stats[f'{phase_name}_duration']
        blink_count = blink_counts_by_phase[flag_code]

        if phase_duration_sec > 0:
            mean_blinks = (blink_count / phase_duration_sec) * 60
            results['blinking'][f'mean_per_minute_{phase_name}'] = round(mean_blinks, 2)

    """
    Pobranie czasu trwania symulacji i ilości mrugnięć podczas symulacji
    """
    total_duration_sec = time_stats['duration']
    total_blinks = results['blinking']['count']

    """
    Sprawdzenie czy symulacja trwała więcej niż 0 sekund, i obliczenie dla niej średniej wartości mrugnięć na minute.
    """
    if total_duration_sec > 0:
        overall_mean_blinks = (total_blinks / total_duration_sec) * 60
        results['blinking']['mean'] = round(overall_mean_blinks, 2)

    """
    Zwracanie słownika z danymi
    """
    return results

"""
Funckja zmieniająca "," na "." w zbiorze danych

data - zbiór danych 
"""
def replace_comma_with_dot(data: pd.DataFrame):
    """
    Sprawdzenie czy zbiór danych istnieje
    """
    if data.empty:
        raise Exception("Dane są puste")

    """
    Dla każdej kolumny zawierającej liczbe z "," na typ numeryczny z "."
    """
    for col in data.columns:
        if data[col].dtype == 'object':
            data[col] = pd.to_numeric(data[col].str.replace(',', '.', regex=False), errors='coerce')

"""
Funkcja zliczająca wystąpienia emocji w podczas symulacji

data - zbiór danych
"""
def count_emotions(data: pd.DataFrame):
    """
    Słownik zawierający rodzaje procedur symulacji
    """
    flag_map = {
        0: 'normal',
        1: 'starting',
        2: 'turbulence',
        3: 'landing'
    }

    """
    Zlicza wystąpiejnia emocji dla danych procedur symulacji
    """
    counts = data.groupby(['flag', 'label']).size()

    """
    Inicjalizacja słownika zawierającego słowniki dla emocji dla procedur, oraz dla całej symulacji
    """
    emotions = {
        'starting': {'natural': 0, 'happy': 0, 'sad': 0, 'surprised': 0, 'disturbed': 0},
        'turbulence': {'natural': 0, 'happy': 0, 'sad': 0, 'surprised': 0, 'disturbed': 0},
        'landing': {'natural': 0, 'happy': 0, 'sad': 0, 'surprised': 0, 'disturbed': 0},
        'normal': {'natural': 0, 'happy': 0, 'sad': 0, 'surprised': 0, 'disturbed': 0},
        'all': {'natural': 0, 'happy': 0, 'sad': 0, 'surprised': 0, 'disturbed': 0}
    }

    """
    Dla każdej z wartości z zgrupowanych danych, zostaje ona przypisana do odpowiedniego pola w głownym słowniku, 
    oraz zlicza wystąpienia emocji dla całej symulacji 
    """
    for (flag, label), count in counts.items():
        phase_name = flag_map.get(flag)
        if phase_name and label in emotions[phase_name]:
            emotions[phase_name][label] = count
            emotions['all'][label] += count

    """
    Zwraca słownik z emocjami dla procedur i całej symulacji
    """
    return emotions

"""
Funkcja zapoisująca dane do pliku JSON

data - dane do zapisania
filename - nazwa pliku, bądz nazwa wraz z ścieżką
"""
def export_to_json(data, filename : str):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Dane zostały pomyślnie zapisane do pliku: {filename}")

"""
Funkcja zliczająca długość trwania poszczególnych procedur, oraz ich okres czasu występowania w symulacji 

data - zbiór danych
"""
def calculate_time_statistics(data: pd.DataFrame):

    """
    Jeżeli zbiór danych jest pusty zwraca pusty słownik
    """
    if data.empty:
        return {
            'duration': 0.0, 'start_duration': 0.0, 'landing_duration': 0.0,
            'turbulence_duration': 0.0, 'normal_duration': 0.0,
            'start': [], 'normal': [], 'turbulence': [], 'landing': []
        }

    """
    Słownik zawirający nazwy procedur, kluczami są odpowiadające dane z kolumny flag
    """
    flag_map = {
        0: 'normal',
        1: 'start',
        2: 'turbulence',
        3: 'landing'
    }

    """
    Inicjacja pustego słownika z danymi o długości trwania danej procedury, oraz z okresami wystąpień ich w symulacji
    """
    time_stats = {
        'duration': 0.0,
        'start_duration': 0.0,
        'landing_duration': 0.0,
        'turbulence_duration': 0.0,
        'normal_duration': 0.0,
        'start': [],
        'normal': [],
        'turbulence': [],
        'landing': []
    }

    """
    Przypisanie pierwszej flagi odpowiadającej procedurze z zbioru danych,
    oraz przypisanie czasu początku symulacji.
    """
    current_flag = data['flag'].iloc[0]
    start_time_of_current_phase = data['unityGameTime'].iloc[0]

    """
    Wyliczanie okresów dla procedur, i dodawanie ich do głównego słownika
    """
    for i in range(1, len(data)):
        new_flag = data['flag'].iloc[i]

        if new_flag != current_flag:
            end_time = data['unityGameTime'].iloc[i - 1]
            phase_name = flag_map.get(current_flag)

            if phase_name:
                interval_duration = end_time - start_time_of_current_phase
                time_stats[f'{phase_name}_duration'] += interval_duration

                interval_dict = {
                    "start": round(start_time_of_current_phase, 3),
                    "end": round(end_time, 3),
                    "duration": round(interval_duration, 3)
                }
                time_stats[phase_name].append(interval_dict)

            current_flag = new_flag
            start_time_of_current_phase = data['unityGameTime'].iloc[i]

    """
    Przypisanie wartości o czasie z ostatniego rekordu z zbioru danych, oraz przypisanie obecnej flagi
    """
    end_time = data['unityGameTime'].iloc[-1]
    phase_name = flag_map.get(current_flag)

    """
    Wyliczanie okresu procedury z końca symulacji i zapis jej do głównego słownika 
    """
    if phase_name:
        interval_duration = end_time - start_time_of_current_phase
        time_stats[f'{phase_name}_duration'] += interval_duration

        final_interval_dict = {
            "start": round(start_time_of_current_phase, 3),
            "end": round(end_time, 3),
            "duration": round(interval_duration, 3)
        }
        time_stats[phase_name].append(final_interval_dict)

    """
    Przypisanie wartości czasu trwania symulacji do głównego słownika
    """
    time_stats['duration'] = round(data['unityGameTime'].iloc[-1], 3)

    """
    Zaokrąglanie wartości czasu trwania poszczególnych procedur do liczby z maksymalnie 3 miejscami po przecinku
    """
    for key in ['start_duration', 'landing_duration', 'turbulence_duration', 'normal_duration']:
        time_stats[key] = round(time_stats[key], 3)

    """
    Zwracanie słownika z informacjami o procedurach w trakcie symulacji
    """
    return time_stats

"""
Funkcja rozpoznająca ruch oczu i zapisująca te dane

data - zbiór danych
"""
def detect_eye_rotation(data: pd.DataFrame):
    """
    Przypisanie wartości ilości wierszy w zbiorze danych
    """
    num_rows = data.shape[0]

    """
    Flaga mówiąca czy patrzył się w górę
    """
    is_up = (data['rightEyeUpValue'] > 0.5) & (data['leftEyeUpValue'] > 0.5)

    """
    Flaga mówiąca czy patrzył się w dół
    """
    is_down = (data['rightEyeDownValue'] > 0.5) & (data['leftEyeDownValue'] > 0.5)

    """
    Flaga mówiąca czy patrzył się w prawo
    """
    is_right = (data['rightEyeRightValue'] > 0.5) & (data['leftEyeRightValue'] > 0.5)

    """
    Flaga mówiąca czy patrzył się w lewo
    """
    is_left = (data['rightEyeLeftValue'] > 0.5) & (data['leftEyeLeftValue'] > 0.5)

    """
    Flaga mówiąca czy patrzył się w górę i bez rozglądania na lewo i prawo
    """
    is_v_center = ~is_up & ~is_down

    """
    Flaga mówiąca czy patrzył się w dół i bez rozglądania na lewo i prawo
    """
    is_h_center = ~is_right & ~is_left

    """
    Słownik z wartościami odpowiadającymi gdzie patrzył się podczas całej symulacji
    """
    counts = {
        'upper_right': (is_up & is_right).sum(),
        'upper_left': (is_up & is_left).sum(),
        'upper_center': (is_up & is_h_center).sum(),

        'right': (is_v_center & is_right).sum(),
        'left': (is_v_center & is_left).sum(),
        'center': (is_v_center & is_h_center).sum(),

        'bottom_right': (is_down & is_right).sum(),
        'bottom_left': (is_down & is_left).sum(),
        'bottom_center': (is_down & is_h_center).sum(),
    }

    """
    Przypisanie głównemu słownikowi odpowiadających wartości
    """
    if num_rows > 0:
        final_proportions = {key: round(value / num_rows * 100, 2) for key, value in counts.items()}
    else:
        final_proportions = {key: 0 for key in counts.keys()}

    """
    Zwraca słownik z wartościami rotacji oczu
    """
    return final_proportions

"""
Kolumny z zbioru danych brane pod uwage przy predykcji emocji
"""
columns_to_predict = ['rightCheekRiseValue', 'leftCheekRiseValue', 'rightSmileValue',
                      'leftSmileValue', 'rightDimplerValue', 'leftDimplerValue',
                      'leftBrowLowerValue', 'rightBrowLowerValue', 'leftInnerBrowRiseValue',
                      'rightInnerBrowRiseValue', 'leftLidTightnerValue', 'rightLidTightnerValue',
                      'jawDropValue', 'leftLidRiserValue', 'rightLidRiserValue', 'leftLipCornerDepressor',
                      'rightLipCornerDepressor']

"""
Funkcja zamieniająca nazwe katalogu na odpowiadającą mu date i czas
"""
def create_title(text : str):
    split_date_and_time = text.split('_')
    split_date = split_date_and_time[0].split('-')
    split_time = split_date_and_time[1].split('-')

    return f'{split_date[2]}/{split_date[1]}/{split_date[0]} {split_time[0]}:{split_time[1]}:{split_time[2]}'
"""
Funkcja generująca raport z badania w formie pliku html.
Zapisuje wykresy do folderu odpowiadającego dacie i czasie pliku z danymi,
w folderze plots, zapisuje również plik JSON zawierający informacje o mruganiu, zamknięciu oczu, 
emocjach i procedurach w trakcie symulacji, również w folderze plots
Kożysta z wcześniej wytrenowanego modelu do predykcji

filename - nazwa pliku z danymi
"""
def generate_report(filename):
    """
    Sprawdzenie czy podana nazwa pliku nie jest pustym stringiem bądz None
    W przypadku podania błędnego parametru wywołuje wyjątek i kończy działanie
    """
    if filename.strip() == "" or filename is None:
        raise ValueError("Brak pliku z danymi!")

    """
    Pobranie ścieżki do pliku z danymi
    """
    base_name = os.path.basename(filename)

    """
    Tworzy nazwę do katalogu, w którym mają zostac zapisane dane z raportu.
    Robi to na podstawie daty i czasu z nazwy pliku z danymi
    (FaceData_01-01-2000_00-00-00.csv -> 01-01-2000_00_00-00)
    """
    report_dir_name = base_name.replace('FaceData_', '').replace('.csv', '')

    """
    Tworzenie katalogu dla danych
    """
    create_directory(report_dir_name)

    """
    Tworzenie ścieżki do katalogu plots w folderze na dane
    """
    plots_dir_path = os.path.join(report_dir_name, 'plots')

    """
    Tworzenie katalogu plots w folderze na dane
    """
    create_directory(plots_dir_path)

    """
    Wczytanie danych z pliku z danymi
    """
    data = pd.read_csv(filename, sep=";")
    print(f"Wczytano dane z pliku {filename}")
    """
    Zamiana "," na "." w zbiorze danych 
    """
    replace_comma_with_dot(data)

    """
    Zamiana wartości w kolumnie odpowiadającej za czas symulacji, poniewarz czas liczy sie zanim skrypt wystartuje.
    """
    data['unityGameTime'] = data['unityGameTime'] - data['unityGameTime'].iloc[0]

    """
    Wczytujemy model do predyckji emocji wraz z koderem etykiet
    """
    labels_encoder = joblib.load('label_encoder.joblib')
    model = joblib.load('model.joblib')

    """
    Wyłuskanie potrzebnych danych do predyckji emocji  ze zbioru danych 
    """
    data_to_predict = data[columns_to_predict]

    """
    Predyckja emocji
    """
    print("Rozpoznawanie emocji...")
    predictions = model.predict(data_to_predict)

    """
    Odkodywanie etykiet z wartości numerycznych na ciągi znaków
    """
    predictions_transformed = labels_encoder.inverse_transform(predictions)

    """
    Dodanie do zbioru danych przewidzianych etykiet dla każdego wiersza zbioru danych
    """
    data['label'] = predictions_transformed
    print("Przypisanie emocji do odpowiednich wierszy w zbiorze danych")
    """
    Zbeiranje danych o emocjach
    """
    emotions = count_emotions(data)
    print("Znieranie informacji o emocjach")
    """
    Zbeiranje danych o procedurach w  trakcie symulacji
    """
    time_stats = calculate_time_statistics(data)
    print("Znieranie informacji o procedurach w symulacji")
    """
    Zbeiranje danych o mruganiu i zamykaniu oczu
    """
    eyes_stats = analyze_eye_movements(data, time_stats)
    print("Znieranie informacji o mruganiu i zamknięciu oczu")
    """
    Zbeiranje danych o rotacji oczu
    """
    eyes_rotation = detect_eye_rotation(data)
    print("Znieranie informacji o rotacji oczu")
    """
    Zbieranie danych do słownika
    """
    more_info = {
        'time' : time_stats,
        'eye' : eyes_stats,
        "eyes_rotation": eyes_rotation
    }

    """
    Eksportownanie słownika do pliku JSONm w katalogu plots
    """
    export_to_json(more_info, plots_dir_path + '\\more_info.json')

    """
    Eksportownanie wykresów danych w formie zdjęć do katalogu plots 
    """
    save_all_plots(data, plots_dir_path)
    print("Zapisano wykresy dla danych")

    """
    Eksportownanie wykresów o emocjach w formie zdjęć do katalogu plots 
    """
    save_all_emotions_plots(emotions, plots_dir_path)
    print("Zapisano wykresy dla emocji")

    """
    Tworzenie ścieżki dla pliku index.html
    """
    index_html_path = os.path.join(report_dir_name, "index.html")

    """
    Zapis pliku index.html w katalogu dla danych z raportu, oraz tworzenie tytułu po dacie z nazwy katalogu
    """
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(generate_index_html(create_title(report_dir_name), str(more_info)))

    print(f"Plik index.html został zapisany w: {index_html_path}")
    print(f"Raport został pomyślnie wygenerowany w katalogu: '{report_dir_name}'")
