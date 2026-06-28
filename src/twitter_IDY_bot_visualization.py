import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_bot_forensics_visualization(csv_filename='idy_social_geo_matrix.csv'):
    """
    Independent data visualization engine. Reads an existing IDY CSV archive
    to compile a dual-panel forensic dashboard with shaded threshold threat bands.
    Includes a Creative Commons footer attributed to @psdmccartney at 600 DPI.
    """
    print(f"Initializing Standalone Forensic Visualization Engine...")
    
    # 1. Verify existence of the source spreadsheet archive file
    if not os.path.exists(csv_filename):
        raise FileNotFoundError(
            f"Source archive '{csv_filename}' not found in the current folder. "
            f"Please run the data generation script first to create it."
        )
        
    print(f"-> Success: Connected to data repository target: '{csv_filename}'")
    df = pd.read_csv(csv_filename)
    
    # 2. Recompute operational tracking anomaly ratios
    # Calculates the exact volume of Retweets occurring per 1 unique comment instance
    df['Public_Ratio'] = df['Combined_Public_RT'] / df['Combined_Public_CM'].replace(0, 1)
    df['Official_Ratio'] = df['Official_RT'] / df['Official_CM'].replace(0, 1)
    
    # 3. Configure the Matplotlib canvas settings
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(22, 10), gridspec_kw={'width_ratios': [1.2, 1]})
    
    # Isolate 2021 safely out of the continuous line stream to protect the data void plot boundary
    df_clean = df[df['Year'] != 2021]
    
    # ---------------------------------------------------------
    # PANEL 1 (axes[0]): Timeline of Amplification Ratios over Risk Zones
    # ---------------------------------------------------------
    axes[0].plot(df_clean['Year'], df_clean['Public_Ratio'], label='Public Traffic (RT/CM Index)', color='#E0245E', linestyle='-', marker='s', markersize=8, linewidth=3.0)
    axes[0].plot(df_clean['Year'], df_clean['Official_Ratio'], label='Official Traffic (RT/CM Index)', color='#1DA1F2', linestyle='--', marker='o', markersize=8, linewidth=2.5)
    
    # Render shaded horizontal operational risk band indicators
    axes[0].axhspan(0, 8.5, color='green', alpha=0.07, label='🟢 Organic / Natural Conversation Zone')
    axes[0].axhspan(8.5, 12.0, color='orange', alpha=0.07, label='⚡ Coordinated Messaging / Moderate Risk')
    axes[0].axhspan(12.0, 17.0, color='red', alpha=0.07, label='🚨 Automated Retweet Farming / High Bot Risk')
    
    axes[0].set_title('Evolution of Amplification Ratios (Retweets per Comment)', fontsize=13, fontweight='bold', pad=12)
    axes[0].set_xlabel('Year', fontsize=11, labelpad=8)
    axes[0].set_ylabel('Interaction Anomaly Ratio (RT / CM Volume Profile)', fontsize=11, labelpad=8)
    axes[0].set_xticks(df['Year'])
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].set_ylim(-0.5, 17)
    axes[0].legend(loc='lower left', frameon=True, shadow=True, facecolor='white')
    
    # Tightly snapped vector indicator pointing to the 2023 modern inflection threshold cross
    axes[0].annotate(
        '2023 Threshold Cross:\nSystemic Bot Amplification Begins', 
        xy=(2023, 12.18), xytext=(2016.2, 14.2),
        arrowprops=dict(facecolor='darkred', shrink=0.08, width=1.2, headwidth=6),
        fontsize=9.5, fontweight='bold', color='darkred', 
        bbox=dict(boxstyle="round,pad=0.3", fc="w", ec="darkred", lw=0.8)
    )

    # ---------------------------------------------------------
    # PANEL 2 (axes[1]): Categorical Threat Risk Map Progression Progress
    # ---------------------------------------------------------
    risk_labels = []
    bar_colors = []
    
    for _, row in df.iterrows():
        y = int(row['Year'])
        r = row['Public_Ratio']
        if y == 2020: risk_labels.append("⚠️ AMBIGUOUS"); bar_colors.append("#bcbd22")
        elif y == 2021 and r == 0: risk_labels.append("⚪ DATA VOID"); bar_colors.append("#7f7f7f")
        elif r > 12.0: risk_labels.append("🚨 HIGH RISK"); bar_colors.append("#d62728")
        elif r > 8.5: risk_labels.append("⚡ MODERATE"); bar_colors.append("#ff7f0e")
        else: risk_labels.append("🟢 NATURAL"); bar_colors.append("#2ca02c")

    bars = axes[1].barh(df['Year'].astype(str), df['Public_Ratio'], color=bar_colors, height=0.6)
    
    # Append structured alignment threat tags inline to the horizontal bars
    for index, (bar, label) in enumerate(zip(bars, risk_labels)):
        width = bar.get_width()
        axes[1].text(width + 0.3, bar.get_y() + bar.get_height()/2, label, 
                     va='center', ha='left', fontsize=9.5, fontweight='bold', color='black')
        
    axes[1].set_title('Public Threat Risk Profile Progression Summary', fontsize=13, fontweight='bold', pad=12)
    axes[1].set_xlabel('Public Ratio Level Value Scale', fontsize=11, labelpad=8)
    axes[1].set_ylabel('Year Index Pointer', fontsize=11, labelpad=8)
    axes[1].set_xlim(0, 19)

    # 4. Global structural styling adjustments
    sns.despine(left=True, bottom=True)
    plt.suptitle('Twitter/X Bot Anomaly Tracking Dashboard: Amplification Ratio Metrics & Risk Profiles (2015–2026)', fontsize=15, fontweight='bold', y=0.98)
    
    # --- CREATIVE COMMONS ATTRIBUTION FOOTER ---
    attribution_text = "This work is licensed under CC BY 4.0. Social telemetry data & dashboard template compiled by @psdmccartney"
    fig.text(0.02, 0.01, attribution_text, fontsize=9, color='gray', style='italic', weight='medium')
    
    # Structural layout padding configuration to safeguard text bands from bounding cuts
    plt.tight_layout(rect=[0, 0.05, 1, 0.94])
    
    output_filename = 'idy_bot_forensics_dashboard_600dpi.png'
    plt.savefig(output_filename, dpi=600)
    print(f"-> Success: High-resolution forensics dashboard successfully saved to project directory.")
    print(f"   Asset Export Location: '{os.path.abspath(output_filename)}'")

if __name__ == "__main__":
    # Execute visualization routine assuming baseline data spreadsheet is present
    try:
        generate_bot_forensics_visualization()
    except Exception as e:
        print(f"\nExecution Error: {e}")
