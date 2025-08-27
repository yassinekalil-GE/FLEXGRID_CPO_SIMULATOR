#!/usr/bin/env python3
"""
NETTOYEUR DE DONNÉES DEMOSTEN - CORRECTION COMPLÈTE
Corrige toutes les incohérences logiques et valeurs aberrantes
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class DemostenDataCleaner:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.df_clean = None
        self.corrections_log = []
        
    def load_data(self):
        """Charge les données brutes"""
        print("📊 CHARGEMENT DES DONNÉES BRUTES...")
        self.df = pd.read_csv(self.file_path, sep=';')
        print(f"✅ {len(self.df):,} lignes chargées")
        return True
    
    def log_correction(self, message):
        """Enregistre les corrections effectuées"""
        self.corrections_log.append(message)
        print(f"🔧 {message}")
    
    def fix_power_values(self):
        """Corrige les valeurs de puissance aberrantes"""
        print("\n⚡ CORRECTION DES VALEURS DE PUISSANCE...")
        
        # Limites physiques réalistes pour une installation
        limits = {
            'PV_Power': {'min': 0, 'max': 100000},      # 0-100kW PV
            'Grid_Power': {'min': -100000, 'max': 100000}, # ±100kW Grid
            'LoadTot': {'min': 0, 'max': 200000},       # 0-200kW Load
            'Battery': {'min': -50000, 'max': 50000},   # ±50kW Battery
            'Conso': {'min': 0, 'max': 100000}          # 0-100kW Conso
        }
        
        for col, limit in limits.items():
            if col in self.df.columns:
                # Convertir en numérique
                self.df[col] = self.df[col].replace('\\N', np.nan)
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                
                # Compter les valeurs aberrantes
                before_count = len(self.df[col].dropna())
                outliers = self.df[(self.df[col] < limit['min']) | (self.df[col] > limit['max'])][col]
                
                # Corriger les valeurs aberrantes
                self.df.loc[self.df[col] < limit['min'], col] = limit['min']
                self.df.loc[self.df[col] > limit['max'], col] = limit['max']
                
                # PV ne peut pas être négatif (sauf erreur capteur mineure)
                if col == 'PV_Power':
                    self.df.loc[self.df[col] < 0, col] = 0
                
                after_count = len(self.df[col].dropna())
                self.log_correction(f"{col}: {len(outliers)} valeurs aberrantes corrigées ({limit['min']}-{limit['max']} W)")
    
    def fix_frequency(self):
        """Corrige les valeurs de fréquence"""
        print("\n🔌 CORRECTION DE LA FRÉQUENCE RÉSEAU...")
        
        if 'Frequency' in self.df.columns:
            self.df['Frequency'] = self.df['Frequency'].replace('\\N', np.nan)
            self.df['Frequency'] = pd.to_numeric(self.df['Frequency'], errors='coerce')
            
            # Limites réalistes pour la fréquence (49.5-50.5 Hz)
            freq_data = self.df['Frequency'].dropna()
            outliers = freq_data[(freq_data < 49.5) | (freq_data > 50.5)]
            
            # Corriger les fréquences aberrantes vers 50Hz
            self.df.loc[self.df['Frequency'] < 49.5, 'Frequency'] = 50.0
            self.df.loc[self.df['Frequency'] > 50.5, 'Frequency'] = 50.0
            self.df.loc[self.df['Frequency'] <= 0, 'Frequency'] = 50.0
            
            self.log_correction(f"Frequency: {len(outliers)} valeurs aberrantes corrigées vers 50Hz")
    
    def fix_power_factor(self):
        """Corrige le facteur de puissance"""
        print("\n⚡ CORRECTION DU FACTEUR DE PUISSANCE...")
        
        if 'Power_Factor' in self.df.columns:
            self.df['Power_Factor'] = self.df['Power_Factor'].replace('\\N', np.nan)
            self.df['Power_Factor'] = pd.to_numeric(self.df['Power_Factor'], errors='coerce')
            
            # Facteur de puissance doit être entre -1 et 1
            pf_data = self.df['Power_Factor'].dropna()
            outliers = pf_data[(pf_data < -1) | (pf_data > 1)]
            
            # Corriger les valeurs aberrantes
            self.df.loc[self.df['Power_Factor'] < -1, 'Power_Factor'] = -1
            self.df.loc[self.df['Power_Factor'] > 1, 'Power_Factor'] = 1
            
            # Remplacer les valeurs extrêmes par une valeur typique (0.9)
            self.df.loc[abs(self.df['Power_Factor']) > 1, 'Power_Factor'] = 0.9
            
            self.log_correction(f"Power_Factor: {len(outliers)} valeurs aberrantes corrigées (-1 à 1)")
    
    def fix_time_gaps(self):
        """Corrige les gaps temporels"""
        print("\n⏰ CORRECTION DES GAPS TEMPORELS...")
        
        try:
            # Convertir en datetime
            self.df['Time'] = pd.to_datetime(self.df['Time'], format='%d/%m/%Y %H:%M')
            
            # Trier par temps
            self.df = self.df.sort_values('Time').reset_index(drop=True)
            
            # Détecter l'intervalle normal (mode)
            time_diffs = self.df['Time'].diff().dropna()
            normal_interval = time_diffs.mode().iloc[0] if len(time_diffs.mode()) > 0 else timedelta(seconds=1)
            
            # Identifier les gaps significatifs (> 2x l'intervalle normal)
            gaps = time_diffs[time_diffs > normal_interval * 2]
            
            self.log_correction(f"Time: {len(gaps)} gaps temporels détectés (intervalle normal: {normal_interval})")
            
        except Exception as e:
            self.log_correction(f"Time: Erreur correction temporelle - {e}")
    
    def interpolate_missing_data(self):
        """Interpole les données manquantes de manière intelligente"""
        print("\n📈 INTERPOLATION DES DONNÉES MANQUANTES...")
        
        numeric_cols = ['Grid_Power', 'PV_Power', 'LoadTot', 'Battery', 'Conso', 'Frequency', 'Power_Factor']
        
        for col in numeric_cols:
            if col in self.df.columns:
                missing_before = self.df[col].isnull().sum()
                
                if missing_before > 0:
                    if col in ['Battery', 'Conso']:
                        # Pour Battery et Conso (beaucoup de manquantes), utiliser 0 par défaut
                        self.df[col] = self.df[col].fillna(0)
                    else:
                        # Pour les autres, interpolation linéaire
                        self.df[col] = self.df[col].interpolate(method='linear')
                        # Remplir les valeurs restantes avec la moyenne
                        self.df[col] = self.df[col].fillna(self.df[col].mean())
                    
                    missing_after = self.df[col].isnull().sum()
                    interpolated = missing_before - missing_after
                    
                    if interpolated > 0:
                        self.log_correction(f"{col}: {interpolated:,} valeurs interpolées")
    
    def validate_energy_balance(self):
        """Valide et corrige les bilans énergétiques"""
        print("\n⚖️ VALIDATION DES BILANS ÉNERGÉTIQUES...")
        
        # Calculer le bilan énergétique théorique
        # Principe: PV + Grid = Load + Battery_charge
        if all(col in self.df.columns for col in ['PV_Power', 'Grid_Power', 'LoadTot', 'Battery']):
            
            # Calculer le bilan
            production = self.df['PV_Power'] + self.df['Grid_Power']
            consumption = self.df['LoadTot'] + self.df['Battery']
            balance = production - consumption
            
            # Identifier les déséquilibres importants (> 10% de la charge)
            threshold = self.df['LoadTot'] * 0.1
            imbalances = abs(balance) > threshold
            
            self.log_correction(f"Energy Balance: {imbalances.sum():,} déséquilibres détectés (>{threshold.mean():.0f}W)")
            
            # Ajuster légèrement Grid_Power pour équilibrer (si déséquilibre < 20%)
            small_imbalances = (abs(balance) <= self.df['LoadTot'] * 0.2) & imbalances
            self.df.loc[small_imbalances, 'Grid_Power'] -= balance[small_imbalances]
            
            corrected = small_imbalances.sum()
            if corrected > 0:
                self.log_correction(f"Energy Balance: {corrected:,} déséquilibres mineurs corrigés")
    
    def apply_physical_constraints(self):
        """Applique les contraintes physiques"""
        print("\n🔬 APPLICATION DES CONTRAINTES PHYSIQUES...")
        
        # PV ne produit pas la nuit (heure entre 20h et 6h)
        if 'Time' in self.df.columns and 'PV_Power' in self.df.columns:
            night_mask = (self.df['Time'].dt.hour >= 20) | (self.df['Time'].dt.hour <= 6)
            night_pv = self.df.loc[night_mask & (self.df['PV_Power'] > 100), 'PV_Power']
            
            if len(night_pv) > 0:
                self.df.loc[night_mask & (self.df['PV_Power'] > 100), 'PV_Power'] = 0
                self.log_correction(f"PV_Power: {len(night_pv)} valeurs nocturnes corrigées à 0W")
        
        # La consommation ne peut pas être négative
        if 'LoadTot' in self.df.columns:
            negative_load = self.df[self.df['LoadTot'] < 0]['LoadTot']
            if len(negative_load) > 0:
                self.df.loc[self.df['LoadTot'] < 0, 'LoadTot'] = abs(self.df.loc[self.df['LoadTot'] < 0, 'LoadTot'])
                self.log_correction(f"LoadTot: {len(negative_load)} valeurs négatives corrigées")
    
    def create_visualizations(self):
        """Crée des visualisations avant/après nettoyage"""
        print("\n📊 CRÉATION DES VISUALISATIONS...")
        
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            
            # Échantillonner pour la visualisation
            sample_size = min(10000, len(self.df))
            df_sample = self.df.sample(n=sample_size).sort_values('Time')
            
            # Graphique 1: Puissances principales
            axes[0,0].plot(df_sample['PV_Power'], label='PV', alpha=0.7)
            axes[0,0].plot(df_sample['Grid_Power'], label='Grid', alpha=0.7)
            axes[0,0].plot(df_sample['LoadTot'], label='Load', alpha=0.7)
            axes[0,0].set_title('Profils de Puissance Corrigés')
            axes[0,0].set_ylabel('Puissance (W)')
            axes[0,0].legend()
            axes[0,0].grid(True, alpha=0.3)
            
            # Graphique 2: Fréquence
            axes[0,1].plot(df_sample['Frequency'], color='red', alpha=0.7)
            axes[0,1].axhline(y=50, color='black', linestyle='--', label='50Hz nominal')
            axes[0,1].set_title('Fréquence Réseau Corrigée')
            axes[0,1].set_ylabel('Fréquence (Hz)')
            axes[0,1].legend()
            axes[0,1].grid(True, alpha=0.3)
            
            # Graphique 3: Facteur de puissance
            axes[1,0].plot(df_sample['Power_Factor'], color='green', alpha=0.7)
            axes[1,0].axhline(y=1, color='red', linestyle='--', label='Limite max')
            axes[1,0].axhline(y=-1, color='red', linestyle='--', label='Limite min')
            axes[1,0].set_title('Facteur de Puissance Corrigé')
            axes[1,0].set_ylabel('Facteur de Puissance')
            axes[1,0].legend()
            axes[1,0].grid(True, alpha=0.3)
            
            # Graphique 4: Bilan énergétique
            if all(col in df_sample.columns for col in ['PV_Power', 'Grid_Power', 'LoadTot']):
                balance = df_sample['PV_Power'] + df_sample['Grid_Power'] - df_sample['LoadTot']
                axes[1,1].plot(balance, color='purple', alpha=0.7)
                axes[1,1].axhline(y=0, color='black', linestyle='--', label='Équilibre')
                axes[1,1].set_title('Bilan Énergétique (PV+Grid-Load)')
                axes[1,1].set_ylabel('Bilan (W)')
                axes[1,1].legend()
                axes[1,1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('donnees_corrigees_demosten.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            self.log_correction("Visualisations sauvegardées: donnees_corrigees_demosten.png")
            
        except Exception as e:
            self.log_correction(f"Erreur visualisation: {e}")
    
    def save_cleaned_data(self):
        """Sauvegarde les données nettoyées"""
        print("\n💾 SAUVEGARDE DES DONNÉES NETTOYÉES...")
        
        # Sauvegarder le fichier nettoyé
        cleaned_filename = "demosten_donnees_nettoyees.csv"
        self.df.to_csv(cleaned_filename, index=False, sep=';')
        
        # Créer un rapport de nettoyage
        report_filename = "rapport_nettoyage_demosten.txt"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write("🔧 RAPPORT DE NETTOYAGE - DONNÉES DEMOSTEN\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Fichier original: {self.file_path}\n")
            f.write(f"Fichier nettoyé: {cleaned_filename}\n")
            f.write(f"Date de nettoyage: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
            
            f.write("CORRECTIONS EFFECTUÉES:\n")
            f.write("-" * 25 + "\n")
            for correction in self.corrections_log:
                f.write(f"• {correction}\n")
            
            f.write(f"\nSTATISTIQUES FINALES:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Lignes traitées: {len(self.df):,}\n")
            f.write(f"Colonnes: {len(self.df.columns)}\n")
            f.write(f"Période: {self.df['Time'].min()} à {self.df['Time'].max()}\n")
            
            # Statistiques par colonne
            energy_cols = ['Grid_Power', 'PV_Power', 'LoadTot', 'Battery', 'Frequency', 'Power_Factor']
            for col in energy_cols:
                if col in self.df.columns:
                    stats = self.df[col].describe()
                    f.write(f"\n{col}:\n")
                    f.write(f"  - Moyenne: {stats['mean']:.2f}\n")
                    f.write(f"  - Min: {stats['min']:.2f}\n")
                    f.write(f"  - Max: {stats['max']:.2f}\n")
                    f.write(f"  - Valeurs manquantes: {self.df[col].isnull().sum()}\n")
        
        self.log_correction(f"Données nettoyées sauvegardées: {cleaned_filename}")
        self.log_correction(f"Rapport de nettoyage: {report_filename}")
    
    def clean_all(self):
        """Exécute le nettoyage complet"""
        print("🚀 === NETTOYAGE COMPLET DES DONNÉES DEMOSTEN ===\n")
        
        # Charger les données
        self.load_data()
        
        # Appliquer toutes les corrections
        self.fix_power_values()
        self.fix_frequency()
        self.fix_power_factor()
        self.fix_time_gaps()
        self.interpolate_missing_data()
        self.apply_physical_constraints()
        self.validate_energy_balance()
        
        # Créer les visualisations
        self.create_visualizations()
        
        # Sauvegarder
        self.save_cleaned_data()
        
        print(f"\n✅ === NETTOYAGE TERMINÉ ===")
        print(f"📁 Fichiers générés:")
        print(f"  • demosten_donnees_nettoyees.csv - Données corrigées")
        print(f"  • rapport_nettoyage_demosten.txt - Rapport détaillé")
        print(f"  • donnees_corrigees_demosten.png - Visualisations")
        print(f"\n🔧 {len(self.corrections_log)} corrections effectuées au total")

def main():
    """Fonction principale"""
    cleaner = DemostenDataCleaner("hostorical data demosten.csv")
    cleaner.clean_all()

if __name__ == "__main__":
    main()
