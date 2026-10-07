import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.calibration import CalibratedClassifierCV, CalibrationDisplay
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.benchmark_engine import load_and_prep_data

def calibrate_and_plot(X, y, name="jds"):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    clf = XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42)
    clf.fit(X_train, y_train)
    
    cal_sigmoid = CalibratedClassifierCV(clf, cv=5, method="sigmoid")
    cal_sigmoid.fit(X_train, y_train) 
    
    cal_isotonic = CalibratedClassifierCV(clf, cv=5, method="isotonic")
    cal_isotonic.fit(X_train, y_train)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    CalibrationDisplay.from_estimator(clf, X_test, y_test, n_bins=10, ax=ax, name="Uncalibrated")
    CalibrationDisplay.from_estimator(cal_sigmoid, X_test, y_test, n_bins=10, ax=ax, name="Sigmoid")
    CalibrationDisplay.from_estimator(cal_isotonic, X_test, y_test, n_bins=10, ax=ax, name="Isotonic")
    
    plt.title(f"Calibration Curves - {name.upper()}")
    
    os.makedirs("reports/figures", exist_ok=True)
    plt.savefig(f"reports/figures/calibration_{name}.png")
    plt.close()

if __name__ == "__main__":
    X_jds, y_jds = load_and_prep_data("data/processed/jds_skills_clean.xlsx", "jds")
    calibrate_and_plot(X_jds, y_jds, "jds")
    
    X_sds, y_sds = load_and_prep_data("data/processed/sds_personality_clean.xlsx", "sds")
    calibrate_and_plot(X_sds, y_sds, "sds")
