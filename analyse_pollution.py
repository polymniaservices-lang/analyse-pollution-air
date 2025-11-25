import pandas as pd
import matplotlib.pyplot as plt

# ========================================
# 1. CHARGER LES DONNÉES
# ========================================
df = pd.read_csv('FR_E2_2025-01-01.csv', sep=';')

print("Aperçu des données :")
print(df.head())
print(f"\n[{len(df)} lignes × {len(df.columns)} colonnes]")

# ========================================
# 2. NETTOYER ET SÉLECTIONNER LES COLONNES UTILES
# ========================================
df_clean = df[['Date de début', 'nom site', 'Polluant', 'valeur', 'unité de mesure']].copy()

# Convertir la date en format datetime
df_clean['Date de début'] = pd.to_datetime(df_clean['Date de début'], format='%Y/%m/%d %H:%M:%S')

# Voir les polluants disponibles
print("\nPolluants disponibles :")
print(df_clean['Polluant'].unique())

# ========================================
# 3. FILTRER NO2 ET METZ-CENTRE
# ========================================
df_no2 = df_clean[df_clean['Polluant'] == 'NO2'].copy()

print(f"\nNombre de mesures NO2 : {len(df_no2)}")

# Filtrer SEULEMENT Metz-Centre
df_metz = df_no2[df_no2['nom site'] == 'Metz-Centre'].copy()

# Extraire juste l'heure
df_metz['heure'] = df_metz['Date de début'].dt.hour

print(f"Nombre de mesures NO2 pour Metz-Centre : {len(df_metz)}")
print("\nAperçu des données Metz :")
print(df_metz.head())

# ========================================
# 4. GRAPHIQUE 1 : ÉVOLUTION NO2 METZ-CENTRE
# ========================================
plt.figure(figsize=(14, 7))
plt.plot(df_metz['heure'], df_metz['valeur'], color='blue', linewidth=2, marker='o', markersize=8)
plt.xlabel('Heure de la journée', fontsize=12)
plt.ylabel('Concentration NO2 (µg/m³)', fontsize=12)
plt.title(f'Evolution de la concentration de NO2 - Metz-Centre - 1er janvier 2025 ({len(df_metz)} mesures)', 
          fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

# Formatter l'axe X avec "00h00", "01h00", etc.
heures_labels = [f"{h:02d}h00" for h in range(0, 24)]
plt.xticks(range(0, 24), heures_labels, rotation=90)

plt.tight_layout()
plt.savefig('no2_metz_evolution.png', dpi=300)
plt.show()

print("\nGraphique 1 sauvegardé : no2_metz_evolution.png")

# ========================================
# 5. GRAPHIQUE 2 : COMPARAISON DES POLLUANTS
# ========================================
polluants_a_comparer = ['NO2', 'O3', 'PM10']
df_comparaison = df_clean[(df_clean['nom site'] == 'Metz-Centre') & 
                          (df_clean['Polluant'].isin(polluants_a_comparer))].copy()

# Extraire l'heure
df_comparaison['heure'] = df_comparaison['Date de début'].dt.hour

plt.figure(figsize=(14, 7))

for polluant in polluants_a_comparer:
    data = df_comparaison[df_comparaison['Polluant'] == polluant]
    if len(data) > 0:
        plt.plot(data['heure'], data['valeur'], marker='o', linewidth=2, markersize=6, label=polluant)

plt.xlabel('Heure de la journée', fontsize=12)
plt.ylabel('Concentration (µg/m³)', fontsize=12)
plt.title('Comparaison des polluants - Metz-Centre - 1er janvier 2025', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)

# Formatter l'axe X
plt.xticks(range(0, 24), heures_labels, rotation=90)

plt.tight_layout()
plt.savefig('comparaison_polluants_metz.png', dpi=300)
plt.show()

print("Graphique 2 sauvegardé : comparaison_polluants_metz.png")

print("\n✅ Analyse terminée !")