"""
🌍 Professional CPO Dashboard - COMPLETE VERSION
Advanced EV Charging Station Management with Real-Time Analytics
Global Charging Infrastructure & Comprehensive Financial Analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

# Professional Page Configuration
st.set_page_config(
    page_title="FLEXGRID CPO - Real-Time Intelligent Dashboard for Ancillary Services",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }
    
    .main-header h2 {
        margin: 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.9;
    }
    
    .kpi-metric {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .kpi-metric h3 {
        margin: 0.5rem 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .kpi-metric h4 {
        margin: 0;
        font-size: 1rem;
        font-weight: 500;
        opacity: 0.9;
    }
    
    .professional-alert {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        border-left: 4px solid #0066cc;
        font-family: 'Inter', sans-serif;
    }
    
    .success-alert {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: #2d3748;
        margin: 1rem 0;
        border-left: 4px solid #10b981;
        font-family: 'Inter', sans-serif;
    }
    
    .charging-station-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: #2d3748;
        margin: 1rem 0;
        border-left: 4px solid #f59e0b;
        font-family: 'Inter', sans-serif;
    }
    
    .executive-summary {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 10px;
        color: #2d3748;
        margin: 1rem 0;
        border-left: 4px solid #10b981;
        font-family: 'Inter', sans-serif;
    }
    
    .sidebar .sidebar-content {
        font-family: 'Inter', sans-serif;
        background: #f8fafc;
    }
    
    .stSelectbox > div > div {
        font-family: 'Inter', sans-serif;
    }
    
    .stMetric {
        font-family: 'Inter', sans-serif;
    }
    
    .real-time-dashboard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

class MoroccanGridData:
    """Moroccan Grid Infrastructure Data"""
    
    @staticmethod
    def get_grid_zones():
        return {
            'Casablanca': {
                'voltage_level_kv': 225,
                'capacity_mw': 850,
                'renewable_percentage': 35,
                'grid_stability': 0.92,
                'peak_hours': '18:00-22:00',
                'modernization_level': 'High',
                'population': 3360000,
                'ev_adoption_rate': 0.08,
                'grid_code': 'ONEE_HV_2024'
            },
            'Rabat': {
                'voltage_level_kv': 400,
                'capacity_mw': 480,
                'renewable_percentage': 45,
                'grid_stability': 0.95,
                'peak_hours': '19:00-23:00',
                'modernization_level': 'Very High',
                'population': 1930000,
                'ev_adoption_rate': 0.12,
                'grid_code': 'ONEE_HV_2024'
            },
            'Marrakech': {
                'voltage_level_kv': 225,
                'capacity_mw': 380,
                'renewable_percentage': 55,
                'grid_stability': 0.88,
                'peak_hours': '17:30-21:30',
                'modernization_level': 'Medium',
                'population': 1330000,
                'ev_adoption_rate': 0.06,
                'grid_code': 'ONEE_MV_2024'
            },
            'Fès': {
                'voltage_level_kv': 225,
                'capacity_mw': 320,
                'renewable_percentage': 40,
                'grid_stability': 0.90,
                'peak_hours': '18:30-22:30',
                'modernization_level': 'Medium',
                'population': 1150000,
                'ev_adoption_rate': 0.05,
                'grid_code': 'ONEE_MV_2024'
            },
            'Tanger': {
                'voltage_level_kv': 400,
                'capacity_mw': 420,
                'renewable_percentage': 50,
                'grid_stability': 0.93,
                'peak_hours': '18:00-22:00',
                'modernization_level': 'High',
                'population': 1070000,
                'ev_adoption_rate': 0.09,
                'grid_code': 'ONEE_HV_2024'
            },
            'Agadir': {
                'voltage_level_kv': 225,
                'capacity_mw': 280,
                'renewable_percentage': 65,
                'grid_stability': 0.87,
                'peak_hours': '17:00-21:00',
                'modernization_level': 'Medium',
                'population': 924000,
                'ev_adoption_rate': 0.07,
                'grid_code': 'ONEE_MV_2024'
            },
            'Meknès': {
                'voltage_level_kv': 225,
                'capacity_mw': 240,
                'renewable_percentage': 42,
                'grid_stability': 0.89,
                'peak_hours': '18:00-22:00',
                'modernization_level': 'Medium',
                'population': 835000,
                'ev_adoption_rate': 0.04,
                'grid_code': 'ONEE_MV_2024'
            },
            'Oujda': {
                'voltage_level_kv': 225,
                'capacity_mw': 200,
                'renewable_percentage': 38,
                'grid_stability': 0.86,
                'peak_hours': '18:30-22:30',
                'modernization_level': 'Medium',
                'population': 720000,
                'ev_adoption_rate': 0.03,
                'grid_code': 'ONEE_MV_2024'
            },
            'Kenitra': {
                'voltage_level_kv': 225,
                'capacity_mw': 180,
                'renewable_percentage': 44,
                'grid_stability': 0.91,
                'peak_hours': '18:00-22:00',
                'modernization_level': 'High',
                'population': 650000,
                'ev_adoption_rate': 0.06,
                'grid_code': 'ONEE_MV_2024'
            },
            'Tétouan': {
                'voltage_level_kv': 225,
                'capacity_mw': 160,
                'renewable_percentage': 48,
                'grid_stability': 0.88,
                'peak_hours': '17:30-21:30',
                'modernization_level': 'Medium',
                'population': 580000,
                'ev_adoption_rate': 0.05,
                'grid_code': 'ONEE_MV_2024'
            }
        }
    
    @staticmethod
    def get_onee_tariffs():
        return {
            'residential': {
                'peak_hours': {'time': '18:00-22:00', 'price_mad_kwh': 1.45},
                'standard_hours': {'time': '06:00-18:00', 'price_mad_kwh': 1.15},
                'off_peak_hours': {'time': '22:00-06:00', 'price_mad_kwh': 0.85}
            },
            'commercial': {
                'peak_hours': {'time': '18:00-22:00', 'price_mad_kwh': 1.65},
                'standard_hours': {'time': '06:00-18:00', 'price_mad_kwh': 1.35},
                'off_peak_hours': {'time': '22:00-06:00', 'price_mad_kwh': 1.05}
            },
            'industrial': {
                'peak_hours': {'time': '18:00-22:00', 'price_mad_kwh': 1.25},
                'standard_hours': {'time': '06:00-18:00', 'price_mad_kwh': 0.95},
                'off_peak_hours': {'time': '22:00-06:00', 'price_mad_kwh': 0.75}
            }
        }

class GlobalChargingStations:
    """Global Famous Charging Station Models and Specifications"""

    @staticmethod
    def get_station_models():
        return {
            # Tesla Supercharger Series
            'Tesla_Supercharger_V3': {
                'name': 'Tesla Supercharger V3',
                'manufacturer': 'Tesla',
                'type': 'DC_Ultra_Fast',
                'max_power_kw': 250,
                'connector_type': 'CCS2 + Tesla Connector',
                'installation_cost_mad': 450000,
                'operational_cost_mad_month': 8500,
                'efficiency': 0.94,
                'warranty_years': 4,
                'grid_connection': 'MV 22kV + DC conversion',
                'communication': 'Tesla Protocol + OCPP 2.0',
                'v2g_capable': False,
                'global_installations': 45000,
                'vehicles_supported': 2
            },
            'Tesla_Supercharger_V4': {
                'name': 'Tesla Supercharger V4',
                'manufacturer': 'Tesla',
                'type': 'DC_Ultra_Fast',
                'max_power_kw': 350,
                'connector_type': 'CCS2 + Tesla Connector',
                'installation_cost_mad': 520000,
                'operational_cost_mad_month': 9500,
                'efficiency': 0.96,
                'warranty_years': 5,
                'grid_connection': 'MV 22kV + DC conversion',
                'communication': 'Tesla Protocol + OCPP 2.0.1',
                'v2g_capable': True,
                'global_installations': 8000,
                'vehicles_supported': 2
            },

            # ABB Terra Series
            'ABB_Terra_360': {
                'name': 'ABB Terra 360',
                'manufacturer': 'ABB',
                'type': 'DC_Ultra_Fast',
                'max_power_kw': 360,
                'connector_type': 'CCS2 + CHAdeMO + Type 2',
                'installation_cost_mad': 750000,
                'operational_cost_mad_month': 12000,
                'efficiency': 0.96,
                'warranty_years': 5,
                'grid_connection': 'MV 22kV + DC conversion',
                'communication': 'OCPP 2.0.1',
                'v2g_capable': True,
                'global_installations': 15000,
                'vehicles_supported': 2
            },
            'ABB_Terra_184': {
                'name': 'ABB Terra 184',
                'manufacturer': 'ABB',
                'type': 'DC_Fast',
                'max_power_kw': 180,
                'connector_type': 'CCS2 + CHAdeMO',
                'installation_cost_mad': 380000,
                'operational_cost_mad_month': 6500,
                'efficiency': 0.95,
                'warranty_years': 5,
                'grid_connection': 'LV 400V + DC conversion',
                'communication': 'OCPP 2.0',
                'v2g_capable': True,
                'global_installations': 25000,
                'vehicles_supported': 2
            },
            'ABB_Terra_AC': {
                'name': 'ABB Terra AC',
                'manufacturer': 'ABB',
                'type': 'AC_Fast',
                'max_power_kw': 22,
                'connector_type': 'Type 2',
                'installation_cost_mad': 65000,
                'operational_cost_mad_month': 1400,
                'efficiency': 0.93,
                'warranty_years': 5,
                'grid_connection': 'LV 400V AC',
                'communication': 'OCPP 1.6J',
                'v2g_capable': False,
                'global_installations': 80000,
                'vehicles_supported': 1
            },

            # ChargePoint Series
            'ChargePoint_Express_250': {
                'name': 'ChargePoint Express 250',
                'manufacturer': 'ChargePoint',
                'type': 'DC_Fast',
                'max_power_kw': 250,
                'connector_type': 'CCS1/CCS2 + CHAdeMO',
                'installation_cost_mad': 420000,
                'operational_cost_mad_month': 7800,
                'efficiency': 0.93,
                'warranty_years': 3,
                'grid_connection': 'LV 400V + DC conversion',
                'communication': 'OCPP 1.6J',
                'v2g_capable': False,
                'global_installations': 35000,
                'vehicles_supported': 2
            },
            'ChargePoint_CT4000': {
                'name': 'ChargePoint CT4000',
                'manufacturer': 'ChargePoint',
                'type': 'AC_Standard',
                'max_power_kw': 7.4,
                'connector_type': 'Type 2',
                'installation_cost_mad': 28000,
                'operational_cost_mad_month': 650,
                'efficiency': 0.91,
                'warranty_years': 3,
                'grid_connection': 'LV 230V AC',
                'communication': 'OCPP 1.6J',
                'v2g_capable': False,
                'global_installations': 150000,
                'vehicles_supported': 1
            },

            # Schneider Electric Series
            'Schneider_EVlink_Pro_AC': {
                'name': 'Schneider EVlink Pro AC',
                'manufacturer': 'Schneider Electric',
                'type': 'AC_Fast',
                'max_power_kw': 22,
                'connector_type': 'Type 2',
                'installation_cost_mad': 55000,
                'operational_cost_mad_month': 1200,
                'efficiency': 0.91,
                'warranty_years': 3,
                'grid_connection': 'LV 400V AC',
                'communication': 'OCPP 1.6J',
                'v2g_capable': False,
                'global_installations': 120000,
                'vehicles_supported': 1
            },
            'Schneider_EVlink_DC': {
                'name': 'Schneider EVlink DC',
                'manufacturer': 'Schneider Electric',
                'type': 'DC_Fast',
                'max_power_kw': 90,
                'connector_type': 'CCS2 + CHAdeMO',
                'installation_cost_mad': 220000,
                'operational_cost_mad_month': 4200,
                'efficiency': 0.94,
                'warranty_years': 4,
                'grid_connection': 'LV 400V + DC conversion',
                'communication': 'OCPP 2.0',
                'v2g_capable': False,
                'global_installations': 18000,
                'vehicles_supported': 2
            },

            # Siemens VersiCharge Series
            'Siemens_VersiCharge_UC100': {
                'name': 'Siemens VersiCharge UC100',
                'manufacturer': 'Siemens',
                'type': 'DC_Fast',
                'max_power_kw': 100,
                'connector_type': 'CCS2 + CHAdeMO',
                'installation_cost_mad': 280000,
                'operational_cost_mad_month': 5200,
                'efficiency': 0.94,
                'warranty_years': 4,
                'grid_connection': 'LV 400V + DC conversion',
                'communication': 'OCPP 2.0',
                'v2g_capable': True,
                'global_installations': 12000,
                'vehicles_supported': 2
            },
            'Siemens_VersiCharge_AC': {
                'name': 'Siemens VersiCharge AC',
                'manufacturer': 'Siemens',
                'type': 'AC_Fast',
                'max_power_kw': 11,
                'connector_type': 'Type 2',
                'installation_cost_mad': 42000,
                'operational_cost_mad_month': 950,
                'efficiency': 0.92,
                'warranty_years': 4,
                'grid_connection': 'LV 400V AC',
                'communication': 'OCPP 1.6J',
                'v2g_capable': False,
                'global_installations': 45000,
                'vehicles_supported': 1
            },

            # I-Smart Morocco Series (Local)
            'ISmart_AC22': {
                'name': 'I-Smart AC22 Morocco',
                'manufacturer': 'I-Smart Morocco',
                'type': 'AC_Fast',
                'max_power_kw': 22,
                'connector_type': 'Type 2',
                'installation_cost_mad': 48000,
                'operational_cost_mad_month': 1100,
                'efficiency': 0.92,
                'warranty_years': 3,
                'grid_connection': 'LV 400V AC',
                'communication': 'OCPP 1.6J',
                'v2g_capable': False,
                'global_installations': 2500,
                'vehicles_supported': 1
            },
            'ISmart_DC50': {
                'name': 'I-Smart DC50 Morocco',
                'manufacturer': 'I-Smart Morocco',
                'type': 'DC_Fast',
                'max_power_kw': 50,
                'connector_type': 'CCS2 + CHAdeMO',
                'installation_cost_mad': 180000,
                'operational_cost_mad_month': 3500,
                'efficiency': 0.94,
                'warranty_years': 4,
                'grid_connection': 'LV 400V + DC conversion',
                'communication': 'OCPP 2.0',
                'v2g_capable': True,
                'global_installations': 800,
                'vehicles_supported': 2
            },
            'ISmart_V2G_Bidirectional': {
                'name': 'I-Smart V2G Bidirectional',
                'manufacturer': 'I-Smart Morocco',
                'type': 'V2G_Bidirectional',
                'max_power_kw': 75,
                'connector_type': 'CCS2 Bidirectional',
                'installation_cost_mad': 280000,
                'operational_cost_mad_month': 5500,
                'efficiency': 0.93,
                'warranty_years': 5,
                'grid_connection': 'LV 400V Bidirectional',
                'communication': 'OCPP 2.0.1 + V2G Protocol',
                'v2g_capable': True,
                'global_installations': 200,
                'vehicles_supported': 2
            }
        }

class ComprehensiveEVModels:
    """Comprehensive Global EV Models Database"""

    @staticmethod
    def get_ev_models():
        return {
            # Tesla Models
            'Tesla_Model_3': {
                'name': 'Tesla Model 3',
                'manufacturer': 'Tesla',
                'category': 'Premium Sedan',
                'battery_capacity_kwh': 57.5,
                'usable_capacity_kwh': 53.5,
                'range_km': 448,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 170,
                'max_discharge_power_kw': 11,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 15.8,
                'v2g_capable': True,
                'price_mad': 450000,
                'market_share_morocco': 2.8,
                'charging_efficiency': 0.90,
                'discharging_efficiency': 0.88,
                'fast_charge_time_min': 28,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Tesla_Model_Y': {
                'name': 'Tesla Model Y',
                'manufacturer': 'Tesla',
                'category': 'Premium SUV',
                'battery_capacity_kwh': 75.0,
                'usable_capacity_kwh': 70.0,
                'range_km': 533,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 250,
                'max_discharge_power_kw': 11,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 16.9,
                'v2g_capable': True,
                'price_mad': 580000,
                'market_share_morocco': 1.5,
                'charging_efficiency': 0.91,
                'discharging_efficiency': 0.89,
                'fast_charge_time_min': 25,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Tesla_Model_S': {
                'name': 'Tesla Model S',
                'manufacturer': 'Tesla',
                'category': 'Luxury Sedan',
                'battery_capacity_kwh': 100.0,
                'usable_capacity_kwh': 95.0,
                'range_km': 652,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 250,
                'max_discharge_power_kw': 11,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 18.1,
                'v2g_capable': True,
                'price_mad': 950000,
                'market_share_morocco': 0.3,
                'charging_efficiency': 0.92,
                'discharging_efficiency': 0.90,
                'fast_charge_time_min': 22,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },

            # Volkswagen Group
            'Volkswagen_ID3': {
                'name': 'Volkswagen ID.3',
                'manufacturer': 'Volkswagen',
                'category': 'Compact Hatchback',
                'battery_capacity_kwh': 58.0,
                'usable_capacity_kwh': 54.0,
                'range_km': 426,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 120,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 15.4,
                'v2g_capable': False,
                'price_mad': 380000,
                'market_share_morocco': 4.2,
                'charging_efficiency': 0.89,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 35,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Volkswagen_ID4': {
                'name': 'Volkswagen ID.4',
                'manufacturer': 'Volkswagen',
                'category': 'Compact SUV',
                'battery_capacity_kwh': 77.0,
                'usable_capacity_kwh': 72.0,
                'range_km': 520,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 135,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 16.8,
                'v2g_capable': False,
                'price_mad': 480000,
                'market_share_morocco': 2.1,
                'charging_efficiency': 0.90,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 38,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },

            # Renault Group
            'Dacia_Spring': {
                'name': 'Dacia Spring',
                'manufacturer': 'Dacia',
                'category': 'City Car',
                'battery_capacity_kwh': 27.4,
                'usable_capacity_kwh': 25.5,
                'range_km': 230,
                'max_ac_charge_power_kw': 7.4,
                'max_dc_charge_power_kw': 30,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 13.9,
                'v2g_capable': False,
                'price_mad': 180000,
                'market_share_morocco': 18.7,
                'charging_efficiency': 0.84,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 56,
                'warranty_years': 8,
                'battery_chemistry': 'LFP'
            },
            'Renault_Zoe': {
                'name': 'Renault Zoe',
                'manufacturer': 'Renault',
                'category': 'Compact Hatchback',
                'battery_capacity_kwh': 52.0,
                'usable_capacity_kwh': 48.5,
                'range_km': 395,
                'max_ac_charge_power_kw': 22,
                'max_dc_charge_power_kw': 50,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 17.2,
                'v2g_capable': False,
                'price_mad': 280000,
                'market_share_morocco': 12.3,
                'charging_efficiency': 0.86,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 65,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },

            # Nissan
            'Nissan_Leaf': {
                'name': 'Nissan Leaf',
                'manufacturer': 'Nissan',
                'category': 'Compact Hatchback',
                'battery_capacity_kwh': 40.0,
                'usable_capacity_kwh': 37.0,
                'range_km': 270,
                'max_ac_charge_power_kw': 6.6,
                'max_dc_charge_power_kw': 46,
                'max_discharge_power_kw': 6.0,
                'connector_type': 'Type 2 + CHAdeMO',
                'energy_consumption_kwh_100km': 17.1,
                'v2g_capable': True,
                'price_mad': 320000,
                'market_share_morocco': 8.5,
                'charging_efficiency': 0.85,
                'discharging_efficiency': 0.83,
                'fast_charge_time_min': 60,
                'warranty_years': 8,
                'battery_chemistry': 'LMO'
            },

            # Hyundai/Kia Group
            'Hyundai_Kona_Electric': {
                'name': 'Hyundai Kona Electric',
                'manufacturer': 'Hyundai',
                'category': 'Compact SUV',
                'battery_capacity_kwh': 64.0,
                'usable_capacity_kwh': 59.5,
                'range_km': 449,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 77,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 15.9,
                'v2g_capable': False,
                'price_mad': 390000,
                'market_share_morocco': 3.8,
                'charging_efficiency': 0.87,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 47,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Hyundai_Ioniq5': {
                'name': 'Hyundai Ioniq 5',
                'manufacturer': 'Hyundai',
                'category': 'Premium SUV',
                'battery_capacity_kwh': 72.6,
                'usable_capacity_kwh': 68.0,
                'range_km': 481,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 235,
                'max_discharge_power_kw': 3.6,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 16.7,
                'v2g_capable': True,
                'price_mad': 520000,
                'market_share_morocco': 1.2,
                'charging_efficiency': 0.92,
                'discharging_efficiency': 0.90,
                'fast_charge_time_min': 18,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Kia_EV6': {
                'name': 'Kia EV6',
                'manufacturer': 'Kia',
                'category': 'Premium SUV',
                'battery_capacity_kwh': 77.4,
                'usable_capacity_kwh': 72.0,
                'range_km': 528,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 240,
                'max_discharge_power_kw': 3.6,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 16.5,
                'v2g_capable': True,
                'price_mad': 550000,
                'market_share_morocco': 0.9,
                'charging_efficiency': 0.93,
                'discharging_efficiency': 0.91,
                'fast_charge_time_min': 18,
                'warranty_years': 7,
                'battery_chemistry': 'NCM'
            },

            # Chinese Brands
            'BYD_Atto_3': {
                'name': 'BYD Atto 3',
                'manufacturer': 'BYD',
                'category': 'Compact SUV',
                'battery_capacity_kwh': 60.5,
                'usable_capacity_kwh': 57.0,
                'range_km': 420,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 88,
                'max_discharge_power_kw': 3.3,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 15.8,
                'v2g_capable': True,
                'price_mad': 350000,
                'market_share_morocco': 2.8,
                'charging_efficiency': 0.88,
                'discharging_efficiency': 0.86,
                'fast_charge_time_min': 45,
                'warranty_years': 6,
                'battery_chemistry': 'LFP'
            },
            'MG_ZS_EV': {
                'name': 'MG ZS EV',
                'manufacturer': 'MG',
                'category': 'Compact SUV',
                'battery_capacity_kwh': 51.1,
                'usable_capacity_kwh': 47.5,
                'range_km': 320,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 76,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 17.3,
                'v2g_capable': False,
                'price_mad': 290000,
                'market_share_morocco': 4.1,
                'charging_efficiency': 0.86,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 40,
                'warranty_years': 7,
                'battery_chemistry': 'NCM'
            },

            # Additional Tesla Models
            'Tesla_Model_X': {
                'name': 'Tesla Model X',
                'manufacturer': 'Tesla',
                'category': 'Luxury SUV',
                'battery_capacity_kwh': 100.0,
                'usable_capacity_kwh': 95.0,
                'range_km': 560,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 250,
                'max_discharge_power_kw': 11,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 20.8,
                'v2g_capable': True,
                'price_mad': 1200000,
                'market_share_morocco': 0.1,
                'charging_efficiency': 0.92,
                'discharging_efficiency': 0.90,
                'fast_charge_time_min': 20,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Tesla_Cybertruck': {
                'name': 'Tesla Cybertruck',
                'manufacturer': 'Tesla',
                'category': 'Electric Pickup',
                'battery_capacity_kwh': 123.0,
                'usable_capacity_kwh': 115.0,
                'range_km': 547,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 250,
                'max_discharge_power_kw': 11,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 23.5,
                'v2g_capable': True,
                'price_mad': 1100000,
                'market_share_morocco': 0.05,
                'charging_efficiency': 0.91,
                'discharging_efficiency': 0.89,
                'fast_charge_time_min': 18,
                'warranty_years': 8,
                'battery_chemistry': 'LFP'
            },

            # More Volkswagen Group
            'Volkswagen_ID5': {
                'name': 'Volkswagen ID.5',
                'manufacturer': 'Volkswagen',
                'category': 'Premium SUV',
                'battery_capacity_kwh': 77.0,
                'usable_capacity_kwh': 72.0,
                'range_km': 520,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 135,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 17.2,
                'v2g_capable': False,
                'price_mad': 520000,
                'market_share_morocco': 1.8,
                'charging_efficiency': 0.90,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 36,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Volkswagen_ID_Buzz': {
                'name': 'Volkswagen ID.Buzz',
                'manufacturer': 'Volkswagen',
                'category': 'Electric Van',
                'battery_capacity_kwh': 77.0,
                'usable_capacity_kwh': 72.0,
                'range_km': 423,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 170,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 19.5,
                'v2g_capable': False,
                'price_mad': 580000,
                'market_share_morocco': 0.3,
                'charging_efficiency': 0.89,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 30,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Audi_Q4_e_tron': {
                'name': 'Audi Q4 e-tron',
                'manufacturer': 'Audi',
                'category': 'Premium SUV',
                'battery_capacity_kwh': 76.6,
                'usable_capacity_kwh': 72.0,
                'range_km': 520,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 125,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 17.8,
                'v2g_capable': False,
                'price_mad': 680000,
                'market_share_morocco': 0.6,
                'charging_efficiency': 0.91,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 38,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Porsche_Taycan': {
                'name': 'Porsche Taycan',
                'manufacturer': 'Porsche',
                'category': 'Luxury Sports',
                'battery_capacity_kwh': 93.4,
                'usable_capacity_kwh': 83.7,
                'range_km': 484,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 270,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 19.6,
                'v2g_capable': False,
                'price_mad': 1400000,
                'market_share_morocco': 0.02,
                'charging_efficiency': 0.94,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 22,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Skoda_Enyaq': {
                'name': 'Škoda Enyaq iV',
                'manufacturer': 'Škoda',
                'category': 'Compact SUV',
                'battery_capacity_kwh': 77.0,
                'usable_capacity_kwh': 72.0,
                'range_km': 534,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 125,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 16.7,
                'v2g_capable': False,
                'price_mad': 450000,
                'market_share_morocco': 1.2,
                'charging_efficiency': 0.89,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 38,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },

            # More Stellantis Group
            'Peugeot_e208': {
                'name': 'Peugeot e-208',
                'manufacturer': 'Peugeot',
                'category': 'Compact Hatchback',
                'battery_capacity_kwh': 50.0,
                'usable_capacity_kwh': 46.5,
                'range_km': 362,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 100,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 16.1,
                'v2g_capable': False,
                'price_mad': 320000,
                'market_share_morocco': 5.8,
                'charging_efficiency': 0.87,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 30,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Peugeot_e308': {
                'name': 'Peugeot e-308',
                'manufacturer': 'Peugeot',
                'category': 'Compact Hatchback',
                'battery_capacity_kwh': 54.0,
                'usable_capacity_kwh': 51.0,
                'range_km': 412,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 100,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 15.8,
                'v2g_capable': False,
                'price_mad': 380000,
                'market_share_morocco': 3.2,
                'charging_efficiency': 0.88,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 32,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Fiat_500e': {
                'name': 'Fiat 500e',
                'manufacturer': 'Fiat',
                'category': 'City Car',
                'battery_capacity_kwh': 42.0,
                'usable_capacity_kwh': 37.3,
                'range_km': 320,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 85,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 14.9,
                'v2g_capable': False,
                'price_mad': 280000,
                'market_share_morocco': 2.1,
                'charging_efficiency': 0.85,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 35,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Jeep_Avenger_4xe': {
                'name': 'Jeep Avenger 4xe',
                'manufacturer': 'Jeep',
                'category': 'Compact SUV',
                'battery_capacity_kwh': 54.0,
                'usable_capacity_kwh': 51.0,
                'range_km': 400,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 100,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 16.8,
                'v2g_capable': False,
                'price_mad': 420000,
                'market_share_morocco': 1.5,
                'charging_efficiency': 0.87,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 32,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },

            # More BMW Group
            'BMW_i4': {
                'name': 'BMW i4',
                'manufacturer': 'BMW',
                'category': 'Premium Sedan',
                'battery_capacity_kwh': 83.9,
                'usable_capacity_kwh': 80.7,
                'range_km': 590,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 200,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 16.1,
                'v2g_capable': False,
                'price_mad': 720000,
                'market_share_morocco': 0.4,
                'charging_efficiency': 0.92,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 31,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'BMW_iX': {
                'name': 'BMW iX',
                'manufacturer': 'BMW',
                'category': 'Luxury SUV',
                'battery_capacity_kwh': 111.5,
                'usable_capacity_kwh': 105.2,
                'range_km': 630,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 200,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 19.8,
                'v2g_capable': False,
                'price_mad': 1100000,
                'market_share_morocco': 0.1,
                'charging_efficiency': 0.93,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 39,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'MINI_Cooper_SE': {
                'name': 'MINI Cooper SE',
                'manufacturer': 'MINI',
                'category': 'Premium Hatchback',
                'battery_capacity_kwh': 32.6,
                'usable_capacity_kwh': 28.9,
                'range_km': 233,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 50,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 15.2,
                'v2g_capable': False,
                'price_mad': 380000,
                'market_share_morocco': 0.8,
                'charging_efficiency': 0.86,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 36,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },

            # More Mercedes-Benz
            'Mercedes_EQB': {
                'name': 'Mercedes EQB',
                'manufacturer': 'Mercedes-Benz',
                'category': 'Premium SUV',
                'battery_capacity_kwh': 66.5,
                'usable_capacity_kwh': 62.0,
                'range_km': 423,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 112,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 17.9,
                'v2g_capable': False,
                'price_mad': 620000,
                'market_share_morocco': 0.7,
                'charging_efficiency': 0.90,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 32,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Mercedes_EQC': {
                'name': 'Mercedes EQC',
                'manufacturer': 'Mercedes-Benz',
                'category': 'Luxury SUV',
                'battery_capacity_kwh': 80.0,
                'usable_capacity_kwh': 74.0,
                'range_km': 471,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 110,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 19.7,
                'v2g_capable': False,
                'price_mad': 850000,
                'market_share_morocco': 0.3,
                'charging_efficiency': 0.91,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 40,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Mercedes_EQS': {
                'name': 'Mercedes EQS',
                'manufacturer': 'Mercedes-Benz',
                'category': 'Luxury Sedan',
                'battery_capacity_kwh': 107.8,
                'usable_capacity_kwh': 99.0,
                'range_km': 770,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 200,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 15.7,
                'v2g_capable': False,
                'price_mad': 1300000,
                'market_share_morocco': 0.05,
                'charging_efficiency': 0.94,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 31,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },

            # More Hyundai/Kia
            'Hyundai_Ioniq6': {
                'name': 'Hyundai Ioniq 6',
                'manufacturer': 'Hyundai',
                'category': 'Premium Sedan',
                'battery_capacity_kwh': 77.4,
                'usable_capacity_kwh': 72.6,
                'range_km': 614,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 235,
                'max_discharge_power_kw': 3.6,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 14.3,
                'v2g_capable': True,
                'price_mad': 580000,
                'market_share_morocco': 0.8,
                'charging_efficiency': 0.93,
                'discharging_efficiency': 0.91,
                'fast_charge_time_min': 18,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Kia_Niro_EV': {
                'name': 'Kia Niro EV',
                'manufacturer': 'Kia',
                'category': 'Compact SUV',
                'battery_capacity_kwh': 64.8,
                'usable_capacity_kwh': 60.0,
                'range_km': 460,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 77,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 16.2,
                'v2g_capable': False,
                'price_mad': 420000,
                'market_share_morocco': 1.8,
                'charging_efficiency': 0.88,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 43,
                'warranty_years': 7,
                'battery_chemistry': 'NCM'
            },
            'Genesis_GV60': {
                'name': 'Genesis GV60',
                'manufacturer': 'Genesis',
                'category': 'Luxury SUV',
                'battery_capacity_kwh': 77.4,
                'usable_capacity_kwh': 72.6,
                'range_km': 466,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 235,
                'max_discharge_power_kw': 3.6,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 18.1,
                'v2g_capable': True,
                'price_mad': 780000,
                'market_share_morocco': 0.1,
                'charging_efficiency': 0.92,
                'discharging_efficiency': 0.90,
                'fast_charge_time_min': 18,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },

            # More Chinese Brands
            'BYD_Han_EV': {
                'name': 'BYD Han EV',
                'manufacturer': 'BYD',
                'category': 'Premium Sedan',
                'battery_capacity_kwh': 85.4,
                'usable_capacity_kwh': 80.0,
                'range_km': 521,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 110,
                'max_discharge_power_kw': 3.3,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 17.2,
                'v2g_capable': True,
                'price_mad': 480000,
                'market_share_morocco': 1.2,
                'charging_efficiency': 0.89,
                'discharging_efficiency': 0.87,
                'fast_charge_time_min': 25,
                'warranty_years': 6,
                'battery_chemistry': 'LFP'
            },
            'BYD_Tang_EV': {
                'name': 'BYD Tang EV',
                'manufacturer': 'BYD',
                'category': 'Premium SUV',
                'battery_capacity_kwh': 86.4,
                'usable_capacity_kwh': 81.0,
                'range_km': 505,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 110,
                'max_discharge_power_kw': 3.3,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 18.9,
                'v2g_capable': True,
                'price_mad': 520000,
                'market_share_morocco': 0.8,
                'charging_efficiency': 0.88,
                'discharging_efficiency': 0.86,
                'fast_charge_time_min': 30,
                'warranty_years': 6,
                'battery_chemistry': 'LFP'
            },
            'NIO_ET7': {
                'name': 'NIO ET7',
                'manufacturer': 'NIO',
                'category': 'Luxury Sedan',
                'battery_capacity_kwh': 100.0,
                'usable_capacity_kwh': 94.0,
                'range_km': 580,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 125,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 17.8,
                'v2g_capable': False,
                'price_mad': 680000,
                'market_share_morocco': 0.2,
                'charging_efficiency': 0.91,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 20,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Xpeng_P7': {
                'name': 'Xpeng P7',
                'manufacturer': 'Xpeng',
                'category': 'Premium Sedan',
                'battery_capacity_kwh': 80.9,
                'usable_capacity_kwh': 76.0,
                'range_km': 562,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 120,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 15.6,
                'v2g_capable': False,
                'price_mad': 450000,
                'market_share_morocco': 0.3,
                'charging_efficiency': 0.90,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 31,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'MG_Marvel_R': {
                'name': 'MG Marvel R',
                'manufacturer': 'MG',
                'category': 'Premium SUV',
                'battery_capacity_kwh': 70.0,
                'usable_capacity_kwh': 65.0,
                'range_km': 402,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 92,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 18.2,
                'v2g_capable': False,
                'price_mad': 420000,
                'market_share_morocco': 0.9,
                'charging_efficiency': 0.87,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 40,
                'warranty_years': 7,
                'battery_chemistry': 'NCM'
            },
            'MG_MG4': {
                'name': 'MG MG4',
                'manufacturer': 'MG',
                'category': 'Compact Hatchback',
                'battery_capacity_kwh': 64.0,
                'usable_capacity_kwh': 61.0,
                'range_km': 450,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 117,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 16.8,
                'v2g_capable': False,
                'price_mad': 320000,
                'market_share_morocco': 2.8,
                'charging_efficiency': 0.88,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 35,
                'warranty_years': 7,
                'battery_chemistry': 'LFP'
            },

            # Japanese Brands
            'Nissan_Ariya': {
                'name': 'Nissan Ariya',
                'manufacturer': 'Nissan',
                'category': 'Premium SUV',
                'battery_capacity_kwh': 87.0,
                'usable_capacity_kwh': 82.0,
                'range_km': 533,
                'max_ac_charge_power_kw': 22,
                'max_dc_charge_power_kw': 130,
                'max_discharge_power_kw': 9.0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 17.6,
                'v2g_capable': True,
                'price_mad': 580000,
                'market_share_morocco': 1.5,
                'charging_efficiency': 0.89,
                'discharging_efficiency': 0.87,
                'fast_charge_time_min': 35,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Toyota_bZ4X': {
                'name': 'Toyota bZ4X',
                'manufacturer': 'Toyota',
                'category': 'Compact SUV',
                'battery_capacity_kwh': 71.4,
                'usable_capacity_kwh': 67.0,
                'range_km': 516,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 150,
                'max_discharge_power_kw': 1.5,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 16.1,
                'v2g_capable': True,
                'price_mad': 520000,
                'market_share_morocco': 1.1,
                'charging_efficiency': 0.88,
                'discharging_efficiency': 0.85,
                'fast_charge_time_min': 30,
                'warranty_years': 8,
                'battery_chemistry': 'LFP'
            },
            'Lexus_UX300e': {
                'name': 'Lexus UX 300e',
                'manufacturer': 'Lexus',
                'category': 'Luxury SUV',
                'battery_capacity_kwh': 72.8,
                'usable_capacity_kwh': 68.0,
                'range_km': 450,
                'max_ac_charge_power_kw': 6.6,
                'max_dc_charge_power_kw': 50,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CHAdeMO',
                'energy_consumption_kwh_100km': 17.2,
                'v2g_capable': False,
                'price_mad': 680000,
                'market_share_morocco': 0.2,
                'charging_efficiency': 0.86,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 80,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Mazda_MX30': {
                'name': 'Mazda MX-30',
                'manufacturer': 'Mazda',
                'category': 'Compact SUV',
                'battery_capacity_kwh': 35.5,
                'usable_capacity_kwh': 32.0,
                'range_km': 200,
                'max_ac_charge_power_kw': 6.6,
                'max_dc_charge_power_kw': 50,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 18.0,
                'v2g_capable': False,
                'price_mad': 380000,
                'market_share_morocco': 0.4,
                'charging_efficiency': 0.84,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 36,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },

            # American Brands
            'Ford_F150_Lightning': {
                'name': 'Ford F-150 Lightning',
                'manufacturer': 'Ford',
                'category': 'Electric Pickup',
                'battery_capacity_kwh': 131.0,
                'usable_capacity_kwh': 123.0,
                'range_km': 515,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 155,
                'max_discharge_power_kw': 9.6,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 25.7,
                'v2g_capable': True,
                'price_mad': 980000,
                'market_share_morocco': 0.1,
                'charging_efficiency': 0.89,
                'discharging_efficiency': 0.87,
                'fast_charge_time_min': 41,
                'warranty_years': 8,
                'battery_chemistry': 'LFP'
            },
            'Chevrolet_Bolt_EV': {
                'name': 'Chevrolet Bolt EV',
                'manufacturer': 'Chevrolet',
                'category': 'Compact Hatchback',
                'battery_capacity_kwh': 65.0,
                'usable_capacity_kwh': 60.0,
                'range_km': 417,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 55,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 16.9,
                'v2g_capable': False,
                'price_mad': 380000,
                'market_share_morocco': 0.6,
                'charging_efficiency': 0.86,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 60,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },
            'Cadillac_Lyriq': {
                'name': 'Cadillac Lyriq',
                'manufacturer': 'Cadillac',
                'category': 'Luxury SUV',
                'battery_capacity_kwh': 102.0,
                'usable_capacity_kwh': 95.0,
                'range_km': 502,
                'max_ac_charge_power_kw': 11,
                'max_dc_charge_power_kw': 190,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2 + CCS2',
                'energy_consumption_kwh_100km': 20.1,
                'v2g_capable': False,
                'price_mad': 850000,
                'market_share_morocco': 0.05,
                'charging_efficiency': 0.91,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 32,
                'warranty_years': 8,
                'battery_chemistry': 'NCM'
            },

            # HYBRID VEHICLES
            # Toyota Hybrids
            'Toyota_Prius_Hybrid': {
                'name': 'Toyota Prius Hybrid',
                'manufacturer': 'Toyota',
                'category': 'Hybrid Sedan',
                'battery_capacity_kwh': 1.3,
                'usable_capacity_kwh': 1.0,
                'range_km': 1200,
                'max_ac_charge_power_kw': 0,
                'max_dc_charge_power_kw': 0,
                'max_discharge_power_kw': 0,
                'connector_type': 'No Charging Port',
                'energy_consumption_kwh_100km': 4.3,
                'v2g_capable': False,
                'price_mad': 280000,
                'market_share_morocco': 8.5,
                'charging_efficiency': 0.0,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 0,
                'warranty_years': 8,
                'battery_chemistry': 'NiMH'
            },
            'Toyota_Corolla_Hybrid': {
                'name': 'Toyota Corolla Hybrid',
                'manufacturer': 'Toyota',
                'category': 'Hybrid Sedan',
                'battery_capacity_kwh': 1.3,
                'usable_capacity_kwh': 1.0,
                'range_km': 1100,
                'max_ac_charge_power_kw': 0,
                'max_dc_charge_power_kw': 0,
                'max_discharge_power_kw': 0,
                'connector_type': 'No Charging Port',
                'energy_consumption_kwh_100km': 4.5,
                'v2g_capable': False,
                'price_mad': 250000,
                'market_share_morocco': 12.3,
                'charging_efficiency': 0.0,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 0,
                'warranty_years': 8,
                'battery_chemistry': 'NiMH'
            },
            'Toyota_RAV4_Hybrid': {
                'name': 'Toyota RAV4 Hybrid',
                'manufacturer': 'Toyota',
                'category': 'Hybrid SUV',
                'battery_capacity_kwh': 1.6,
                'usable_capacity_kwh': 1.2,
                'range_km': 950,
                'max_ac_charge_power_kw': 0,
                'max_dc_charge_power_kw': 0,
                'max_discharge_power_kw': 0,
                'connector_type': 'No Charging Port',
                'energy_consumption_kwh_100km': 5.2,
                'v2g_capable': False,
                'price_mad': 380000,
                'market_share_morocco': 6.8,
                'charging_efficiency': 0.0,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 0,
                'warranty_years': 8,
                'battery_chemistry': 'NiMH'
            },

            # Plug-in Hybrids (PHEV)
            'Toyota_Prius_Prime': {
                'name': 'Toyota Prius Prime',
                'manufacturer': 'Toyota',
                'category': 'PHEV Sedan',
                'battery_capacity_kwh': 13.6,
                'usable_capacity_kwh': 11.0,
                'range_km': 69,
                'max_ac_charge_power_kw': 3.3,
                'max_dc_charge_power_kw': 0,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2',
                'energy_consumption_kwh_100km': 16.8,
                'v2g_capable': False,
                'price_mad': 320000,
                'market_share_morocco': 2.1,
                'charging_efficiency': 0.85,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 0,
                'warranty_years': 8,
                'battery_chemistry': 'Li-ion'
            },
            'BMW_X5_xDrive45e': {
                'name': 'BMW X5 xDrive45e',
                'manufacturer': 'BMW',
                'category': 'PHEV SUV',
                'battery_capacity_kwh': 24.0,
                'usable_capacity_kwh': 21.0,
                'range_km': 87,
                'max_ac_charge_power_kw': 3.7,
                'max_dc_charge_power_kw': 0,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2',
                'energy_consumption_kwh_100km': 25.4,
                'v2g_capable': False,
                'price_mad': 780000,
                'market_share_morocco': 0.8,
                'charging_efficiency': 0.87,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 0,
                'warranty_years': 8,
                'battery_chemistry': 'Li-ion'
            },
            'Mercedes_GLE350de': {
                'name': 'Mercedes GLE 350de',
                'manufacturer': 'Mercedes-Benz',
                'category': 'PHEV SUV',
                'battery_capacity_kwh': 31.2,
                'usable_capacity_kwh': 28.0,
                'range_km': 106,
                'max_ac_charge_power_kw': 7.4,
                'max_dc_charge_power_kw': 0,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2',
                'energy_consumption_kwh_100km': 27.2,
                'v2g_capable': False,
                'price_mad': 850000,
                'market_share_morocco': 0.4,
                'charging_efficiency': 0.88,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 0,
                'warranty_years': 8,
                'battery_chemistry': 'Li-ion'
            },
            'Volvo_XC60_Recharge': {
                'name': 'Volvo XC60 Recharge',
                'manufacturer': 'Volvo',
                'category': 'PHEV SUV',
                'battery_capacity_kwh': 18.8,
                'usable_capacity_kwh': 16.0,
                'range_km': 81,
                'max_ac_charge_power_kw': 3.7,
                'max_dc_charge_power_kw': 0,
                'max_discharge_power_kw': 0,
                'connector_type': 'Type 2',
                'energy_consumption_kwh_100km': 21.5,
                'v2g_capable': False,
                'price_mad': 680000,
                'market_share_morocco': 0.6,
                'charging_efficiency': 0.86,
                'discharging_efficiency': 0.0,
                'fast_charge_time_min': 0,
                'warranty_years': 8,
                'battery_chemistry': 'Li-ion'
            }
        }

class PowerFlowEngine:
    """Real-Time Power Flow Analysis Engine with Physics-Based Models"""
    
    def __init__(self):
        self.last_update = datetime.now()
        self.morocco_grid_capacity = 12500  # MW
        self.current_scenario = "Baseline"
        self.fleet_data = {}
        self.optimization_results = {}
        self.simulation_results = {}
        self.system_state = {
            'grid_frequency': 50.0,
            'grid_voltage': 400.0,
            'total_load': 0.0,
            'pv_generation': 0.0,
            'v2g_discharge': 0.0,
            'system_efficiency': 0.92
        }
        self.time_series_data = []
        
    def get_scenarios(self):
        return {
            "Baseline": {
                "name": "Baseline – Reference Situation",
                "description": "Standard charging without optimization",
                "algorithm": "Standard Control",
                "objective": "Simple charging",
                "grid_efficiency": 0.85,
                "v2g_factor": 0.05,
                "cost_factor": 1.0,
                "pv_utilization": 0.70,
                "load_balancing": 0.60
            },
            "Scenario1": {
                "name": "Optimizing Grid Import Costs",
                "description": "MPC Heuristics to minimize grid costs",
                "algorithm": "Model Predictive Control + Heuristics",
                "objective": "Min Grid Import Cost",
                "grid_efficiency": 0.92,
                "v2g_factor": 0.35,
                "cost_factor": 0.65,
                "pv_utilization": 0.85,
                "load_balancing": 0.80
            },
            "Scenario2": {
                "name": "Optimizing Net Costs",
                "description": "Multi-Agent RL for optimal net costs",
                "algorithm": "Multi-Agent Reinforcement Learning",
                "objective": "Min Net Costs",
                "grid_efficiency": 0.90,
                "v2g_factor": 0.40,
                "cost_factor": 0.60,
                "pv_utilization": 0.88,
                "load_balancing": 0.85
            }
        }
    
    def update_fleet_data(self, vehicle_id, arrival_time, departure_time, target_soc, flex_time=2.0):
        """Update fleet data with input validation"""
        if target_soc > 1.0:
            target_soc = 1.0
        if target_soc < 0.1:
            target_soc = 0.1
            
        try:
            arrival_dt = datetime.strptime(arrival_time, "%H:%M")
            departure_dt = datetime.strptime(departure_time, "%H:%M")
            if departure_dt <= arrival_dt:
                departure_dt += timedelta(days=1)
        except:
            arrival_dt = datetime.strptime("08:00", "%H:%M")
            departure_dt = datetime.strptime("18:00", "%H:%M")
        
        current_soc = 0.2 + (hash(vehicle_id) % 100) / 100 * 0.5
        battery_capacity = 50
        charge_power = 7.5
        
        energy_needed = (target_soc - current_soc) * battery_capacity
        min_charging_duration = max(0.5, energy_needed / charge_power)
        
        available_time = (departure_dt - arrival_dt).total_seconds() / 3600
        
        v2g_eligible = (target_soc < 0.9) and (flex_time > 1.0) and (available_time > min_charging_duration + 2)
        
        self.fleet_data[vehicle_id] = {
            'arrival_time': arrival_time,
            'departure_time': departure_time,
            'target_soc': target_soc,
            'current_soc': current_soc,
            'flex_time': flex_time,
            'battery_capacity': battery_capacity,
            'charging_duration': min_charging_duration,
            'available_time': available_time,
            'v2g_eligible': v2g_eligible,
            'charging_feasible': available_time >= min_charging_duration,
            'remaining_time': max(0, available_time - min_charging_duration)
        }

class GridMonitoringSystem:
    """Professional Grid Monitoring System"""
    
    def __init__(self):
        self.last_update = datetime.now()
    
    def get_grid_parameters(self):
        """Get real-time grid parameters"""
        return {
            'phase_voltages': {
                'L1_voltage_v': np.random.normal(400, 5),
                'L2_voltage_v': np.random.normal(400, 5),
                'L3_voltage_v': np.random.normal(400, 5)
            },
            'phase_currents': {
                'L1_current_a': np.random.normal(50, 8),
                'L2_current_a': np.random.normal(52, 8),
                'L3_current_a': np.random.normal(48, 8)
            },
            'power_measurements': {
                'active_power_p_kw': np.random.normal(35, 5),
                'reactive_power_q_kvar': np.random.normal(8, 2),
                'apparent_power_s_kva': np.random.normal(36, 5)
            },
            'frequency_hz': np.random.normal(50.0, 0.02),
            'power_factor': np.random.uniform(0.92, 0.98),
            'thd_voltage_percent': np.random.uniform(2.1, 4.8),
            'thd_current_percent': np.random.uniform(3.2, 7.1)
        }

def initialize_cpo_session_state():
    """Initialize comprehensive CPO session state"""
    
    if 'cpo_system' not in st.session_state:
        st.session_state.cpo_system = {
            'active': False,
            'grid_zones': MoroccanGridData.get_grid_zones(),
            'charging_stations': GlobalChargingStations.get_station_models(),
            'ev_models': ComprehensiveEVModels.get_ev_models(),
            'onee_tariffs': MoroccanGridData.get_onee_tariffs(),
            'grid_monitoring': GridMonitoringSystem(),
            'power_flow_engine': PowerFlowEngine(),
            'regulation_active': False,
            'regulation_strength': 75,
            'regulation_mode': 'Automatic',
            'selected_scenario': 'Baseline'
        }

    if 'cpo_configuration' not in st.session_state:
        st.session_state.cpo_configuration = {
            'selected_zone': 'Casablanca',
            'station_config': {
                'Tesla_Supercharger_V3': 0,
                'Tesla_Supercharger_V4': 0,
                'ABB_Terra_360': 0,
                'ABB_Terra_184': 0,
                'ABB_Terra_AC': 0,
                'ChargePoint_Express_250': 0,
                'ChargePoint_CT4000': 0,
                'Schneider_EVlink_Pro_AC': 0,
                'Schneider_EVlink_DC': 0,
                'Siemens_VersiCharge_UC100': 0,
                'Siemens_VersiCharge_AC': 0,
                'ISmart_AC22': 0,
                'ISmart_DC50': 0,
                'ISmart_V2G_Bidirectional': 0
            },
            'fleet_size': 0,
            'fleet_composition': {},
            'tariff_scheme': 'residential',
            'revenue_target': 'Moderate (10-15%)',
            'operational_mode': 'Standard',
            'operating_mode': 'Balanced Operation',
            'pricing_strategy': 'Time-of-Use',
            'peak_management': 'Peak Shaving',
            'maintenance_mode': 'Predictive',
            'customer_priority': 'First Come First Served',
            'energy_preference': 'Mixed Sources',
            'notification_level': 'Important',
            'investment_strategy': 'Expansion Focus',
            'fleet_strategy': 'Hybrid Approach'
        }

def render_professional_header():
    """Render professional CPO dashboard header with real-time clock"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2rem; font-weight: bold;">FLEXGRID CPO</div>
                <div style="font-size: 1.5rem; opacity: 0.8;">Professional Management</div>
            </div>
            <div style="text-align: right;">
                <div id="real-time-clock" style="font-size: 1.2rem; font-weight: 600;">{current_time}</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Real-time Clock</div>
            </div>
        </div>
        <h1>FLEXGRID CPO – Real-Time Intelligent Dashboard for Ancillary Services</h1>
        <h2>Advanced EV Charging Station Management System</h2>
        <p>Global Infrastructure • Smart Grid Integration • Financial Analytics • Business Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

def render_professional_sidebar():
    """Enhanced Professional CPO Control Center Sidebar"""
    st.sidebar.markdown("## CPO Control Center")

    # Core System Controls
    st.sidebar.markdown("**Core System Controls:**")

    system_active = st.sidebar.checkbox(
        "System Active",
        value=st.session_state.cpo_system['active'],
        help="Activate/deactivate the entire CPO system"
    )
    st.session_state.cpo_system['active'] = system_active

    regulation_active = st.sidebar.checkbox(
        "Enable Smart Grid Regulation",
        value=st.session_state.cpo_system.get('regulation_active', False),
        help="Enable intelligent grid regulation and optimization",
        disabled=not system_active
    )
    st.session_state.cpo_system['regulation_active'] = regulation_active

    # Status indicators
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if system_active:
            st.success("System ON")
        else:
            st.error("System OFF")

    with col2:
        if regulation_active and system_active:
            st.success("Grid REG ON")
        else:
            st.warning("Grid REG OFF")

    st.sidebar.markdown("---")

    # CPO Business Preferences
    st.sidebar.markdown("**CPO Business Preferences:**")
    
    # Operating Mode
    operating_mode = st.sidebar.selectbox(
        "Operating Mode",
        ["Profit Maximization", "Grid Support Priority", "Customer Satisfaction", "Balanced Operation"],
        index=3,
        help="Define your primary business objective"
    )
    st.session_state.cpo_configuration['operating_mode'] = operating_mode
    
    # Pricing Strategy
    pricing_strategy = st.sidebar.selectbox(
        "Pricing Strategy",
        ["Dynamic Pricing", "Fixed Pricing", "Time-of-Use", "Demand-Based"],
        index=2,
        help="Choose your charging pricing model"
    )
    st.session_state.cpo_configuration['pricing_strategy'] = pricing_strategy
    
    # Peak Hour Management
    peak_management = st.sidebar.selectbox(
        "Peak Hour Management",
        ["Load Shifting", "Peak Shaving", "Demand Response", "No Management"],
        index=1,
        help="Strategy for managing peak demand periods"
    )
    st.session_state.cpo_configuration['peak_management'] = peak_management
    
    st.sidebar.markdown("---")
    
    # Fleet Configuration
    st.sidebar.markdown("**Fleet Configuration:**")
    fleet_size = st.sidebar.number_input(
        "Fleet Size",
        min_value=0,
        max_value=1000,
        value=st.session_state.cpo_configuration['fleet_size'],
        step=1,
        help="Enter the number of electric vehicles in your managed fleet"
    )
    st.session_state.cpo_configuration['fleet_size'] = fleet_size

    if fleet_size > 0:
        st.sidebar.success(f"Active Fleet: {fleet_size} vehicles")
    else:
        st.sidebar.warning("No fleet configured")
    
    # Fleet Management Strategy
    fleet_strategy = st.sidebar.selectbox(
        "Fleet Management Strategy",
        ["Centralized Control", "Distributed Management", "Hybrid Approach", "Autonomous Operation"],
        index=2,
        help="Strategy for managing EV fleet charging"
    )
    st.session_state.cpo_configuration['fleet_strategy'] = fleet_strategy

    st.sidebar.markdown("---")
    
    # Configuration Presets
    st.sidebar.markdown("**Configuration Presets:**")

    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.sidebar.button("Small CPO"):
            st.session_state.cpo_configuration['fleet_size'] = 35
            st.session_state.cpo_configuration['station_config']['Tesla_Supercharger_V3'] = 2
            st.session_state.cpo_configuration['station_config']['ISmart_AC22'] = 3
            st.session_state.cpo_configuration['station_config']['ISmart_DC50'] = 2
            st.session_state.cpo_configuration['operating_mode'] = "Customer Satisfaction"
            st.session_state.cpo_configuration['pricing_strategy'] = "Fixed Pricing"
            st.sidebar.success("Small CPO configuration applied!")

    with col2:
        if st.sidebar.button("Large CPO"):
            st.session_state.cpo_configuration['fleet_size'] = 150
            st.session_state.cpo_configuration['station_config']['Tesla_Supercharger_V3'] = 8
            st.session_state.cpo_configuration['station_config']['ABB_Terra_360'] = 6
            st.session_state.cpo_configuration['station_config']['ISmart_AC22'] = 10
            st.session_state.cpo_configuration['station_config']['ISmart_DC50'] = 8
            st.session_state.cpo_configuration['operating_mode'] = "Profit Maximization"
            st.session_state.cpo_configuration['pricing_strategy'] = "Dynamic Pricing"
            st.sidebar.success("Large CPO configuration applied!")
    
    # System Status Summary
    st.sidebar.markdown("---")
    st.sidebar.markdown("**System Status Summary:**")
    
    # Display current preferences summary
    st.sidebar.markdown(f"""
    **Current Configuration:**
    - Mode: {operating_mode}
    - Pricing: {pricing_strategy}
    - Peak Mgmt: {peak_management}
    - Fleet: {fleet_size} vehicles
    - Strategy: {fleet_strategy}
    """)

def render_main_executive_dashboard():
    """Main Executive Dashboard with Real-Time Power Flow Analysis"""
    st.header("Executive Dashboard - System Overview")

    st.markdown("""
    <div class="professional-alert">
        <h4>Executive Command Center</h4>
        <p>Comprehensive oversight of charging infrastructure and grid integration with real-time power flow analysis,
        AI demand forecasting, and operational intelligence for executive decision-making in global EV ecosystems.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get system configuration
    station_models = st.session_state.cpo_system['charging_stations']
    station_config = st.session_state.cpo_configuration['station_config']
    fleet_size = st.session_state.cpo_configuration['fleet_size']
    regulation_active = st.session_state.cpo_system.get('regulation_active', False)
    
    # Calculate total power capacity
    total_power_capacity = 0
    for station_id in station_models.keys():
        quantity = station_config.get(station_id, 0)
        power = station_models[station_id]['max_power_kw']
        total_power_capacity += quantity * power
    
    # Display Critical KPIs
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(f"""
        <div class="kpi-metric">
            <h4>Total Capacity</h4>
            <h3>{total_power_capacity:,.0f} kW</h3>
            <p>Installed Capacity</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_stations = sum(station_config.values())
        st.markdown(f"""
        <div class="kpi-metric">
            <h4>Total Stations</h4>
            <h3>{total_stations}</h3>
            <p>Deployed Stations</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-metric">
            <h4>Active Fleet</h4>
            <h3>{fleet_size}</h3>
            <p>Managed Vehicles</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        # Calculate non-EV loads (facility loads)
        current_hour = datetime.now().hour
        base_facility_load = total_power_capacity * 0.15  # 15% of charging capacity as facility base load
        
        # Time-based variation for facility loads
        if 8 <= current_hour <= 18:  # Business hours
            time_factor = 1.2 + 0.3 * np.sin(np.pi * (current_hour - 8) / 10)
        elif 18 <= current_hour <= 22:  # Evening peak
            time_factor = 1.4
        else:  # Night hours
            time_factor = 0.6
        
        non_ev_load = base_facility_load * time_factor
        st.markdown(f"""
        <div class="kpi-metric">
            <h4>Non-EV Load</h4>
            <h3>{non_ev_load:,.0f} kW</h3>
            <p>Other Facility Loads</p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        grid_stability = np.random.uniform(0.92, 0.98) if regulation_active else np.random.uniform(0.75, 0.85)
        st.markdown(f"""
        <div class="kpi-metric">
            <h4>Grid Stability</h4>
            <h3>{grid_stability:.3f}</h3>
            <p>Stability Index</p>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        daily_revenue = total_stations * 850 if total_stations > 0 else 0
        st.markdown(f"""
        <div class="kpi-metric">
            <h4>Daily Revenue</h4>
            <h3>{daily_revenue:,.0f} MAD</h3>
            <p>Estimated Revenue</p>
        </div>
        """, unsafe_allow_html=True)

    # Real-time Power Flow Analysis
    if regulation_active:
        st.subheader("Real-Time Power Flow Analysis")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1rem; border-radius: 8px; color: white; margin: 1rem 0;">
            <h4>Smart Grid Regulation ACTIVE</h4>
            <p>Real-time energy analysis with optimization engine</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate realistic power data
        hours = list(range(24))
        current_hour = datetime.now().hour
        
        # Charging power profile
        charging_power = []
        for h in hours:
            if 6 <= h <= 22:
                base_power = total_power_capacity * 0.4
                time_factor = 0.5 + 0.5 * np.sin(np.pi * (h - 6) / 16)
                charging_power.append(base_power * time_factor)
            else:
                charging_power.append(total_power_capacity * 0.1)
        
        # V2G power profile
        v2g_power = []
        for h in hours:
            if 18 <= h <= 22:  # Peak hours
                v2g_power.append(fleet_size * 0.3 * 8)  # 30% of fleet, 8kW average
            else:
                v2g_power.append(0)
        
        # PV generation
        pv_power = []
        for h in hours:
            if 6 <= h <= 18:
                pv_factor = np.sin(np.pi * (h - 6) / 12)
                pv_power.append(total_power_capacity * 0.2 * pv_factor)
            else:
                pv_power.append(0)
        
        # Non-EV facility loads (lighting, HVAC, offices, etc.)
        facility_loads = []
        for h in hours:
            base_load = total_power_capacity * 0.15  # 15% of charging capacity as base facility load
            if 8 <= h <= 18:  # Business hours
                time_factor = 1.2 + 0.3 * np.sin(np.pi * (h - 8) / 10)
            elif 18 <= h <= 22:  # Evening peak
                time_factor = 1.4
            else:  # Night hours
                time_factor = 0.6
            facility_loads.append(base_load * time_factor)
        
        # Grid power (total demand minus local generation)
        grid_power = [max(0, cp + fl - vp - pp) for cp, fl, vp, pp in zip(charging_power, facility_loads, v2g_power, pv_power)]
        
        # Power flow visualization
        fig_power = go.Figure()
        
        fig_power.add_trace(go.Scatter(
            x=hours, y=grid_power,
            mode='lines+markers',
            name='Grid Power (kW)',
            line=dict(color='#3b82f6', width=3)
        ))
        
        fig_power.add_trace(go.Scatter(
            x=hours, y=charging_power,
            mode='lines+markers',
            name='Charging Power (kW)',
            line=dict(color='#ef4444', width=3)
        ))
        
        fig_power.add_trace(go.Scatter(
            x=hours, y=v2g_power,
            mode='lines+markers',
            name='V2G Power (kW)',
            line=dict(color='#10b981', width=3)
        ))
        
        fig_power.add_trace(go.Scatter(
            x=hours, y=facility_loads,
            mode='lines+markers',
            name='Facility Loads (kW)',
            line=dict(color='#8b5cf6', width=3)
        ))
        
        fig_power.add_trace(go.Scatter(
            x=hours, y=pv_power,
            mode='lines+markers',
            name='PV Power (kW)',
            line=dict(color='#f59e0b', width=3),
            fill='tozeroy'
        ))
        
        fig_power.add_vline(x=current_hour, line_dash="dash", line_color="red", 
                           annotation_text=f"Now: {current_hour}:00")
        
        fig_power.update_layout(
            title="24h Power Curves - Intelligent Control",
            xaxis_title="Hour",
            yaxis_title="Power (kW)",
            height=500
        )
        
        st.plotly_chart(fig_power, use_container_width=True)
    else:
        st.warning("**Real-Time Power Flow Analysis INACTIVE**")
        st.info("**Enable 'Smart Grid Regulation' in the sidebar**")
    


def main():
    """Main application function"""
    # Initialize session state
    initialize_cpo_session_state()

    # Render header
    render_professional_header()

    # Render sidebar
    render_professional_sidebar()

    # Main navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Executive Dashboard",
        "Station Management", 
        "Fleet Analytics",
        "Grid Regulation",
        "Financial Analysis",
        "Future Roadmap"
    ])

    with tab1:
        render_main_executive_dashboard()

    with tab2:
        render_stations_configuration()

    with tab3:
        render_fleet_vehicles()

    with tab4:
        render_grid_regulation()

    with tab5:
        render_comprehensive_financial_analysis()

    with tab6:
        render_future_improvements_roadmap()

def render_stations_configuration():
    """Stations Configuration with Interactive Selection"""
    st.header("Station Management")
    st.markdown("""
    <div class="professional-alert">
        <h4>Charging Infrastructure Management</h4>
        <p>Interactive station selection and configuration interface.</p>
    </div>
    """, unsafe_allow_html=True)
    
    station_models = st.session_state.cpo_system['charging_stations']
    station_config = st.session_state.cpo_configuration['station_config']
    
    # Station Selection Interface
    st.subheader("Select Charging Station Model")
    
    # Group stations by manufacturer
    manufacturers = {}
    for station_id, specs in station_models.items():
        manufacturer = specs['manufacturer']
        if manufacturer not in manufacturers:
            manufacturers[manufacturer] = []
        manufacturers[manufacturer].append((station_id, specs))
    
    # Manufacturer selection
    selected_manufacturer = st.selectbox(
        "Choose Manufacturer",
        list(manufacturers.keys()),
        help="Select charging station manufacturer"
    )
    
    # Model selection within manufacturer
    available_models = manufacturers[selected_manufacturer]
    model_options = [f"{specs['name']} - {specs['max_power_kw']}kW ({specs['type']})" 
                    for station_id, specs in available_models]
    
    selected_model_idx = st.selectbox(
        "Choose Station Model",
        range(len(model_options)),
        format_func=lambda x: model_options[x],
        help="Select specific charging station model"
    )
    
    selected_station_id, selected_specs = available_models[selected_model_idx]
    
    # Display selected station details
    st.markdown("""
    <div class="charging-station-card">
        <h4>Selected Station Details</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Max Power", f"{selected_specs['max_power_kw']} kW")
        st.metric("Efficiency", f"{selected_specs['efficiency']*100:.1f}%")
        st.metric("Warranty", f"{selected_specs['warranty_years']} years")
    
    with col2:
        st.metric("Installation Cost", f"{selected_specs['installation_cost_mad']:,} MAD")
        st.metric("Monthly OpEx", f"{selected_specs['operational_cost_mad_month']:,} MAD")
        st.metric("Global Installs", f"{selected_specs['global_installations']:,}")
    
    with col3:
        st.write(f"**Type:** {selected_specs['type']}")
        st.write(f"**Connector:** {selected_specs['connector_type']}")
        st.write(f"**V2G Capable:** {'Yes' if selected_specs['v2g_capable'] else 'No'}")
        st.write(f"**Communication:** {selected_specs['communication']}")
    
    # Quantity configuration
    st.subheader("Station Quantity Configuration")
    
    current_qty = station_config.get(selected_station_id, 0)
    new_qty = st.number_input(
        f"Number of {selected_specs['name']} stations",
        min_value=0,
        max_value=50,
        value=current_qty,
        step=1,
        help="Configure the number of stations to deploy"
    )
    
    if st.button("Update Station Configuration"):
        station_config[selected_station_id] = new_qty
        st.success(f"Configuration updated: {new_qty} x {selected_specs['name']}")
    
    # Current deployment summary
    st.subheader("Current Deployment Summary")
    
    deployed_stations = [(sid, specs, qty) for sid, specs in station_models.items() 
                        for qty in [station_config.get(sid, 0)] if qty > 0]
    
    if deployed_stations:
        summary_data = []
        total_stations = 0
        total_power = 0
        total_cost = 0
        
        for station_id, specs, qty in deployed_stations:
            power = qty * specs['max_power_kw']
            cost = qty * specs['installation_cost_mad']
            total_stations += qty
            total_power += power
            total_cost += cost
            
            summary_data.append({
                'Station Model': specs['name'],
                'Manufacturer': specs['manufacturer'],
                'Quantity': qty,
                'Total Power (kW)': f"{power:,}",
                'Installation Cost (MAD)': f"{cost:,}"
            })
        
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True)
        
        # Total metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Stations", total_stations)
        with col2:
            st.metric("Total Power", f"{total_power:,} kW")
        with col3:
            st.metric("Total Investment", f"{total_cost:,} MAD")
    else:
        st.info("No stations configured yet. Select and configure stations above.")

def render_fleet_vehicles():
    """Fleet Analytics with Real-Time Vehicle Status"""
    st.header("Fleet Analytics")
    st.markdown("""
    <div class="professional-alert">
        <h4>Fleet Analysis System</h4>
        <p>Real-time fleet monitoring and comprehensive EV management.</p>
    </div>
    """, unsafe_allow_html=True)
    
    fleet_size = st.session_state.cpo_configuration['fleet_size']
    power_flow_engine = st.session_state.cpo_system['power_flow_engine']
    ev_models = st.session_state.cpo_system['ev_models']
    
    if fleet_size > 0:
        # Real-Time Fleet Status Table
        st.subheader("Real-Time Fleet Status")
        
        # Initialize fleet status data with session state integration
        if 'fleet_status_data' not in st.session_state:
            st.session_state.fleet_status_data = []
        
        # Generate or update fleet data
        fleet_status_data = []
        current_time = datetime.now()
        
        # Get a diverse mix of EV models for the fleet
        popular_models = [
            ('Dacia_Spring', 'Dacia Spring'),
            ('Renault_Zoe', 'Renault Zoe'),
            ('Nissan_Leaf', 'Nissan Leaf'),
            ('Tesla_Model_3', 'Tesla Model 3'),
            ('Volkswagen_ID3', 'Volkswagen ID.3'),
            ('MG_ZS_EV', 'MG ZS EV'),
            ('Hyundai_Kona_Electric', 'Hyundai Kona Electric'),
            ('BYD_Atto_3', 'BYD Atto 3')
        ]
        
        for i in range(fleet_size):
            vehicle_id = f"EV-{i+1:03d}"
            
            # Initialize vehicle_configurations if not exists
            if 'vehicle_configurations' not in st.session_state:
                st.session_state.vehicle_configurations = {}
            
            # Check if vehicle has custom configuration
            if vehicle_id in st.session_state.vehicle_configurations:
                config = st.session_state.vehicle_configurations[vehicle_id]
                model_name = config['model']
                arrival_time = config['arrival_time']
                departure_time = config['departure_time']
                
                # Find model specs from configured model
                model_key = None
                for key, specs in ev_models.items():
                    if specs['name'] == model_name:
                        model_key = key
                        break
                if not model_key:
                    model_key = 'Dacia_Spring'
            else:
                # Assign model based on market share distribution
                if i < fleet_size * 0.25:  # 25% Dacia Spring (most popular)
                    model_key, model_name = popular_models[0]
                elif i < fleet_size * 0.40:  # 15% Renault Zoe
                    model_key, model_name = popular_models[1]
                elif i < fleet_size * 0.52:  # 12% Nissan Leaf
                    model_key, model_name = popular_models[2]
                elif i < fleet_size * 0.60:  # 8% Tesla Model 3
                    model_key, model_name = popular_models[3]
                elif i < fleet_size * 0.70:  # 10% VW ID.3
                    model_key, model_name = popular_models[4]
                elif i < fleet_size * 0.80:  # 10% MG ZS EV
                    model_key, model_name = popular_models[5]
                elif i < fleet_size * 0.90:  # 10% Hyundai Kona
                    model_key, model_name = popular_models[6]
                else:  # 10% BYD Atto 3
                    model_key, model_name = popular_models[7]
                
                # Default times if not configured
                arrival_hour = np.random.randint(6, 10)
                departure_hour = np.random.randint(16, 20)
                arrival_time = f"{arrival_hour:02d}:{np.random.randint(0, 60):02d}"
                departure_time = f"{departure_hour:02d}:{np.random.randint(0, 60):02d}"
            
            model_specs = ev_models.get(model_key, ev_models['Dacia_Spring'])
            
            # Generate realistic status
            current_soc = np.random.uniform(0.15, 0.95)
            is_connected = np.random.choice([True, False], p=[0.3, 0.7])
            is_charging = is_connected and current_soc < 0.85 and np.random.choice([True, False], p=[0.7, 0.3])
            is_v2g_active = (model_specs['v2g_capable'] and is_connected and 
                           current_soc > 0.6 and np.random.choice([True, False], p=[0.2, 0.8]))
            
            # Status determination
            if is_charging:
                status = "Charging"
                status_color = "🔋"
            elif is_v2g_active:
                status = "V2G Active"
                status_color = "⚡"
            elif is_connected:
                status = "Connected"
                status_color = "🔌"
            else:
                status = "Disconnected"
                status_color = "📱"
            
            # Power flow
            if is_charging:
                power_kw = np.random.uniform(3.5, model_specs['max_ac_charge_power_kw'])
                power_flow = f"+{power_kw:.1f} kW"
            elif is_v2g_active:
                power_kw = np.random.uniform(2.0, model_specs.get('max_discharge_power_kw', 6.0))
                power_flow = f"-{power_kw:.1f} kW"
            else:
                power_flow = "0.0 kW"
            
            fleet_status_data.append({
                'Vehicle ID': vehicle_id,
                'Model': model_name,
                'Status': f"{status_color} {status}",
                'SOC (%)': f"{current_soc*100:.1f}%",
                'Battery (kWh)': f"{model_specs['battery_capacity_kwh']:.1f}",
                'V2G Capable': "✅" if model_specs['v2g_capable'] else "❌",
                'Power Flow': power_flow,
                'Arrival': arrival_time,
                'Departure': departure_time,
                'Connected': "✅" if is_connected else "❌"
            })
        
        # Store in session state for consistency
        st.session_state.fleet_status_data = fleet_status_data
        
        # Display fleet status table
        df_fleet_status = pd.DataFrame(fleet_status_data)
        st.dataframe(df_fleet_status, use_container_width=True)
        
        # Fleet Summary Metrics
        st.subheader("Fleet Summary Metrics")
        
        connected_vehicles = sum(1 for row in fleet_status_data if "✅" in row['Connected'])
        charging_vehicles = sum(1 for row in fleet_status_data if "Charging" in row['Status'])
        v2g_active_vehicles = sum(1 for row in fleet_status_data if "V2G Active" in row['Status'])
        v2g_capable_vehicles = sum(1 for row in fleet_status_data if "✅" in row['V2G Capable'])
        
        total_charging_power = sum(float(row['Power Flow'].replace(' kW', '').replace('+', '')) 
                                 for row in fleet_status_data if '+' in row['Power Flow'])
        total_v2g_power = sum(float(row['Power Flow'].replace(' kW', '').replace('-', '')) 
                            for row in fleet_status_data if '-' in row['Power Flow'])
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Connected", f"{connected_vehicles}/{fleet_size}", 
                     delta=f"{connected_vehicles/fleet_size*100:.1f}%")
        
        with col2:
            st.metric("Charging", charging_vehicles, 
                     delta=f"{total_charging_power:.1f} kW")
        
        with col3:
            st.metric("V2G Active", v2g_active_vehicles, 
                     delta=f"{total_v2g_power:.1f} kW")
        
        with col4:
            st.metric("V2G Capable", f"{v2g_capable_vehicles}/{fleet_size}", 
                     delta=f"{v2g_capable_vehicles/fleet_size*100:.1f}%")
        
        with col5:
            net_power = total_charging_power - total_v2g_power
            st.metric("Net Power", f"{net_power:.1f} kW", 
                     delta="Grid Import" if net_power > 0 else "Grid Export")
        
        # Individual Vehicle Configuration
        st.subheader("Individual Vehicle Configuration")
        
        # Initialize session state for vehicle configurations if not exists
        if 'vehicle_configurations' not in st.session_state:
            st.session_state.vehicle_configurations = {}
            # Initialize with current fleet data
            for row in fleet_status_data:
                vehicle_id = row['Vehicle ID']
                # Parse SOC safely and ensure it's within valid range
                try:
                    current_soc = float(row['SOC (%)'].replace('%', ''))
                    # Set target SOC slightly higher than current SOC, minimum 20%
                    target_soc = max(20.0, min(100.0, current_soc + 20.0))
                except (ValueError, AttributeError):
                    target_soc = 80.0
                
                st.session_state.vehicle_configurations[vehicle_id] = {
                    'model': row['Model'],
                    'arrival_time': row['Arrival'],
                    'departure_time': row['Departure'],
                    'target_soc': target_soc,
                    'flex_time': 2.0
                }
        
        vehicle_ids = [f"EV-{i+1:03d}" for i in range(fleet_size)]
        selected_vehicle = st.selectbox("Select Vehicle ID", vehicle_ids, key="vehicle_selector")
        
        # Find selected vehicle data
        selected_vehicle_data = next((row for row in fleet_status_data if row['Vehicle ID'] == selected_vehicle), None)
        
        if selected_vehicle_data:
            current_config = st.session_state.vehicle_configurations.get(selected_vehicle, {})
            
            st.info(f"**Current Status:** {selected_vehicle_data['Status']} | **SOC:** {selected_vehicle_data['SOC (%)']} | **Model:** {selected_vehicle_data['Model']}")
            
            # Model and Type Selection
            st.markdown("**Vehicle Model & Type Selection:**")
            col1, col2 = st.columns(2)
            
            with col1:
                # Get available EV models
                available_models = list(ev_models.keys())
                model_names = [ev_models[key]['name'] for key in available_models]
                
                # Find current model index
                current_model_name = current_config.get('model', selected_vehicle_data['Model'])
                try:
                    current_model_idx = model_names.index(current_model_name)
                except ValueError:
                    current_model_idx = 0
                
                selected_model_idx = st.selectbox(
                    "Select EV Model",
                    range(len(model_names)),
                    format_func=lambda x: f"{model_names[x]} ({ev_models[available_models[x]]['category']})",
                    index=current_model_idx,
                    key=f"model_selector_{selected_vehicle}"
                )
                
                selected_model_key = available_models[selected_model_idx]
                selected_model_specs = ev_models[selected_model_key]
                new_model_name = selected_model_specs['name']
            
            with col2:
                # Vehicle Type/Category
                st.selectbox(
                    "Vehicle Category",
                    [selected_model_specs['category']],
                    index=0,
                    disabled=True,
                    key=f"category_{selected_vehicle}"
                )
                
                # Display key specs
                st.write(f"**Battery:** {selected_model_specs['battery_capacity_kwh']} kWh")
                st.write(f"**Range:** {selected_model_specs['range_km']} km")
                st.write(f"**V2G:** {'✅' if selected_model_specs['v2g_capable'] else '❌'}")
            
            # Time Configuration
            st.markdown("**Schedule Configuration:**")
            col3, col4 = st.columns(2)
            
            with col3:
                # Parse current times or use defaults
                try:
                    current_arrival = datetime.strptime(current_config.get('arrival_time', '08:00'), "%H:%M").time()
                except:
                    current_arrival = datetime.strptime("08:00", "%H:%M").time()
                
                try:
                    current_departure = datetime.strptime(current_config.get('departure_time', '18:00'), "%H:%M").time()
                except:
                    current_departure = datetime.strptime("18:00", "%H:%M").time()
                
                arrival_time = st.time_input(
                    "Arrival Time", 
                    value=current_arrival,
                    key=f"arrival_{selected_vehicle}"
                )
                departure_time = st.time_input(
                    "Departure Time", 
                    value=current_departure,
                    key=f"departure_{selected_vehicle}"
                )
            
            with col4:
                # Ensure target SOC is within valid range
                current_target_soc = current_config.get('target_soc', 80.0)
                if current_target_soc < 20.0:
                    current_target_soc = 20.0
                elif current_target_soc > 100.0:
                    current_target_soc = 100.0
                
                target_soc_percent = st.number_input(
                    "Target SOC (%)", 
                    min_value=20.0,  # Reduced minimum to accommodate current SOC values
                    max_value=100.0, 
                    value=current_target_soc, 
                    step=0.1,
                    key=f"soc_{selected_vehicle}"
                )
                
                # Ensure flex time is within valid range
                current_flex_time = current_config.get('flex_time', 2.0)
                if current_flex_time < 0.5:
                    current_flex_time = 0.5
                elif current_flex_time > 8.0:
                    current_flex_time = 8.0
                
                flex_time = st.number_input(
                    "Flexible Time (hours)", 
                    min_value=0.5, 
                    max_value=8.0, 
                    value=current_flex_time, 
                    step=0.1,
                    key=f"flex_{selected_vehicle}"
                )
            
            # Real-time update when any parameter changes
            new_config = {
                'model': new_model_name,
                'arrival_time': arrival_time.strftime("%H:%M"),
                'departure_time': departure_time.strftime("%H:%M"),
                'target_soc': target_soc_percent,
                'flex_time': flex_time
            }
            
            # Real-time update when any parameter changes
            config_changed = (st.session_state.vehicle_configurations.get(selected_vehicle, {}) != new_config)
            
            if config_changed:
                # Update session state immediately
                st.session_state.vehicle_configurations[selected_vehicle] = new_config
                
                # Update power flow engine
                power_flow_engine.update_fleet_data(
                    selected_vehicle,
                    arrival_time.strftime("%H:%M"),
                    departure_time.strftime("%H:%M"),
                    target_soc_percent / 100,
                    flex_time
                )
                
                # Force immediate table update by triggering rerun
                st.rerun()
            
            # Professional confirmation button without balloons
            if st.button(f"🔄 Apply Configuration to {selected_vehicle}", key=f"update_{selected_vehicle}"):
                # Update configuration
                st.session_state.vehicle_configurations[selected_vehicle] = new_config
                power_flow_engine.update_fleet_data(
                    selected_vehicle,
                    arrival_time.strftime("%H:%M"),
                    departure_time.strftime("%H:%M"),
                    target_soc_percent / 100,
                    flex_time
                )
                st.success(f"✅ Configuration applied successfully for {selected_vehicle}")
                st.rerun()
        
        # Fleet Composition Analysis
        st.subheader("Fleet Composition Analysis")
        
        # Model distribution in current fleet
        model_counts = {}
        for row in fleet_status_data:
            model = row['Model']
            model_counts[model] = model_counts.get(model, 0) + 1
        
        composition_data = []
        for model, count in model_counts.items():
            percentage = (count / fleet_size) * 100
            composition_data.append({
                'Model': model,
                'Count': count,
                'Percentage': f"{percentage:.1f}%"
            })
        
        df_composition = pd.DataFrame(composition_data)
        df_composition = df_composition.sort_values('Count', ascending=False)
        st.dataframe(df_composition, use_container_width=True)
        
    else:
        st.info("Configure fleet size in the sidebar to access fleet management features")
        
        # Show available EV models even without fleet
        st.subheader("Available EV Models in Morocco")
        
        # Create summary table of all models
        all_models_data = []
        for model_id, specs in ev_models.items():
            all_models_data.append({
                'Model': specs['name'],
                'Manufacturer': specs['manufacturer'],
                'Category': specs['category'],
                'Battery (kWh)': specs['battery_capacity_kwh'],
                'Range (km)': specs['range_km'],
                'Price (MAD)': f"{specs['price_mad']:,}",
                'Market Share (%)': specs['market_share_morocco'],
                'V2G Capable': '✅' if specs['v2g_capable'] else '❌'
            })
        
        df_all_models = pd.DataFrame(all_models_data)
        df_all_models = df_all_models.sort_values('Market Share (%)', ascending=False)
        st.dataframe(df_all_models, use_container_width=True)

def render_grid_regulation():
    """Grid Regulation Control - Technical Parameters"""
    st.header("Grid Regulation & Power Quality")
    st.markdown("""
    <div class="professional-alert">
        <h4>Smart Grid Regulation System</h4>
        <p>Advanced grid regulation and power quality management. Financial benefits from grid services are detailed in the Financial Analysis section.</p>
    </div>
    """, unsafe_allow_html=True)
    
    regulation_active = st.session_state.cpo_system.get('regulation_active', False)
    fleet_size = st.session_state.cpo_configuration['fleet_size']
    
    if regulation_active:
        # Grid Services Status
        st.subheader("⚡ Grid Services Status")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Frequency Regulation", "49.98 Hz", delta="🟢 Active", help="Primary frequency response service")
        
        with col2:
            st.metric("Voltage Support", "400.2 V", delta="🟢 Active", help="Reactive power compensation service")
        
        with col3:
            st.metric("Peak Shaving", "92.1%", delta="+1.2 MW", help="Peak demand reduction service")
        
        with col4:
            st.metric("Grid Services", "Active", delta="💰 See Financial Analysis", help="Revenue details in Financial Analysis section")
        
        # Power Quality Monitoring
        st.subheader("⚡ Power Quality & Grid Health")
        
        # Generate realistic grid parameters
        current_time = datetime.now()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # THD and Power Quality Metrics
            thd_voltage = np.random.uniform(2.1, 4.2)
            thd_current = np.random.uniform(3.8, 6.5)
            power_factor = np.random.uniform(0.92, 0.98)
            
            st.markdown("**Power Quality Indicators:**")
            
            # THD Voltage
            thd_status = "🟢 Excellent" if thd_voltage < 3.0 else "🟡 Good" if thd_voltage < 4.0 else "🟠 Acceptable"
            st.metric("THD Voltage", f"{thd_voltage:.1f}%", delta=f"{thd_status}", help="Total Harmonic Distortion - Voltage")
            
            # THD Current
            thd_current_status = "🟢 Excellent" if thd_current < 5.0 else "🟡 Good" if thd_current < 7.0 else "🟠 Acceptable"
            st.metric("THD Current", f"{thd_current:.1f}%", delta=f"{thd_current_status}", help="Total Harmonic Distortion - Current")
            
            # Power Factor
            pf_status = "🟢 Optimal" if power_factor > 0.95 else "🟡 Good" if power_factor > 0.90 else "🟠 Needs Improvement"
            st.metric("Power Factor", f"{power_factor:.3f}", delta=f"{pf_status}", help="Power Factor - Efficiency indicator")
        
        with col2:
            # Grid Stability Metrics
            frequency = np.random.normal(50.0, 0.05)
            voltage_l1 = np.random.normal(400, 8)
            voltage_l2 = np.random.normal(400, 8)
            voltage_l3 = np.random.normal(400, 8)
            
            st.markdown("**Grid Stability Metrics:**")
            
            # Frequency
            freq_status = "🟢 Stable" if abs(frequency - 50.0) < 0.1 else "🟡 Monitoring"
            st.metric("Grid Frequency", f"{frequency:.2f} Hz", delta=f"{freq_status}", help="Grid frequency stability")
            
            # Voltage Balance
            voltage_avg = (voltage_l1 + voltage_l2 + voltage_l3) / 3
            voltage_imbalance = max(abs(voltage_l1 - voltage_avg), abs(voltage_l2 - voltage_avg), abs(voltage_l3 - voltage_avg)) / voltage_avg * 100
            balance_status = "🟢 Balanced" if voltage_imbalance < 1.0 else "🟡 Slight Imbalance" if voltage_imbalance < 2.0 else "🟠 Imbalanced"
            st.metric("Voltage Balance", f"{voltage_imbalance:.1f}%", delta=f"{balance_status}", help="Three-phase voltage balance")
            
            # Grid Efficiency
            grid_efficiency = np.random.uniform(0.94, 0.97)
            efficiency_status = "🟢 Excellent" if grid_efficiency > 0.95 else "🟡 Good"
            st.metric("Grid Efficiency", f"{grid_efficiency*100:.1f}%", delta=f"{efficiency_status}", help="Overall grid efficiency")
        
        # V2G Services Technical Status
        if fleet_size > 0:
            st.subheader("🔄 V2G Services Technical Status")
            
            v2g_capable_vehicles = sum(1 for model_key in ['Tesla_Model_3', 'Tesla_Model_Y', 'Nissan_Leaf', 'Hyundai_Ioniq5', 'BYD_Atto_3'] 
                                     if model_key in st.session_state.cpo_system['ev_models'])
            v2g_fleet_ratio = min(0.4, v2g_capable_vehicles / max(1, fleet_size))  # Assume 40% max V2G capable
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                v2g_power = fleet_size * v2g_fleet_ratio * 8  # 8kW average per V2G vehicle
                st.metric("V2G Capacity", f"{v2g_power:.1f} kW", help="Available V2G discharge capacity")
            
            with col2:
                st.metric("V2G Vehicles", f"{int(fleet_size * v2g_fleet_ratio)}", delta=f"{v2g_fleet_ratio*100:.0f}% of fleet", help="V2G capable vehicles")
            
            with col3:
                st.metric("Grid Support", "Active", delta="💰 Revenue in Financial", help="Financial details in Financial Analysis")
        
        # Grid Services Configuration
        st.subheader("⚙️ Grid Services Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Active Services:**")
            services = {
                "Frequency Response": True,
                "Voltage Support": True,
                "Peak Shaving": regulation_active,
                "Load Balancing": True,
                "Harmonic Filtering": fleet_size > 20,
                "V2G Arbitrage": fleet_size > 10
            }
            
            for service, active in services.items():
                status = "✅ Active" if active else "⏸️ Inactive"
                st.write(f"**{service}:** {status}")
        
        with col2:
            st.markdown("**Financial Benefits:**")
            st.info("💰 **Grid Services Revenue**")
            st.write("• Frequency regulation income")
            st.write("• Voltage support compensation")
            st.write("• Peak shaving savings")
            st.write("• V2G arbitrage profits")
            st.write("")
            st.write("📈 **See Financial Analysis for detailed revenue calculations**")
        
        # Real-time Grid Parameters Chart
        st.subheader("📊 Real-Time Grid Parameters")
        
        # Generate 24h data for key parameters
        hours = list(range(24))
        current_hour = datetime.now().hour
        
        # Frequency variation throughout the day
        frequency_profile = [50.0 + 0.05 * np.sin(2 * np.pi * h / 24) + np.random.normal(0, 0.02) for h in hours]
        
        # THD variation (higher during peak hours due to more electronic loads)
        thd_profile = [3.0 + 1.5 * (0.5 + 0.5 * np.sin(np.pi * (h - 6) / 16)) if 6 <= h <= 22 else 2.5 + np.random.uniform(-0.3, 0.3) for h in hours]
        
        # Power factor variation
        pf_profile = [0.95 - 0.08 * (0.5 + 0.5 * np.sin(np.pi * (h - 6) / 16)) if 6 <= h <= 22 else 0.96 + np.random.uniform(-0.02, 0.02) for h in hours]
        
        fig_grid = go.Figure()
        
        fig_grid.add_trace(go.Scatter(
            x=hours, y=frequency_profile,
            mode='lines+markers',
            name='Frequency (Hz)',
            line=dict(color='#3b82f6', width=2),
            yaxis='y1'
        ))
        
        fig_grid.add_trace(go.Scatter(
            x=hours, y=thd_profile,
            mode='lines+markers',
            name='THD Voltage (%)',
            line=dict(color='#ef4444', width=2),
            yaxis='y2'
        ))
        
        fig_grid.add_trace(go.Scatter(
            x=hours, y=pf_profile,
            mode='lines+markers',
            name='Power Factor',
            line=dict(color='#10b981', width=2),
            yaxis='y3'
        ))
        
        fig_grid.add_vline(x=current_hour, line_dash="dash", line_color="red", 
                          annotation_text=f"Now: {current_hour}:00")
        
        fig_grid.update_layout(
            title="24h Grid Quality Parameters",
            xaxis_title="Hour",
            yaxis=dict(title="Frequency (Hz)", side="left", range=[49.9, 50.1]),
            yaxis2=dict(title="THD (%)", side="right", overlaying="y", range=[2, 6]),
            yaxis3=dict(title="Power Factor", side="right", overlaying="y", position=0.95, range=[0.85, 1.0]),
            height=400,
            legend=dict(x=0.02, y=0.98)
        )
        
        st.plotly_chart(fig_grid, use_container_width=True)
        
    else:
        st.warning("**Grid Regulation Services INACTIVE**")
        st.info("**⚡ Enable 'Smart Grid Regulation' in the sidebar to activate grid services**")
        
        # Show potential benefits even when inactive
        if fleet_size > 0:
            st.markdown(f"""
            <div class="charging-station-card">
                <h4>⚡ Grid Services Potential</h4>
                <p>With your current fleet of <strong>{fleet_size} vehicles</strong>, you could provide:</p>
                <ul>
                    <li><strong>Frequency regulation</strong> services to ONEE</li>
                    <li><strong>Voltage support</strong> and reactive power compensation</li>
                    <li><strong>Peak shaving</strong> and load balancing</li>
                    <li><strong>V2G services</strong> for grid stability</li>
                </ul>
                <p><em>💰 Financial benefits detailed in Financial Analysis section</em></p>
            </div>
            """, unsafe_allow_html=True)

def render_comprehensive_financial_analysis():
    """Comprehensive Financial Analysis with Grid Services Revenue"""
    st.header("Financial Analysis & Revenue Optimization")
    st.markdown("""
    <div class="professional-alert">
        <h4>CPO Financial Intelligence Center</h4>
        <p>Comprehensive financial analysis including charging revenue, grid services income, ONEE tariff optimization, and investment analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get system configuration
    onee_tariffs = st.session_state.cpo_system['onee_tariffs']
    tariff_scheme = st.session_state.cpo_configuration['tariff_scheme']
    station_models = st.session_state.cpo_system['charging_stations']
    station_config = st.session_state.cpo_configuration['station_config']
    fleet_size = st.session_state.cpo_configuration['fleet_size']
    regulation_active = st.session_state.cpo_system.get('regulation_active', False)
    
    # Calculate total investments
    total_stations = sum(station_config.values())
    total_investment = 0
    monthly_opex = 0
    
    for station_id, quantity in station_config.items():
        if quantity > 0:
            station_specs = station_models[station_id]
            total_investment += quantity * station_specs['installation_cost_mad']
            monthly_opex += quantity * station_specs['operational_cost_mad_month']
    
    # Revenue Streams Overview
    st.subheader("💰 Revenue Streams Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Charging Revenue
    with col1:
        daily_charging_revenue = total_stations * 850 if total_stations > 0 else 0
        monthly_charging_revenue = daily_charging_revenue * 30
        st.markdown(f"""
        <div class="kpi-metric">
            <h4>Charging Revenue</h4>
            <h3>{monthly_charging_revenue:,.0f} MAD</h3>
            <p>Monthly from EV charging</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Grid Services Revenue (from Grid Regulation benefits)
    with col2:
        if regulation_active and fleet_size > 0:
            freq_revenue = fleet_size * 12.5 * 30  # Monthly
            voltage_revenue = fleet_size * 8.3 * 30
            peak_revenue = fleet_size * 15.7 * 30
            monthly_grid_revenue = freq_revenue + voltage_revenue + peak_revenue
        else:
            monthly_grid_revenue = 0
        
        st.markdown(f"""
        <div class="kpi-metric">
            <h4>Grid Services</h4>
            <h3>{monthly_grid_revenue:,.0f} MAD</h3>
            <p>Monthly from grid regulation</p>
        </div>
        """, unsafe_allow_html=True)
    
    # V2G Arbitrage Revenue
    with col3:
        if regulation_active and fleet_size > 0:
            v2g_fleet_ratio = min(0.4, fleet_size * 0.3)  # 30% V2G capable
            v2g_power = fleet_size * v2g_fleet_ratio * 8
            monthly_v2g_revenue = v2g_power * 12 * (1.45 - 0.85) * 30  # Arbitrage
        else:
            monthly_v2g_revenue = 0
        
        st.markdown(f"""
        <div class="kpi-metric">
            <h4>V2G Arbitrage</h4>
            <h3>{monthly_v2g_revenue:,.0f} MAD</h3>
            <p>Monthly energy arbitrage</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Total Monthly Revenue
    with col4:
        total_monthly_revenue = monthly_charging_revenue + monthly_grid_revenue + monthly_v2g_revenue
        st.markdown(f"""
        <div class="kpi-metric">
            <h4>Total Revenue</h4>
            <h3>{total_monthly_revenue:,.0f} MAD</h3>
            <p>Total monthly income</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Investment & ROI Analysis
    st.subheader("📈 Investment & ROI Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Capital Expenditure (CAPEX):**")
        
        # Investment breakdown
        investment_data = []
        for station_id, quantity in station_config.items():
            if quantity > 0:
                station_specs = station_models[station_id]
                investment = quantity * station_specs['installation_cost_mad']
                investment_data.append({
                    'Station Type': station_specs['name'],
                    'Quantity': quantity,
                    'Unit Cost (MAD)': f"{station_specs['installation_cost_mad']:,}",
                    'Total Investment (MAD)': f"{investment:,}"
                })
        
        if investment_data:
            df_investment = pd.DataFrame(investment_data)
            st.dataframe(df_investment, use_container_width=True)
            
            st.metric("Total CAPEX", f"{total_investment:,} MAD")
        else:
            st.info("Configure stations to see investment analysis")
    
    with col2:
        st.markdown("**Operational Expenditure (OPEX) & ROI:**")
        
        if total_investment > 0:
            annual_revenue = total_monthly_revenue * 12
            annual_opex = monthly_opex * 12
            annual_profit = annual_revenue - annual_opex
            roi_years = total_investment / annual_profit if annual_profit > 0 else float('inf')
            roi_percentage = (annual_profit / total_investment) * 100 if total_investment > 0 else 0
            
            st.metric("Monthly OPEX", f"{monthly_opex:,.0f} MAD")
            st.metric("Annual Profit", f"{annual_profit:,.0f} MAD", delta=f"{roi_percentage:.1f}% ROI")
            
            if roi_years < 10:
                st.metric("Payback Period", f"{roi_years:.1f} years", delta="🟢 Profitable")
            else:
                st.metric("Payback Period", ">10 years", delta="🟡 Review needed")
        else:
            st.info("Investment data will appear when stations are configured")
    

    
    # ONEE Tariffs
    st.subheader("⚡ ONEE Tariff Structure")
    
    current_tariffs = onee_tariffs[tariff_scheme]
    
    tariff_data = []
    for period_key, period_data in current_tariffs.items():
        period_names = {
            'peak_hours': 'Peak Hours',
            'standard_hours': 'Standard Hours', 
            'off_peak_hours': 'Off-Peak Hours'
        }
        
        tariff_data.append({
            'Period': period_names[period_key],
            'Schedule': period_data['time'],
            'Price (MAD/kWh)': f"{period_data['price_mad_kwh']:.2f}"
        })
    
    df_tariffs = pd.DataFrame(tariff_data)
    st.dataframe(df_tariffs, use_container_width=True)
    
    # Financial Projections
    if total_monthly_revenue > 0:
        st.subheader("📈 Financial Projections (5 Years)")
        
        years = list(range(1, 6))
        annual_revenues = []
        cumulative_profit = []
        cumulative = 0
        
        # Calculate base annual revenue
        annual_revenue = total_monthly_revenue * 12
        
        for year in years:
            # Assume 5% annual growth
            year_revenue = annual_revenue * (1.05 ** (year - 1))
            year_opex = annual_opex * (1.03 ** (year - 1))  # 3% opex growth
            year_profit = year_revenue - year_opex
            cumulative += year_profit
            
            annual_revenues.append(year_revenue)
            cumulative_profit.append(cumulative)
        
        fig_projection = go.Figure()
        
        fig_projection.add_trace(go.Bar(
            x=years,
            y=annual_revenues,
            name='Annual Revenue',
            marker_color='#3b82f6'
        ))
        
        fig_projection.add_trace(go.Scatter(
            x=years,
            y=cumulative_profit,
            mode='lines+markers',
            name='Cumulative Profit',
            line=dict(color='#10b981', width=3),
            yaxis='y2'
        ))
        
        fig_projection.update_layout(
            title="5-Year Financial Projection",
            xaxis_title="Year",
            yaxis=dict(title="Annual Revenue (MAD)", side="left"),
            yaxis2=dict(title="Cumulative Profit (MAD)", side="right", overlaying="y"),
            height=400
        )
        
        st.plotly_chart(fig_projection, use_container_width=True)
    
    # Grid Services Revenue Detail (from Grid Regulation)
    if regulation_active and fleet_size > 0:
        st.subheader("⚡ Grid Services Revenue Detail")
        st.info("🔌 **Source: Grid Regulation Services** - Technical parameters managed in Grid Regulation section")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Daily Grid Services Revenue:**")
            daily_freq = fleet_size * 12.5
            daily_voltage = fleet_size * 8.3
            daily_peak = fleet_size * 15.7
            
            st.write(f"• Frequency Regulation: **{daily_freq:,.0f} MAD/day**")
            st.write(f"• Voltage Support: **{daily_voltage:,.0f} MAD/day**")
            st.write(f"• Peak Shaving: **{daily_peak:,.0f} MAD/day**")
            st.write(f"• **Total Daily: {daily_freq + daily_voltage + daily_peak:,.0f} MAD**")
        
        with col2:
            st.markdown("**Monthly Grid Services Revenue:**")
            st.write(f"• Frequency Regulation: **{freq_revenue:,.0f} MAD/month**")
            st.write(f"• Voltage Support: **{voltage_revenue:,.0f} MAD/month**")
            st.write(f"• Peak Shaving: **{peak_revenue:,.0f} MAD/month**")
            st.write(f"• **Total Monthly: {monthly_grid_revenue:,.0f} MAD**")
    
    elif fleet_size > 0:
        st.subheader("⚡ Potential Grid Services Revenue")
        st.warning("⏸️ Grid Regulation is currently inactive")
        
        potential_daily = fleet_size * (12.5 + 8.3 + 15.7)
        potential_monthly = potential_daily * 30
        potential_annual = potential_monthly * 12
        
        st.markdown(f"""
        <div class="charging-station-card">
            <h4>💰 Missed Revenue Opportunity</h4>
            <p>With your current fleet of <strong>{fleet_size} vehicles</strong>, you could earn:</p>
            <ul>
                <li><strong>{potential_daily:,.0f} MAD/day</strong> from grid services</li>
                <li><strong>{potential_monthly:,.0f} MAD/month</strong> additional revenue</li>
                <li><strong>{potential_annual:,.0f} MAD/year</strong> annual income</li>
            </ul>
            <p><em>⚡ Enable Grid Regulation in the sidebar to unlock this revenue stream!</em></p>
        </div>
        """, unsafe_allow_html=True)

def render_future_improvements_roadmap():
    """Simple Recommendations & Future Improvements"""
    st.header("Recommendations & Future Improvements")
    st.markdown("""
    <div class="professional-alert">
        <h4>Strategic Recommendations</h4>
        <p>Practical recommendations to improve your CPO operations and profitability.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current configuration for personalized recommendations
    fleet_size = st.session_state.cpo_configuration['fleet_size']
    station_config = st.session_state.cpo_configuration['station_config']
    total_stations = sum(station_config.values())
    operating_mode = st.session_state.cpo_configuration['operating_mode']
    
    # Immediate Actions (0-3 months)
    st.subheader("🚀 Immediate Actions (0-3 months)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="success-alert">
            <h4>📊 Operational Optimization</h4>
            <ul>
                <li><strong>Smart Pricing:</strong> Implement time-of-use pricing to increase revenue by 15-20%</li>
                <li><strong>Load Balancing:</strong> Distribute charging across off-peak hours</li>
                <li><strong>Maintenance Schedule:</strong> Preventive maintenance to ensure 99% uptime</li>
                <li><strong>Customer App:</strong> Mobile app for reservations and payments</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-alert">
            <h4>💰 Revenue Enhancement</h4>
            <ul>
                <li><strong>Peak Hour Premiums:</strong> 20-30% higher rates during 18h-22h</li>
                <li><strong>Subscription Plans:</strong> Monthly/yearly plans for regular users</li>
                <li><strong>Corporate Contracts:</strong> Fleet charging agreements</li>
                <li><strong>Advertising Revenue:</strong> Digital displays at charging stations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Short-term Improvements (3-12 months)
    st.subheader("🎯 Short-term Improvements (3-12 months)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="charging-station-card">
            <h4>⚡ Infrastructure Expansion</h4>
            <ul>
                <li><strong>V2G Integration:</strong> Enable vehicle-to-grid services for additional revenue</li>
                <li><strong>Solar Panels:</strong> Reduce grid dependency by 30-40%</li>
                <li><strong>Battery Storage:</strong> Store cheap off-peak energy</li>
                <li><strong>Fast Charging:</strong> Add DC fast chargers for premium pricing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="charging-station-card">
            <h4>📊 Analytics & Monitoring</h4>
            <ul>
                <li><strong>Real-time Monitoring:</strong> 24/7 station health monitoring</li>
                <li><strong>Predictive Maintenance:</strong> AI-based failure prediction</li>
                <li><strong>Customer Analytics:</strong> Usage patterns and preferences</li>
                <li><strong>Energy Management:</strong> Smart grid integration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Long-term Vision (1-3 years)
    st.subheader("🌆 Long-term Vision (1-3 years)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🌍 Market Expansion:**
        - Geographic expansion to new cities
        - Partnership with hotels, malls, offices
        - Highway charging corridors
        - International expansion opportunities
        
        **🤖 Technology Integration:**
        - AI-powered demand forecasting
        - Autonomous charging robots
        - Wireless charging technology
        - Integration with smart city infrastructure
        """)
    
    with col2:
        st.markdown("""
        **💹 Business Model Innovation:**
        - Energy trading and arbitrage
        - Virtual power plant services
        - Carbon credit monetization
        - Mobility-as-a-Service integration
        
        **🌱 Sustainability Goals:**
        - 100% renewable energy sourcing
        - Carbon neutral operations
        - Circular economy practices
        - Green building certifications
        """)
    
    # Personalized Recommendations
    st.subheader("🎯 Personalized Recommendations")
    
    if fleet_size == 0:
        st.info("🚗 **Fleet Recommendation:** Consider adding a managed fleet to increase utilization and revenue.")
    elif fleet_size < 50:
        st.info(f"📈 **Fleet Growth:** Your current fleet of {fleet_size} vehicles could be expanded to optimize station utilization.")
    else:
        st.success(f"✅ **Fleet Size:** Your fleet of {fleet_size} vehicles is well-sized for current operations.")
    
    if total_stations == 0:
        st.warning("⚠️ **Infrastructure:** Configure charging stations to start operations.")
    elif total_stations < 10:
        st.info(f"🔌 **Station Expansion:** Consider adding more stations to your current {total_stations} for better coverage.")
    else:
        st.success(f"✅ **Infrastructure:** Your {total_stations} stations provide good coverage.")
    
    if operating_mode == "Profit Maximization":
        st.info("💰 **Focus on:** Dynamic pricing, premium services, and high-margin offerings.")
    elif operating_mode == "Customer Satisfaction":
        st.info("😊 **Focus on:** Service quality, reliability, and customer experience improvements.")
    elif operating_mode == "Grid Support Priority":
        st.info("⚡ **Focus on:** V2G services, demand response, and grid stabilization revenue.")
    else:
        st.info("⚖️ **Focus on:** Balanced approach across profitability, service, and grid support.")
    
    # Quick Action Items
    st.subheader("✅ Quick Action Items")
    
    action_items = [
        "Review and optimize current pricing strategy",
        "Implement preventive maintenance schedule",
        "Analyze peak usage patterns for capacity planning",
        "Explore partnerships with local businesses",
        "Investigate renewable energy integration options",
        "Develop customer loyalty program",
        "Assess V2G revenue opportunities",
        "Plan for regulatory compliance updates"
    ]
    
    for i, item in enumerate(action_items, 1):
        st.checkbox(f"{i}. {item}", key=f"action_{i}")
    
    # Footer
    st.markdown("---")
    st.markdown("**© 2025 FLEXGRID CPO Platform** - Professional EV Charging Management System")
    st.markdown("*Driving the future of sustainable transportation and smart grid integration*")

if __name__ == "__main__":
    main()