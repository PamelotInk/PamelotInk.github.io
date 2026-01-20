import streamlit as st
import plotly.graph_objects as go
from datetime import date, datetime
import pandas as pd
from random import randint

from core.data_manager import ExperimentDataManager
from core.statistical_engine import ABTestCalculator

# Page config
st.set_page_config(
    page_title="Experimentation Platform",
    page_icon="🧪",
    layout="wide"
)

# Initialize
dm = ExperimentDataManager()
calc = ABTestCalculator()

# Custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🧪 Experimentation Platform")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "➕ Create Experiment", "📈 Results"]
)

# ============= DASHBOARD PAGE =============
if page == "📊 Dashboard":
    st.title("📊 Experimentation Dashboard")
    st.markdown("Welcome to your A/B testing platform!")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    active_exps = dm.get_active_experiments()
    
    with col1:
        st.metric("Active Experiments", len(active_exps))
    
    with col2:
        st.metric("Tests This Month", 12)
    
    with col3:
        st.metric("Win Rate", "42%", delta="5%")
    
    with col4:
        st.metric("Time to Insight", "3.2 days", delta="-4.8 days")
    
    st.markdown("---")
    
    # Active experiments
    st.subheader("🟢 Active Experiments")
    
    if len(active_exps) > 0:
        for idx, exp in active_exps.iterrows():
            days_running = (datetime.now().date() - pd.to_datetime(exp['start_date']).date()).days
            
            with st.expander(f"**{exp['experiment_name']}** - Day {days_running}"):
                st.write(f"**Description:** {exp['description']}")
                st.write(f"**Started:** {exp['start_date']}")
                
                # Get results
                results_df = dm.get_experiment_results(exp['experiment_id'])
                
                if len(results_df) >= 2 and results_df['total_impressions'].sum() > 0:
                    control = results_df[results_df['variant_name'] == 'control'].iloc[0]
                    variant = results_df[results_df['variant_name'] != 'control'].iloc[0]
                    
                    if control['total_impressions'] > 0 and variant['total_impressions'] > 0:
                        stats = calc.is_significant(
                            control_conv=int(control['total_conversions']),
                            control_imp=int(control['total_impressions']),
                            variant_conv=int(variant['total_conversions']),
                            variant_imp=int(variant['total_impressions'])
                        )
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Control", f"{stats['control_rate']:.2f}%")
                        
                        with col2:
                            st.metric(
                                "Variant", 
                                f"{stats['variant_rate']:.2f}%",
                                delta=f"{stats['relative_lift']:.1f}%"
                            )
                        
                        with col3:
                            confidence_icon = "🟢" if stats['is_significant'] else "🟡"
                            st.metric("Confidence", f"{confidence_icon} {stats['confidence']:.1f}%")
                        
                        # Status
                        if stats['is_significant']:
                            if stats['winner'] == 'variant':
                                st.success(f"✅ **WINNER!** Variant shows {stats['relative_lift']:.1f}% improvement")
                            else:
                                st.info("ℹ️ No significant improvement detected")
                        else:
                            st.warning("⏳ Keep running - not yet significant")
                        
                        # Chart
                        fig = go.Figure()
                        
                        fig.add_trace(go.Bar(
                            name='Control',
                            x=['Conversion Rate'],
                            y=[stats['control_rate']],
                            marker_color='lightblue',
                            text=[f"{stats['control_rate']:.2f}%"],
                            textposition='auto'
                        ))
                        
                        fig.add_trace(go.Bar(
                            name='Variant',
                            x=['Conversion Rate'],
                            y=[stats['variant_rate']],
                            marker_color='lightgreen',
                            text=[f"{stats['variant_rate']:.2f}%"],
                            textposition='auto'
                        ))
                        
                        fig.update_layout(height=250, showlegend=True)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("📊 Collecting data... Check back soon!")
                else:
                    st.info("📊 No data yet. Metrics will appear once traffic is recorded.")
    else:
        st.info("👋 No active experiments yet. Create one to get started!")

# ============= CREATE EXPERIMENT PAGE =============
elif page == "➕ Create Experiment":
    st.title("➕ Create New Experiment")
    
    with st.form("new_experiment"):
        col1, col2 = st.columns(2)
        
        with col1:
            exp_name = st.text_input("Experiment Name*", placeholder="e.g., Homepage Hero Image Test")
            created_by = st.text_input("Your Email*", placeholder="your.email@company.com")
        
        with col2:
            start_date = st.date_input("Start Date*", value=date.today())
        
        description = st.text_area("Description", placeholder="What are you testing?")
        hypothesis = st.text_area("Hypothesis", placeholder="We believe that...")
        
        st.markdown("---")
        st.subheader("Variants")
        
        num_variants = st.number_input("Number of variants", min_value=2, max_value=4, value=2)
        
        variants = []
        total_allocation = 0
        
        for i in range(int(num_variants)):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                v_name = st.text_input(
                    f"Variant {i+1} Name",
                    value="control" if i == 0 else f"variant_{chr(96+i)}",
                    key=f"name_{i}"
                )
            
            with col2:
                v_alloc = st.number_input(
                    "Traffic %",
                    min_value=0,
                    max_value=100,
                    value=int(100/num_variants),
                    key=f"alloc_{i}"
                )
            
            variants.append({'name': v_name, 'allocation': v_alloc, 'description': f'Variant {i+1}'})
            total_allocation += v_alloc
        
        if total_allocation != 100:
            st.warning(f"⚠️ Traffic allocation = {total_allocation}% (should be 100%)")
        
        st.markdown("---")
        
        st.subheader("📊 Sample Size Calculator")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            baseline = st.number_input("Baseline Conv. Rate (%)", value=10.0) / 100
        
        with col2:
            mde = st.number_input("Min. Detectable Effect (%)", value=10) / 100
        
        with col3:
            traffic = st.number_input("Daily Traffic", value=10000)
        
        sample_size = calc.calculate_sample_size(baseline, baseline * mde)
        days = calc.estimate_time_to_significance(traffic, baseline, mde)
        
        st.info(f"📏 Need **{sample_size:,}** users per variant • Est. **{days} days**")
        
        submitted = st.form_submit_button("🚀 Launch Experiment", type="primary")
        
        if submitted:
            if not exp_name or not created_by:
                st.error("❌ Please fill in all required fields")
            elif total_allocation != 100:
                st.error("❌ Traffic allocation must equal 100%")
            else:
                try:
                    exp_id = dm.create_experiment(
                        name=exp_name,
                        description=description,
                        hypothesis=hypothesis,
                        start_date=start_date,
                        created_by=created_by,
                        variants=variants
                    )
                    
                    st.success(f"""
                    ✅ **Experiment Created!**
                    
                    **ID:** {exp_id}  
                    **Name:** {exp_name}
                    
                    Your experiment is now live! 🎉
                    """)
                    
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ============= RESULTS PAGE =============
else:
    st.title("📈 Experiment Results")
    
    all_exps = dm.get_active_experiments()
    
    if len(all_exps) > 0:
        exp_names = {row['experiment_id']: row['experiment_name'] for _, row in all_exps.iterrows()}
        
        selected_id = st.selectbox(
            "Select Experiment",
            options=list(exp_names.keys()),
            format_func=lambda x: exp_names[x]
        )
        
        if selected_id:
            exp_info = all_exps[all_exps['experiment_id'] == selected_id].iloc[0]
            
            st.subheader(exp_info['experiment_name'])
            st.caption(f"Started: {exp_info['start_date']} • Status: {exp_info['status']}")
            
            results_df = dm.get_experiment_results(selected_id)
            
            if len(results_df) >= 2 and results_df['total_impressions'].sum() > 0:
                control = results_df[results_df['variant_name'] == 'control'].iloc[0]
                variant = results_df[results_df['variant_name'] != 'control'].iloc[0]
                
                if control['total_impressions'] > 0 and variant['total_impressions'] > 0:
                    stats = calc.is_significant(
                        control_conv=int(control['total_conversions']),
                        control_imp=int(control['total_impressions']),
                        variant_conv=int(variant['total_conversions']),
                        variant_imp=int(variant['total_impressions'])
                    )
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Control", f"{stats['control_rate']:.2f}%")
                    with col2:
                        st.metric("Variant", f"{stats['variant_rate']:.2f}%", delta=f"{stats['relative_lift']:.1f}%")
                    with col3:
                        st.metric("Confidence", f"{stats['confidence']:.1f}%")
                    with col4:
                        st.metric("P-Value", f"{stats['p_value']:.4f}")
                    
                    st.markdown("---")
                    
                    # Detailed table
                    comparison = pd.DataFrame({
                        'Metric': ['Impressions', 'Conversions', 'Conversion Rate', 'Revenue'],
                        'Control': [
                            f"{int(control['total_impressions']):,}",
                            f"{int(control['total_conversions']):,}",
                            f"{stats['control_rate']:.2f}%",
                            f"${float(control['total_revenue']):,.2f}"
                        ],
                        'Variant': [
                            f"{int(variant['total_impressions']):,}",
                            f"{int(variant['total_conversions']):,}",
                            f"{stats['variant_rate']:.2f}%",
                            f"${float(variant['total_revenue']):,.2f}"
                        ]
                    })
                    
                    st.dataframe(comparison, use_container_width=True, hide_index=True)
                    
                    st.markdown("---")
                    
                    # Recommendation
                    if stats['is_significant']:
                        if stats['winner'] == 'variant':
                            st.success(f"### ✅ Ship the Variant!\n\n**{stats['relative_lift']:.1f}% improvement** with {stats['confidence']:.1f}% confidence")
                        else:
                            st.info("### ℹ️ Keep Current Version\n\nNo significant improvement detected.")
                    else:
                        st.warning(f"### ⏳ Keep Running\n\nCurrent confidence: {stats['confidence']:.1f}% (need 95%+)")
                else:
                    st.info("📊 Waiting for traffic data...")
            else:
                st.info("📊 No data available yet.")
    else:
        st.info("No experiments found. Create one to get started!")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ using Streamlit and Pamela Austin's Engineering")