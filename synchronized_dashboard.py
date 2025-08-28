"""
🌍 FLEXGRID CPO Dashboard - SYNCHRONIZED VERSION
Single Source of Truth with Real-Time Data Consistency
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="FLEXGRID CPO - Synchronized Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State - Single Source of Truth
def initialize_session_state():
    if "data" not in st.session_state:
        st.session_state["data"] = {
            "stations": [],
            "fleet": [],
            "financial": {
                "total_investment": 0,
                "annual_revenue": 0,
                "roi_years": 0,
                "monthly_profit": 0,
                "operational_costs": 0
            }
        }
    
    if "last_update" not in st.session_state:
        st.session_state["last_update"] = datetime.now()

# Station Types Database
STATION_TYPES = {
    "AC Standard (7kW)": {"power": 7, "cost": 25000, "efficiency": 0.92},
    "AC Fast (22kW)": {"power": 22, "cost": 45000, "efficiency": 0.94},
    "DC Fast (50kW)": {"power": 50, "cost": 85000, "efficiency": 0.96},
    "DC Ultra Fast (150kW)": {"power": 150, "cost": 180000, "efficiency": 0.98},
    "DC Hypercharger (350kW)": {"power": 350, "cost": 420000, "efficiency": 0.99}
}

# Vehicle Types Database
VEHICLE_TYPES = {
    "Tesla Model 3": {"battery": 75, "efficiency": 0.85, "v2g": True},
    "Nissan Leaf": {"battery": 40, "efficiency": 0.82, "v2g": True},
    "BMW i3": {"battery": 42, "efficiency": 0.80, "v2g": False},
    "VW ID.3": {"battery": 58, "efficiency": 0.83, "v2g": True},
    "Kia EV6": {"battery": 77, "efficiency": 0.86, "v2g": True}
}

# Financial Calculation Engine
def update_financials():
    """Recalculate all financial metrics based on current stations and fleet"""
    stations = st.session_state["data"]["stations"]
    fleet = st.session_state["data"]["fleet"]
    
    # Calculate total investment
    total_investment = sum(station["cost"] for station in stations)
    
    # Calculate capacity and utilization
    total_capacity = sum(station["power"] for station in stations)
    num_stations = len(stations)
    
    # Revenue calculations (MAD)
    if num_stations > 0:
        # Base revenue per station per day (MAD)
        daily_revenue_per_station = 850
        utilization_rate = min(0.85, len(fleet) / max(num_stations, 1) * 0.3)
        
        annual_revenue = num_stations * daily_revenue_per_station * 365 * utilization_rate
        
        # Operational costs (15% of revenue)
        operational_costs = annual_revenue * 0.15
        
        # Monthly profit
        monthly_profit = (annual_revenue - operational_costs) / 12
        
        # ROI calculation
        roi_years = total_investment / max(annual_revenue - operational_costs, 1)
    else:
        annual_revenue = 0
        operational_costs = 0
        monthly_profit = 0
        roi_years = 0
    
    # Update session state
    st.session_state["data"]["financial"] = {
        "total_investment": total_investment,
        "annual_revenue": annual_revenue,
        "roi_years": roi_years,
        "monthly_profit": monthly_profit,
        "operational_costs": operational_costs,
        "total_capacity": total_capacity,
        "utilization_rate": utilization_rate if num_stations > 0 else 0
    }
    
    st.session_state["last_update"] = datetime.now()

# Station Management Section
def station_management_section():
    st.header("🔌 Station Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Add New Station")
        station_type = st.selectbox("Station Type", list(STATION_TYPES.keys()))
        quantity = st.number_input("Quantity", min_value=1, max_value=50, value=1)
        location = st.text_input("Location", value="Casablanca")
        
        if st.button("Add Stations", type="primary"):
            station_data = STATION_TYPES[station_type]
            for i in range(quantity):
                new_station = {
                    "id": len(st.session_state["data"]["stations"]) + 1,
                    "type": station_type,
                    "power": station_data["power"],
                    "cost": station_data["cost"],
                    "efficiency": station_data["efficiency"],
                    "location": location,
                    "status": "Active"
                }
                st.session_state["data"]["stations"].append(new_station)
            
            update_financials()
            st.success(f"Added {quantity} {station_type} station(s)")
            st.rerun()
    
    with col2:
        st.subheader("Quick Stats")
        stations = st.session_state["data"]["stations"]
        st.metric("Total Stations", len(stations))
        if stations:
            total_power = sum(s["power"] for s in stations)
            st.metric("Total Capacity", f"{total_power} kW")
    
    # Current Stations Table
    if st.session_state["data"]["stations"]:
        st.subheader("Current Stations")
        df = pd.DataFrame(st.session_state["data"]["stations"])
        
        # Add remove functionality
        col1, col2 = st.columns([3, 1])
        with col1:
            st.dataframe(df, use_container_width=True)
        
        with col2:
            if st.button("Clear All Stations", type="secondary"):
                st.session_state["data"]["stations"] = []
                update_financials()
                st.rerun()

# Fleet Analytics Section
def fleet_analytics_section():
    st.header("🚗 Fleet Analytics")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Add Vehicles")
        vehicle_type = st.selectbox("Vehicle Type", list(VEHICLE_TYPES.keys()))
        fleet_size = st.number_input("Fleet Size", min_value=1, max_value=200, value=10)
        
        if st.button("Add Fleet", type="primary"):
            vehicle_data = VEHICLE_TYPES[vehicle_type]
            for i in range(fleet_size):
                new_vehicle = {
                    "id": len(st.session_state["data"]["fleet"]) + 1,
                    "type": vehicle_type,
                    "battery": vehicle_data["battery"],
                    "efficiency": vehicle_data["efficiency"],
                    "v2g_capable": vehicle_data["v2g"],
                    "status": "Available"
                }
                st.session_state["data"]["fleet"].append(new_vehicle)
            
            update_financials()
            st.success(f"Added {fleet_size} {vehicle_type} vehicles")
            st.rerun()
    
    with col2:
        st.subheader("Fleet Overview")
        fleet = st.session_state["data"]["fleet"]
        st.metric("Total Vehicles", len(fleet))
        if fleet:
            v2g_count = sum(1 for v in fleet if v["v2g_capable"])
            st.metric("V2G Capable", f"{v2g_count} ({v2g_count/len(fleet)*100:.0f}%)")
    
    # Fleet Distribution Chart
    if st.session_state["data"]["fleet"]:
        st.subheader("Fleet Distribution")
        df = pd.DataFrame(st.session_state["data"]["fleet"])
        type_counts = df['type'].value_counts()
        
        fig = px.pie(values=type_counts.values, names=type_counts.index, 
                    title="Vehicle Type Distribution")
        st.plotly_chart(fig, use_container_width=True)
        
        if st.button("Clear Fleet", type="secondary"):
            st.session_state["data"]["fleet"] = []
            update_financials()
            st.rerun()

# Financial Analysis Section
def financial_analysis_section():
    st.header("💰 Financial Analysis")
    
    # Always use session state data
    financial = st.session_state["data"]["financial"]
    stations = st.session_state["data"]["stations"]
    fleet = st.session_state["data"]["fleet"]
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Investment", 
            f"{financial['total_investment']:,.0f} MAD",
            delta=f"{len(stations)} stations"
        )
    
    with col2:
        st.metric(
            "Annual Revenue", 
            f"{financial['annual_revenue']:,.0f} MAD",
            delta=f"{financial['utilization_rate']:.1%} utilization"
        )
    
    with col3:
        st.metric(
            "Monthly Profit", 
            f"{financial['monthly_profit']:,.0f} MAD"
        )
    
    with col4:
        roi_color = "normal"
        if financial['roi_years'] < 3:
            roi_color = "inverse"
        elif financial['roi_years'] > 7:
            roi_color = "off"
            
        st.metric(
            "ROI Period", 
            f"{financial['roi_years']:.1f} years",
            delta="Excellent" if financial['roi_years'] < 3 else "Good" if financial['roi_years'] < 5 else "Review"
        )
    
    # Investment and ROI Analysis Table
    st.subheader("Investment & ROI Analysis")
    
    if stations:
        # Create detailed analysis
        analysis_data = []
        station_types = {}
        
        for station in stations:
            station_type = station['type']
            if station_type not in station_types:
                station_types[station_type] = {
                    'count': 0,
                    'total_cost': 0,
                    'total_power': 0
                }
            
            station_types[station_type]['count'] += 1
            station_types[station_type]['total_cost'] += station['cost']
            station_types[station_type]['total_power'] += station['power']
        
        for station_type, data in station_types.items():
            analysis_data.append({
                'Station Type': station_type,
                'Quantity': data['count'],
                'Total Investment (MAD)': f"{data['total_cost']:,}",
                'Total Capacity (kW)': data['total_power'],
                'Annual Revenue (MAD)': f"{data['count'] * 850 * 365 * financial['utilization_rate']:,.0f}",
                'ROI (years)': f"{data['total_cost'] / max(data['count'] * 850 * 365 * financial['utilization_rate'] * 0.85, 1):.1f}"
            })
        
        df_analysis = pd.DataFrame(analysis_data)
        st.dataframe(df_analysis, use_container_width=True)
        
        # Revenue Projection Chart
        st.subheader("5-Year Revenue Projection")
        years = list(range(1, 6))
        revenues = [financial['annual_revenue'] * (1.05 ** (year-1)) for year in years]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years, y=revenues,
            mode='lines+markers',
            name='Projected Revenue',
            line=dict(color='#667eea', width=3)
        ))
        fig.update_layout(
            title="Revenue Growth Projection (5% annual growth)",
            xaxis_title="Year",
            yaxis_title="Revenue (MAD)",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("Add stations in Station Management to see financial analysis")

# CPO Control Center
def cpo_control_center():
    st.header("🎛️ CPO Control Center")
    
    # Real-time synchronized data
    stations = st.session_state["data"]["stations"]
    fleet = st.session_state["data"]["fleet"]
    financial = st.session_state["data"]["financial"]
    
    # Executive Summary
    st.subheader("Executive Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Infrastructure Overview:**
        - **{len(stations)}** charging stations deployed
        - **{financial.get('total_capacity', 0):.0f} kW** total capacity
        - **{len(fleet)}** vehicles in fleet
        - **{financial.get('utilization_rate', 0):.1%}** utilization rate
        """)
    
    with col2:
        st.markdown(f"""
        **Financial Performance:**
        - **{financial['total_investment']:,.0f} MAD** total investment
        - **{financial['monthly_profit']:,.0f} MAD** monthly profit
        - **{financial['roi_years']:.1f} years** ROI period
        - **Last Updated:** {st.session_state['last_update'].strftime('%H:%M:%S')}
        """)
    
    # System Status
    if stations and fleet:
        st.success("✅ System Operational - All data synchronized")
        
        # Performance Indicators
        col1, col2, col3 = st.columns(3)
        
        with col1:
            efficiency = np.mean([s['efficiency'] for s in stations])
            st.metric("Avg Station Efficiency", f"{efficiency:.1%}")
        
        with col2:
            v2g_ratio = sum(1 for v in fleet if v['v2g_capable']) / len(fleet)
            st.metric("V2G Fleet Ratio", f"{v2g_ratio:.1%}")
        
        with col3:
            capacity_per_vehicle = financial.get('total_capacity', 0) / max(len(fleet), 1)
            st.metric("kW per Vehicle", f"{capacity_per_vehicle:.1f}")
    
    else:
        st.warning("⚠️ Configure stations and fleet to activate control center")

# Main Application
def main():
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚡ FLEXGRID CPO Dashboard</h1>
        <h2>Synchronized Real-Time Management System</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    section = st.sidebar.selectbox(
        "Select Section",
        ["CPO Control Center", "Station Management", "Fleet Analytics", "Financial Analysis"]
    )
    
    # Data sync indicator
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Last Update:** {st.session_state['last_update'].strftime('%H:%M:%S')}")
    st.sidebar.markdown(f"**Stations:** {len(st.session_state['data']['stations'])}")
    st.sidebar.markdown(f"**Fleet:** {len(st.session_state['data']['fleet'])}")
    
    # Auto-refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        update_financials()
        st.rerun()
    
    # Section routing
    if section == "Station Management":
        station_management_section()
    elif section == "Fleet Analytics":
        fleet_analytics_section()
    elif section == "Financial Analysis":
        financial_analysis_section()
    elif section == "CPO Control Center":
        cpo_control_center()

# CSS Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()