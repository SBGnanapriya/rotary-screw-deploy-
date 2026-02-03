import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ----------------------------------
# Load dataset
# ----------------------------------
df = pd.read_csv("compressor_data.csv")

print("Dataset Shape:", df.shape)
print("\nMissing Values:\n", df.isnull().sum())
print("\nLabel Distribution:\n", df['Label'].value_counts())

# ----------------------------------
# Feature selection
# ----------------------------------
X = df[
    [
        'Motor_Current_A',
        'Oil_Temperature_C',
        'Line_Pressure_bar',
        'Filter_DeltaP_bar',
        'Running_Hours',
        'Vibration_RMS_mm_s'
    ]
]

y = df['Label']

# ----------------------------------
# Train-test split
# ----------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ----------------------------------
# Model training
# ----------------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ----------------------------------
# Model evaluation
# ----------------------------------
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# ----------------------------------
# Save trained model
# ----------------------------------
joblib.dump(model, "compressor_fault_model.pkl")

print("\nModel saved as compressor_fault_model.pkl")
