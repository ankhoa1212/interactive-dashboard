import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu, ttest_ind
import os
from initial_analysis import get_cell_frequency_data, DB_FILE


def statistical_analysis(return_df=False, test_type='u'):
    data = get_cell_frequency_data(DB_FILE)
    df = pd.DataFrame(data)

    filtered_df = df[df['response'].isin(['yes', 'no'])]

    if filtered_df.empty:
        if return_df:
            return pd.DataFrame()
        print("No data found matching criteria.")
        return

    populations = filtered_df['population'].unique()
    stats_results = []

    for pop in populations:
        pop_data = filtered_df[filtered_df['population'] == pop]

        responders = pop_data[pop_data['response'] == 'yes']['percentage']
        non_responders = pop_data[pop_data['response'] == 'no']['percentage']

        if test_type == 't':
            stat, p_value = ttest_ind(responders, non_responders, equal_var=False, nan_policy='omit')
        else:
            stat, p_value = mannwhitneyu(responders, non_responders)

        mean_resp = responders.mean()
        mean_non_resp = non_responders.mean()
        significant = "YES" if p_value < 0.05 else "NO"

        stats_results.append({
            'population': pop,
            'responder_mean': mean_resp,
            'non_responder_mean': mean_non_resp,
            'p_value': p_value,
            'significant': significant
        })

    stats_df = pd.DataFrame(stats_results)

    if return_df:
        return stats_df

    print(f"{'Population':<15} {'Responder Mean%':<20} {'Non-Responder Mean%':<25} {'P-Value':<10} {'Significant'}")
    print("-" * 90)
    for row in stats_results:
        print(f"{row['population']:<15} {row['responder_mean']:<20.2f} {row['non_responder_mean']:<25.2f} {row['p_value']:<10.4f} {row['significant']}")

    plt.figure(figsize=(12, 8))
    sns.boxplot(y='population', x='percentage', hue='response', data=filtered_df, orient='h')
    plt.title(f'Cell Population Relative Frequencies: Responders vs Non-Responders\n(Filtered, {"t-test" if test_type=="t" else "Mann-Whitney U"})')
    plt.xlabel('Relative Frequency (%)')
    plt.ylabel('Cell Population')

    output_file = 'response_comparison.png'
    plt.savefig(output_file)
    print(f"\nPlot saved to {output_file}")

if __name__ == "__main__":
    statistical_analysis()
