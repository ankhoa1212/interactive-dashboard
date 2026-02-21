import sqlite3
import pandas as pd

DB_FILE = 'cell-count.db'



def data_subset_analysis(return_dict=False, filters=None):
    conn = sqlite3.connect(DB_FILE)
    query = '''
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
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Filters removed; analysis now runs on all samples in the database

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
