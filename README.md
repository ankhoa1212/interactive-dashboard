
# Teiko Technical Immune Cell Analysis

## Prerequisites


## Setup

Clone this repository:
```bash
git clone <repo-url>
cd teiko-technical
```

Install required packages:
```bash
pip install pandas streamlit matplotlib seaborn scipy
```

## Data Loading

To load the CSV file into the SQLite database:
```bash
python load_data.py
```

## Run Analyses

### Cell Frequency Summary
```bash
python initial_analysis.py
```

### Data Subset Analysis
```bash
python data_subset_analysis.py
```

### Statistical Analysis
```bash
python statistical_analysis.py
```

## Run the Dashboard

Launch the Streamlit dashboard:
```bash
streamlit run dashboard.py
```

## Dashboard Link

If the project is running locally, use this:
http://localhost:8501


## Database Schema & Rationale

The project uses a normalized relational schema in SQLite which separates the data into 3 parts:

**subjects**
- `subject_id` (primary key): Unique subject identifier
- `project_id`: Project identifier
- `condition`: Disease/condition (e.g., melanoma)
- `age`, `sex`, `treatment`, `response`: Subject metadata

**samples**
- `sample_id` (primary key): Unique sample identifier
- `subject_id` (foreign key): Linked to subjects
- `sample_type`: e.g., PBMC
- `time_from_treatment_start`: Integer (e.g., 0 for baseline)

**cell_counts**
- `id` (primary key): Row id
- `sample_id` (foreign key): Linked to samples
- `b_cell`, `cd8_t_cell`, `cd4_t_cell`, `nk_cell`, `monocyte`: Integer counts

**Database Explanation:**
- Dividing the data into subject, sample, cell count makes the data simpler to retrieve and analyze
- Dividing data on foreign keys (`subject_id`, `sample_id`) also makes it easier to add more data in the future

## Code Structure & Design

- `load_data.py`: Loads CSV data into the database
- `initial_analysis.py`: Computes cell population frequencies for all samples
- `data_subset_analysis.py`: Subset analysis (by project, response, sex)
- `statistical_analysis.py`: Creates a graph and compares responders vs non-responders with selectable statistical tests (Mann-Whitney U or t-test)
- `dashboard.py`: Streamlit dashboard for interactive exploration. Sidebar allows interactive data loading and test selection.
- `cell-count.csv`: Input data file (must be present in repo root).
- `cell-count.db`: Generated SQLite database.
- `response_comparison.png`: Generated boxplot from running `statistical_analysis.py`

**Code Explanation:**
- Each script has a separate, single responsibility
- Analysis logic is stored in separate scripts, making it easier to add/modify in the future
