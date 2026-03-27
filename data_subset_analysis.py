import sqlite3
import pandas as pd

DB_FILE = 'cell-count.db'


def data_subset_analysis(return_dict=False, filters=None):
    """Analyze subset of data based on filters and print summary statistics."""
    conn = sqlite3.connect(DB_FILE)
    if filters is None:  # set default filters
        filters = {
            'condition': 'melanoma',
            'sample_type': 'PBMC',
            'time_from_treatment_start': 0,
            'treatment': 'miraclib'
        }
    where_clauses = []  # apply filters to SQL query
    params = []
    if 'condition' in filters and filters['condition'] is not None:
        where_clauses.append('s.condition = ?')
        params.append(filters['condition'])
    if 'sample_type' in filters and filters['sample_type'] is not None:
        where_clauses.append('sam.sample_type = ?')
        params.append(filters['sample_type'])
    if 'time_from_treatment_start' in filters and filters['time_from_treatment_start'] is not None:
        where_clauses.append('sam.time_from_treatment_start = ?')
        params.append(filters['time_from_treatment_start'])
    if 'treatment' in filters and filters['treatment'] is not None:
        where_clauses.append('s.treatment = ?')
        params.append(filters['treatment'])
    where_sql = ''
    if where_clauses:
        where_sql = 'WHERE ' + ' AND '.join(where_clauses)
    query = f'''
    SELECT 
        s.project_id,
        s.subject_id,
        s.sex,
        s.response,
        s.condition,
        s.treatment,
        sam.sample_id,
        sam.sample_type,
        sam.time_from_treatment_start
    FROM samples sam
    JOIN subjects s ON sam.subject_id = s.subject_id
    {where_sql}
    '''
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    if df.empty:
        if return_dict:
            return {
                'project_counts': pd.Series(dtype='int'),
                'response_counts': pd.Series(dtype='int'),
                'sex_counts': pd.Series(dtype='int'),
                'unique_subjects': 0,
                'unique_samples': 0
            }
        print("No samples found matching the criteria.")
        return

    project_counts = df['project_id'].value_counts()
    unique_subjects_df = df.drop_duplicates(subset=['subject_id'])
    response_counts = unique_subjects_df['response'].value_counts(dropna=False)
    sex_counts = unique_subjects_df['sex'].value_counts(dropna=False)
    unique_subjects = len(unique_subjects_df)
    unique_samples = len(df.drop_duplicates(subset=['sample_id']))

    if return_dict:
        return {
            'project_counts': project_counts,
            'response_counts': response_counts,
            'sex_counts': sex_counts,
            'unique_subjects': unique_subjects,
            'unique_samples': unique_samples
        }

    print("Samples per Project:")
    print(project_counts.to_string())
    print("\nUnique subjects:", unique_subjects)
    print("Subject Response Counts:")
    print(response_counts.to_string())
    print("Subject Sex Counts:")
    print(sex_counts.to_string())

if __name__ == "__main__":
    data_subset_analysis()
