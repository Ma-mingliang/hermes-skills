# Python Data Analysis Tool Patterns

For embedded/IoT projects that collect sensor data and need offline analysis.

## Core Dependencies
```bash
pip install pandas matplotlib numpy scipy
```

## Standard Analysis Pipeline

```python
def load_data(csv_file):
    df = pd.read_csv(csv_file)
    df['time_ms'] = (df['timestamp'] - df['timestamp'].iloc[0]) / 1000.0
    return df

def plot_response(df, output_dir=None):
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    # Plot pitch, roll, batt on separate subplots
    plt.tight_layout()
    if output_dir:
        plt.savefig(os.path.join(output_dir, f'response_plot_{timestamp}.png'), dpi=150)

def analyze_performance(df):
    # Stats: mean, std, min, max, peak-to-peak
    # Steady-state analysis: last N samples
    # Dynamic: settling time, overshoot
```

## Advanced Analysis Functions

### Frequency Analysis (FFT)
```python
from scipy import signal
freqs, psd = signal.welch(pitch_data, fs, nperseg=min(256, len(pitch_data)))
dominant_freq = freqs[np.argmax(psd)]
```
Use: Identify vibration frequencies, control loop oscillations.

### Correlation Analysis
```python
corr_matrix = df[['pitch', 'roll', 'batt']].corr()
```
Use: Find relationships between variables (e.g., battery drop → pitch drift).

### Dataset Comparison
```python
def compare_datasets(df1, df2, labels):
    # Overlay plots with different colors
    # Print statistical comparison
```
Use: Before/after PID tuning comparison, different mode comparison.

### Auto-Report Generation
Generate text report with:
- Basic statistics
- Performance assessment (excellent/good/needs improvement)
- Actionable recommendations (e.g., "reduce Kp" if std > 2°)

## CLI Interface
```bash
python analyze_data.py data.csv                           # Basic analysis
python analyze_data.py data.csv --frequency               # FFT analysis
python analyze_data.py data.csv --correlation             # Correlation matrix
python analyze_data.py data.csv --compare other.csv       # Compare datasets
python analyze_data.py data.csv --report                  # Generate report
python analyze_data.py data.csv --frequency --report -o   # Full analysis
```

## Performance Assessment Criteria

| Metric | Excellent | Good | Needs Work |
|--------|-----------|------|------------|
| Pitch std | < 1° | < 2° | > 2° |
| Roll std | < 1° | < 2° | > 2° |
| Battery | > 11V | > 10V | < 10V |
| Settling time | < 1s | < 2s | > 2s |
| Overshoot | < 5% | < 10% | > 10% |
