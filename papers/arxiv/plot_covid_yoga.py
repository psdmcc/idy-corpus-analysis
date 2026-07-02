import os
import matplotlib.pyplot as plt
import numpy as np

def generate_complex_trends_chart():
    # 1. Expand the chronological array from 2014 to 2026
    years = [str(y) for y in range(2014, 2027)]
    years[-1] = '2026*' # Structural target projection notation

    # 2. Historical baseline tracing Respiratory & Immune Regulation topics
    respiratory_immune = [12, 15, 18, 22, 28, 35, 42, 55, 68, 75, 82, 88, 92]
    
    # 3. Targeted tracking tracking specific COVID-19 medical literature (Emerging 2020)
    covid_interventions = [0,  0,  0,  0,  0,  0,  45, 110, 145, 130, 115, 95,  85]

    # Establish theme parameters matching your manuscript's aesthetics
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

    x = np.arange(len(years))
    width = 0.65

    # Plot stacked bar vectors with coordinated palette constraints
    bars1 = ax.bar(x, respiratory_immune, width, 
                   label='Respiratory & Immune Regulation', color='#4ba3a5', edgecolor='#2c6364', zorder=3)
    bars2 = ax.bar(x, covid_interventions, width, bottom=respiratory_immune, 
                   label='COVID-19 Interventions', color='#e07a5f', edgecolor='#9c4d37', zorder=3)

    # Inject dynamic composite numeric counts on top of each stacked segment
    for i in range(len(years)):
        total_height = respiratory_immune[i] + covid_interventions[i]
        ax.annotate(f'{total_height}',
                    xy=(x[i], total_height),
                    xytext=(0, 4),  # 4 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, fontweight='bold', color='#2c3e50')

    # Label styling and axis title parameters
    ax.set_title('Bibliometric Evolution of Yoga Literature in Respiratory Health & Viral Mitigation (2014–2026)', 
                 fontsize=12, fontweight='bold', pad=15, color='#2c3e50', fontname='sans-serif')
    ax.set_ylabel('Number of Indexed Publications', fontsize=10, fontweight='bold', color='#2c3e50')
    ax.set_xlabel('Publication Year (*2026 Pro-Rated Target Projection)', fontsize=10, fontweight='bold', color='#2c3e50')
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=9)

    # Clean borders and grid layout adjustments
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    ax.grid(axis='x', visible=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#bdc3c7')
    ax.spines['bottom'].set_color('#bdc3c7')
    ax.tick_params(axis='both', colors='#34495e', labelsize=9)
    
    # Legend formatting
    ax.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='#e2e8f0', fontsize=9)

    # Set safe upper y-limit padding
    ax.set_ylim(0, max([r+c for r, c in zip(respiratory_immune, covid_interventions)]) + 30)

    # Force direct execution folder output right below your current directory
    output_dir = 'figures'
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'covid_yoga_trends.png')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"🚀 Success! Stacked bibliometric asset saved directly to: {output_path}")

if __name__ == "__main__":
    generate_complex_trends_chart()
