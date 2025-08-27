#!/usr/bin/env python3
"""
Analyse de Qualité des Données Historiques - EV2Gym
Analyse des données PV/Consommation/Grid avec détection de pertes et nettoyage
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class DataQualityAnalyzer:
    def __init__(self, file_path):
        """Initialise l'analyseur avec le chemin du fichier de données"""
        self.file_path = file_path
        self.df = None
        self.quality_report = {}
        
    def load_data(self):
        """Charge les données depuis le fichier CSV"""
        try:
            print(f"📊 Chargement des données depuis: {self.file_path}")
            
            # Essayer différents encodages
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    self.df = pd.read_csv(self.file_path, encoding=encoding)
                    print(f"✅ Données chargées avec succès (encoding: {encoding})")
                    break
                except UnicodeDecodeError:
                    continue
            
            if self.df is None:
                raise Exception("Impossible de charger le fichier avec les encodages testés")
                
            print(f"📈 Dimensions des données: {self.df.shape}")
            print(f"📅 Colonnes disponibles: {list(self.df.columns)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {str(e)}")
            return False
    
    def detect_datetime_column(self):
        """Détecte automatiquement la colonne de timestamp"""
        datetime_candidates = []
        
        for col in self.df.columns:
            # Vérifier si le nom de colonne suggère une date/heure
            if any(keyword in col.lower() for keyword in ['time', 'date', 'timestamp', 'datetime', 'heure', 'temps']):
                datetime_candidates.append(col)
                
        if datetime_candidates:
            return datetime_candidates[0]
        
        # Si pas trouvé par nom, chercher par contenu
        for col in self.df.columns:
            try:
                pd.to_datetime(self.df[col].iloc[:10])
                return col
            except:
                continue
                
        return None
    
    def basic_quality_checks(self):
        """Effectue les vérifications de qualité de base"""
        print("\n🔍 === VÉRIFICATIONS DE QUALITÉ DES DONNÉES ===")
        
        # 1. Informations générales
        self.quality_report['total_rows'] = len(self.df)
        self.quality_report['total_columns'] = len(self.df.columns)
        
        print(f"📊 Nombre total de lignes: {self.quality_report['total_rows']:,}")
        print(f"📊 Nombre total de colonnes: {self.quality_report['total_columns']}")
        
        # 2. Valeurs manquantes
        missing_data = self.df.isnull().sum()
        missing_percentage = (missing_data / len(self.df)) * 100
        
        self.quality_report['missing_data'] = missing_data.to_dict()
        self.quality_report['missing_percentage'] = missing_percentage.to_dict()
        
        print("\n📉 VALEURS MANQUANTES:")
        for col in self.df.columns:
            if missing_data[col] > 0:
                print(f"  • {col}: {missing_data[col]:,} ({missing_percentage[col]:.2f}%)")
        
        # 3. Doublons
        duplicates = self.df.duplicated().sum()
        self.quality_report['duplicates'] = duplicates
        print(f"\n🔄 Lignes dupliquées: {duplicates:,}")
        
        # 4. Types de données
        print(f"\n📋 TYPES DE DONNÉES:")
        for col in self.df.columns:
            print(f"  • {col}: {self.df[col].dtype}")
        
        return self.quality_report
    
    def detect_data_loss(self):
        """Détecte les pertes de données et les gaps temporels"""
        print("\n🕳️ === DÉTECTION DES PERTES DE DONNÉES ===")
        
        # Détecter la colonne de temps
        datetime_col = self.detect_datetime_column()
        
        if datetime_col is None:
            print("❌ Aucune colonne de timestamp détectée")
            return
        
        print(f"📅 Colonne de timestamp détectée: {datetime_col}")
        
        try:
            # Convertir en datetime
            self.df[datetime_col] = pd.to_datetime(self.df[datetime_col])
            self.df = self.df.sort_values(datetime_col)
            
            # Calculer les intervalles de temps
            time_diffs = self.df[datetime_col].diff()
            
            # Détecter l'intervalle normal (mode)
            normal_interval = time_diffs.mode().iloc[0] if len(time_diffs.mode()) > 0 else timedelta(minutes=15)
            
            print(f"⏱️ Intervalle normal détecté: {normal_interval}")
            
            # Détecter les gaps (intervalles > 2x l'intervalle normal)
            threshold = normal_interval * 2
            gaps = time_diffs[time_diffs > threshold]
            
            self.quality_report['gaps'] = len(gaps)
            self.quality_report['normal_interval'] = str(normal_interval)
            
            print(f"🕳️ Nombre de gaps détectés: {len(gaps)}")
            
            if len(gaps) > 0:
                print("\n📍 GAPS DÉTECTÉS:")
                for idx, gap in gaps.items():
                    start_time = self.df.loc[idx-1, datetime_col] if idx > 0 else "Début"
                    end_time = self.df.loc[idx, datetime_col]
                    print(f"  • Gap de {gap} entre {start_time} et {end_time}")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse temporelle: {str(e)}")
    
    def energy_balance_analysis(self):
        """Analyse les bilans énergétiques"""
        print("\n⚡ === ANALYSE DES BILANS ÉNERGÉTIQUES ===")
        
        # Identifier les colonnes d'énergie
        energy_columns = []
        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['pv', 'solar', 'production', 'consommation', 'consumption', 'grid', 'réseau', 'power', 'puissance', 'energy', 'energie']):
                energy_columns.append(col)
        
        print(f"🔋 Colonnes d'énergie détectées: {energy_columns}")
        
        if len(energy_columns) == 0:
            print("❌ Aucune colonne d'énergie détectée")
            return
        
        # Statistiques descriptives
        print("\n📊 STATISTIQUES ÉNERGÉTIQUES:")
        for col in energy_columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                stats = self.df[col].describe()
                print(f"\n  • {col}:")
                print(f"    - Moyenne: {stats['mean']:.2f}")
                print(f"    - Médiane: {stats['50%']:.2f}")
                print(f"    - Min: {stats['min']:.2f}")
                print(f"    - Max: {stats['max']:.2f}")
                print(f"    - Écart-type: {stats['std']:.2f}")
                
                # Détecter les valeurs aberrantes
                Q1 = stats['25%']
                Q3 = stats['75%']
                IQR = Q3 - Q1
                outliers = self.df[(self.df[col] < Q1 - 1.5*IQR) | (self.df[col] > Q3 + 1.5*IQR)][col]
                print(f"    - Valeurs aberrantes: {len(outliers)} ({len(outliers)/len(self.df)*100:.2f}%)")
    
    def create_visualizations(self):
        """Crée les visualisations des profils énergétiques"""
        print("\n📈 === CRÉATION DES VISUALISATIONS ===")
        
        # Détecter les colonnes importantes
        datetime_col = self.detect_datetime_column()
        energy_columns = []
        
        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['pv', 'solar', 'production', 'consommation', 'consumption', 'grid', 'réseau', 'power', 'puissance']):
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    energy_columns.append(col)
        
        if datetime_col is None or len(energy_columns) == 0:
            print("❌ Données insuffisantes pour les visualisations")
            return
        
        # Convertir la colonne de temps
        self.df[datetime_col] = pd.to_datetime(self.df[datetime_col])
        
        # Créer les graphiques
        fig = make_subplots(
            rows=len(energy_columns), cols=1,
            subplot_titles=energy_columns,
            shared_xaxes=True,
            vertical_spacing=0.05
        )
        
        colors = px.colors.qualitative.Set1
        
        for i, col in enumerate(energy_columns):
            fig.add_trace(
                go.Scatter(
                    x=self.df[datetime_col],
                    y=self.df[col],
                    mode='lines',
                    name=col,
                    line=dict(color=colors[i % len(colors)]),
                    showlegend=True
                ),
                row=i+1, col=1
            )
        
        fig.update_layout(
            title="📊 Profils Énergétiques - PV/Consommation/Grid",
            height=300 * len(energy_columns),
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Temps", row=len(energy_columns), col=1)
        
        # Sauvegarder le graphique
        fig.write_html("energy_profiles_analysis.html")
        print("✅ Graphique sauvegardé: energy_profiles_analysis.html")
        
        return fig
    
    def clean_data(self):
        """Nettoie les données si nécessaire"""
        print("\n🧹 === NETTOYAGE DES DONNÉES ===")
        
        original_rows = len(self.df)
        
        # 1. Supprimer les doublons
        self.df = self.df.drop_duplicates()
        print(f"🔄 Doublons supprimés: {original_rows - len(self.df)}")
        
        # 2. Traiter les valeurs manquantes pour les colonnes numériques
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                # Interpolation linéaire pour les données temporelles
                self.df[col] = self.df[col].interpolate(method='linear')
                print(f"📈 {col}: {missing_count} valeurs interpolées")
        
        # 3. Sauvegarder les données nettoyées
        cleaned_filename = "cleaned_historical_data.csv"
        self.df.to_csv(cleaned_filename, index=False)
        print(f"✅ Données nettoyées sauvegardées: {cleaned_filename}")
        
        return self.df
    
    def generate_report(self):
        """Génère un rapport complet de qualité"""
        print("\n📋 === RAPPORT DE QUALITÉ COMPLET ===")
        
        report = f"""
        🔍 RAPPORT D'ANALYSE DE QUALITÉ DES DONNÉES
        ==========================================
        
        📊 INFORMATIONS GÉNÉRALES:
        - Nombre de lignes: {self.quality_report.get('total_rows', 'N/A'):,}
        - Nombre de colonnes: {self.quality_report.get('total_columns', 'N/A')}
        - Doublons détectés: {self.quality_report.get('duplicates', 'N/A'):,}
        - Gaps temporels: {self.quality_report.get('gaps', 'N/A')}
        
        📉 VALEURS MANQUANTES:
        """
        
        if 'missing_data' in self.quality_report:
            for col, missing in self.quality_report['missing_data'].items():
                if missing > 0:
                    percentage = self.quality_report['missing_percentage'][col]
                    report += f"        - {col}: {missing:,} ({percentage:.2f}%)\n"
        
        report += f"""
        ⏱️ ANALYSE TEMPORELLE:
        - Intervalle normal: {self.quality_report.get('normal_interval', 'N/A')}
        
        ✅ RECOMMANDATIONS:
        - Vérifier les gaps temporels identifiés
        - Valider les valeurs aberrantes détectées
        - Considérer l'interpolation pour les valeurs manquantes
        - Surveiller la cohérence des bilans énergétiques
        """
        
        # Sauvegarder le rapport
        with open("data_quality_report.txt", "w", encoding="utf-8") as f:
            f.write(report)
        
        print(report)
        print("✅ Rapport sauvegardé: data_quality_report.txt")

def main():
    """Fonction principale d'analyse"""
    file_path = r"C:\Users\MODERN\Downloads\hostorical data demosten.csv"
    
    print("🚀 === ANALYSEUR DE QUALITÉ DES DONNÉES EV2GYM ===")
    print(f"📁 Fichier à analyser: {file_path}")
    
    # Initialiser l'analyseur
    analyzer = DataQualityAnalyzer(file_path)
    
    # Charger les données
    if not analyzer.load_data():
        return
    
    # Effectuer les analyses
    analyzer.basic_quality_checks()
    analyzer.detect_data_loss()
    analyzer.energy_balance_analysis()
    analyzer.create_visualizations()
    analyzer.clean_data()
    analyzer.generate_report()
    
    print("\n✅ === ANALYSE TERMINÉE ===")
    print("📁 Fichiers générés:")
    print("  • energy_profiles_analysis.html - Visualisations interactives")
    print("  • cleaned_historical_data.csv - Données nettoyées")
    print("  • data_quality_report.txt - Rapport complet")

if __name__ == "__main__":
    main()
