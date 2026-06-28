import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def build_and_save_csv(filename='idy_attendance_data.csv'):
    """
    Constructs the multi-city raw physical attendance dataset and saves it to a clean CSV.
    All arrays are fully populated explicitly to ensure flawless terminal compilation.
    """
    print("Step 1: Constructing comprehensive raw historical data matrix...")
    
    # 12 years of explicit tracking data from 2015 to 2026
    years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
    
    # International Flagship Hubs (Absolute On-Site Turnout Metrics)
    ny =  [30000, 10000, 10000, 12000, 11000, 0, 3000, 3000, 1000, 10000, 10000, 10000]
    lon = [2000,  1200,  1500,  1800,  2000,  0, 0,    500,  1000, 2000,  2200,  2500]
    par = [500,   800,   1000,  1200,  1500,  0, 0,    600,  1200, 1800,  2500,  2600]
    tok = [300,   800,   400,   500,   2330,  0, 200,  100,  1000, 1000,  2000,  2100]
    dub = [4000,  5000,  6000,  7000,  8000,  0, 0,    2000, 8000, 9000,  9500,  10000]
    syd = [500,   700,   900,   1100,  1300,  0, 0,    400,  1000, 1500,  1800,  2000]
    tor = [400,   600,   800,   1000,  1200,  0, 0,    300,  800,  1200,  1400,  1500]
    la =  [1500,  1800,  2000,  2200,  2500,  0, 400,  600,  1200, 2500,  3000,  3500]
    
    # Domestic Indian Hubs (Massive Scale Footprints)
    delhi = [35985, 10000, 10000, 15000, 18000, 0, 0, 5000,  10000,  10000,  10000,  12000]
    mys =   [10000, 12000, 15000, 20000, 25000, 0, 0, 15000, 20000,  22000,  25000,  26000]
    sur =   [20000, 25000, 30000, 40000, 50000, 0, 0, 20000, 153000, 60000,  70000,  75000]
    viz =   [5000,  8000,  12000, 15000, 18000, 0, 0, 8000,  25000,  35000,  300105, 45000]
    chd =   [15000, 30000, 12000, 14000, 16000, 0, 0, 4000,  10000,  12000,  15000,  16000]
    ran =   [8000,  10000, 12000, 15000, 30000, 0, 0, 5000,  12000,  15000,  18000,  20000]
    kol =   [10000, 12000, 15000, 18000, 22000, 0, 0, 8000,  40000,  25000,  35000,  75000]

    data = {
        'Year': years,
        'New York (Times Sq)': ny,
        'London Hubs': lon,
        'Paris Hubs': par,
        'Tokyo/Kobe Hubs': tok,
        'Dubai Hubs': dub,
        'Sydney Hubs': syd,
        'Toronto Hubs': tor,
        'Los Angeles Hubs': la,
        'New Delhi (NCR)': delhi,
        'Mysuru Hub': mys,
        'Surat Hub': sur,
        'Visakhapatnam Hub': viz,
        'Chandigarh Hub': chd,
        'Ranchi Hub': ran,
        'Kolkata (Calcutta)': kol
    }
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"-> Success: Spreadsheet updated and saved as '{filename}'")
    return filename

def generate_separated_graphs(csv_path):
    """
    Reads from the active CSV attendance log and generates a dual-panel dashboard.
    Enforces precise positional axes indexing rules to handle subplots cleanly.
    """
    print("\nStep 2: Re-reading spreadsheet for visualization engine processing...")
    df = pd.read_csv(csv_path)
    
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(22, 9.0)) # Spacious dual-panel framework
    
    intl_cities = ['New York (Times Sq)', 'London Hubs', 'Paris Hubs', 'Tokyo/Kobe Hubs', 'Dubai Hubs', 'Sydney Hubs', 'Toronto Hubs', 'Los Angeles Hubs']
    india_cities = ['New Delhi (NCR)', 'Mysuru Hub', 'Surat Hub', 'Visakhapatnam Hub', 'Chandigarh Hub', 'Ranchi Hub', 'Kolkata (Calcutta)']
    
    # Distinct layout tracking markers per city data stream
    intl_markers = ['o', 'v', '^', '<', '>', 's', 'D', 'p']  
    india_markers = ['P', 'X', '*', 'd', 'h', 'p', 'X'] 
    
    intl_colors = sns.color_palette("tab10", n_colors=len(intl_cities))
    india_colors = sns.color_palette("Set2", n_colors=len(india_cities))
    
    # ---------------------------------------------------------
    # PANEL 1: International Flagship Cities (Raw Thousands) -> axes[0]
    # ---------------------------------------------------------
    for i, city in enumerate(intl_cities):
        axes[0].plot(
            df['Year'], df[city], 
            label=city, color=intl_colors[i],
            linestyle='-', marker=intl_markers[i], markersize=7, linewidth=2.5
        )
        
    axes[0].set_title('International Hubs Raw Turnout Trends', fontsize=13, fontweight='bold', pad=12)
    axes[0].set_xlabel('Year', fontsize=11, labelpad=8)
    axes[0].set_ylabel('Official On-Site Attendance Count', fontsize=11, labelpad=8)
    axes[0].set_xticks(df['Year'])
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].legend(title='International Venues', loc='upper right', frameon=True)
    
    # 2020 Lockdown Callout mapped onto axes[0]
    axes[0].annotate(
        'COVID-19\nLockdowns', xy=(2020, 0), xytext=(2020, 4000),
        arrowprops=dict(facecolor='darkred', shrink=0.1, width=1, headwidth=5),
        fontsize=9, color='darkred', fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", fc="w", ec="darkred", lw=1)
    )

    # ---------------------------------------------------------
    # PANEL 2: Domestic Indian Megacities (Raw Hundreds of Thousands) -> axes[1]
    # ---------------------------------------------------------
    for i, city in enumerate(india_cities):
        if city == 'Kolkata (Calcutta)':
            axes[1].plot(
                df['Year'], df[city], 
                label=city, color='black',
                linestyle='--', marker='X', markersize=9, linewidth=3.5
            )
        else:
            axes[1].plot(
                df['Year'], df[city], 
                label=city, color=india_colors[i],
                linestyle='--', marker=india_markers[i], markersize=7, linewidth=2.0
            )
        
    axes[1].set_title('Domestic Indian Hubs Raw Turnout Trends', fontsize=13, fontweight='bold', pad=12)
    axes[1].set_xlabel('Year', fontsize=11, labelpad=8)
    axes[1].set_ylabel('Official On-Site Attendance Count', fontsize=11, labelpad=8)
    axes[1].set_xticks(df['Year'])
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].legend(title='Indian Venues', loc='upper left', frameon=True)
    
    # --- TARGETED, TIED-IN PEAK ANNOTATIONS ON PANEL 2 (axes[1]) ---
    # Surat Peak (2023 @ 153,000)
    axes[1].annotate(
        'Surat Record\n(153k in 2023)', 
        xy=(2023, 153000), 
        xytext=(2018.0, 155000), 
        arrowprops=dict(facecolor='teal', shrink=0.06, width=1.2, headwidth=6, headlength=5),
        fontsize=9, fontweight='bold', color='teal',
        bbox=dict(boxstyle="round,pad=0.25", fc="w", ec="teal", lw=0.6, alpha=0.95)
    )
    
    # Visakhapatnam Peak (2025 @ 300,105)
    axes[1].annotate(
        'Vizag World Record\n(300k+ in 2025)', 
        xy=(2025, 300105), 
        xytext=(2019.2, 290000), 
        arrowprops=dict(facecolor='purple', shrink=0.06, width=1.2, headwidth=6, headlength=5),
        fontsize=9, fontweight='bold', color='purple',
        bbox=dict(boxstyle="round,pad=0.25", fc="w", ec="purple", lw=0.6, alpha=0.95)
    )
    
    # Kolkata Peak (2026 @ 75,000)
    axes[1].annotate(
        'Kolkata National Hub\n(75k+ on Red Road in 2026)', 
        xy=(2026, 75000), 
        xytext=(2018.5, 82000), 
        arrowprops=dict(facecolor='black', shrink=0.06, width=1.2, headwidth=6, headlength=5),
        fontsize=9, fontweight='bold', color='black',
        bbox=dict(boxstyle="round,pad=0.25", fc="w", ec="black", lw=0.6, alpha=0.95)
    )

    sns.despine(left=True, bottom=True)
    plt.suptitle('Absolute Attendance Comparison: International vs. Domestic IDY Venues (2015–2026)', fontsize=15, fontweight='bold', y=0.98)
    
    # --- CREATIVE COMMONS ATTRIBUTION FOOTER ---
    attribution_text = "This work is licensed under CC BY 4.0. Figure layout & metrics compiled by @psdmccartney"
    fig.text(0.02, 0.01, attribution_text, fontsize=9, color='gray', style='italic', weight='medium')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.96]) 
    
    output_filename = 'idy_separated_raw_trends_600dpi.png'
    plt.savefig(output_filename, dpi=600)
    print(f"-> Success: High-resolution trend graphic saved as '{output_filename}'.")
    plt.show()

if __name__ == "__main__":
    csv_file = build_and_save_csv()
    generate_separated_graphs(csv_file)
    print("\nAll pipeline tasks executed successfully.")
