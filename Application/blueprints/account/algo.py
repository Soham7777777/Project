import joblib
import numpy as np

def algorithm(df_otherTestingData):
    ensemble = joblib.load('ensemble.pkl')
    scaler = joblib.load('std_scaler.bin')

    df_otherTestingData['Target'] = np.nan
    X_Other_test = df_otherTestingData.drop(['Company', 'Target'], axis=1)
    y_Other_test = df_otherTestingData['Target']
    X_Other_test_scaled = scaler.transform(X_Other_test)

    return ensemble.predict(X_Other_test_scaled)
    