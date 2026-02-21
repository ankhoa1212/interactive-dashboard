import sqlite3

DB_FILE = 'cell-count.db'

def get_cell_frequency_data(db_file):
    """Get cell frequency data from the database and calculate relative frequencies."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            cc.sample_id, cc.b_cell, cc.cd8_t_cell, cc.cd4_t_cell, cc.nk_cell, cc.monocyte,
            s.sample_type, sub.condition, sub.treatment, sub.response
        FROM cell_counts cc
        JOIN samples s ON cc.sample_id = s.sample_id
        JOIN subjects sub ON s.subject_id = sub.subject_id
    ''')
    rows = cursor.fetchall()
    conn.close()

    populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']

    data = []

    for row in rows:
        sample_id = row[0]
        counts = [val if val is not None else 0 for val in row[1:6]]
        sample_type = row[6]
        condition = row[7]
        treatment = row[8]
        response = row[9]
        
        total_count = sum(counts)
        
        if total_count == 0:
            for i, pop in enumerate(populations):
                data.append({
                    'sample': sample_id,
                    'total_count': total_count,
                    'population': pop,
                    'count': counts[i],
                    'percentage': 0.0,
                    'sample_type': sample_type,
                    'condition': condition,
                    'treatment': treatment,
                    'response': response
                })
            continue

        for i, pop in enumerate(populations):
            count = counts[i]
            percentage = (count / total_count) * 100
            data.append({
                'sample': sample_id,
                'total_count': total_count,
                'population': pop,
                'count': count,
                'percentage': percentage,
                'sample_type': sample_type,
                'condition': condition,
                'treatment': treatment,
                'response': response
            })
            
    return data

def main():
    data = get_cell_frequency_data(DB_FILE)

    for item in data:
        print(f"{item['sample']:<15} {item['total_count']:<12} {item['population']:<15} {item['count']:<10} {item['percentage']:.2f}%")

if __name__ == "__main__":
    main()
