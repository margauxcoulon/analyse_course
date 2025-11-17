'''
Fonctions auxiliaires nécessaires pour l'analyse des fichiers .fit
'''

from fitparse import FitFile
import pandas as pd

# Conversion d'un fichier .fit en DataFrame pandas
def fit_to_dataframe(fit_path):
    fitfile = FitFile(fit_path)

    records = []
    for record in fitfile.get_messages("record"):
        data = {}
        for field in record:
            data[field.name] = field.value
        records.append(data)

    df = pd.DataFrame(records)
    return df

# Préparation du DataFrame avec colonnes utiles et calculs
def prepare_dataframe(fit_path):
    df = fit_to_dataframe(fit_path)
    
    # Colonnes utiles
    cols = ["timestamp", "distance", "enhanced_speed", "enhanced_altitude", "heart_rate", "cadence"]
    df = df[cols].copy()
    
    # Conversion
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["elapsed_s"] = (df["timestamp"] - df["timestamp"].iloc[0]).dt.total_seconds() # temps écoulé en secondes
    df["distance_km"] = df["distance"] / 1000 # distance en kilomètres
    df["pace_min_km"] = 16.6667 / df["enhanced_speed"] # allure en min/km
    df["pace_smooth"] = df["pace_min_km"].rolling(window=5, center=True).mean() # allure lissée sur 5 points pour éviter les aberrations (vitesses nulles)
    
    return df

# Nettoyage de la fin de séance en coupant l'inactivité
def clean_end_dataframe(df, speed_threshold=0.5, min_stop_duration=20):
    """
    Nettoie la séance en détectant l'inactivité à la fin et en coupant la partie inactive.
    Retourne df_clean et last_running_index.
    """
    df_cleaned = df.copy()
    
    # Détection inactivité
    df_cleaned["is_stop"] = df_cleaned["enhanced_speed"] < speed_threshold
    df_cleaned["stop_run"] = df_cleaned["is_stop"].rolling(min_stop_duration, min_periods=1).sum()
    last_running_index = df_cleaned[df_cleaned["stop_run"] < min_stop_duration].index[-1]
    
    # Couper la partie inactive
    df_cleaned = df_cleaned.loc[:last_running_index].copy()
    
    # Supprimer colonnes auxiliaires
    df_cleaned = df_cleaned.drop(columns=["is_stop", "stop_run"])
    
    return df_cleaned, last_running_index

# Calcul des indicateurs principaux
def compute_indicators(df):
    indicators = {
        "Distance totale (km)": df["distance_km"].iloc[-1],
        "Durée totale (min)": df["elapsed_s"].iloc[-1] / 60,
        "Allure moyenne (min/km)": df["pace_smooth"].mean(),
        "FC moyenne (bpm)": df["heart_rate"].mean(),
        "FC max (bpm)": df["heart_rate"].max(),
        "D+ (m)": df["enhanced_altitude"].diff().clip(lower=0).sum(),
        "D- (m)": df["enhanced_altitude"].diff().clip(upper=0).abs().sum()
    }
    return indicators

# Classification de la séance en fonction du nom de fichier
def classify_session(file_name):
    if "fraction" in file_name.lower():
        return "Fractionné"
    elif "long" in file_name.lower():
        return "Sortie longue"
    elif "tempo" in file_name.lower():
        return "Tempo"
    elif "race" in file_name.lower():
        return "Compétition"
    else:
        return "Footing"