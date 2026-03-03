# File: brain-engine/train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

def load_and_clean_data(filepath):
    """
    Loads the NSL-KDD dataset and strips away unusable columns.
    """
    print("[INFO] Loading dataset...")
    
    # The NSL-KDD dataset does not have a header row by default. 
    # We must define the columns we care about so Pandas can read it properly.
    # We are keeping only the 6 features Sonika can provide or we can calculate.
    col_names = [
        "duration", "protocol_type", "service", "flag", "src_bytes", 
        "dst_bytes", "land", "wrong_fragment", "urgent", "hot", 
        "num_failed_logins", "logged_in", "num_compromised", "root_shell", 
        "su_attempted", "num_root", "num_file_creations", "num_shells", 
        "num_access_files", "num_outbound_cmds", "is_host_login", 
        "is_guest_login", "count", "srv_count", "serror_rate", 
        "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate", 
        "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", 
        "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate", 
        "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", 
        "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate", 
        "dst_host_srv_rerror_rate", "label", "difficulty"
    ]
    
    # Load the CSV into a Pandas DataFrame
    df = pd.read_csv(filepath, names=col_names)
    
    # DROP the impossible columns. Keep ONLY the "Safe" features.
    # We keep 'label' temporarily so we know the answer key.
    safe_features = ['protocol_type', 'service', 'flag', 'src_bytes', 'count', 'label']
    df_clean = df[safe_features].copy()
    
    print(f"[INFO] Data cleaned. Remaining columns: {list(df_clean.columns)}")
    return df_clean

def preprocess_data(df):
    """
    Converts text data into numbers and separates features from the target label.
    """
    print("[INFO] Encoding text categories into numbers...")
    
    # Machine Learning models only understand numbers.
    # LabelEncoder turns "TCP" into 0, "UDP" into 1, etc.
    encoders = {}
    for col in ['protocol_type', 'service', 'flag']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le # We save the encoder in case we need to decode later
        
    # Convert the 'label' column into Binary (0 = Benign, 1 = Attack).
    # The dataset uses 'normal' for safe traffic.
    df['is_attack'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)
    
    # X = Features (The questions)
    # y = Target (The answers)
    X = df.drop(['label', 'is_attack'], axis=1)
    y = df['is_attack']
    
    return X, y

def train_and_save():
    """
    Main function to execute the training pipeline.
    """
    # 1. Load Data
    filepath = 'KDDTrain+.txt'
    df = load_and_clean_data(filepath)
    
    # 2. Preprocess Data
    X, y = preprocess_data(df)
    
    # 3. Train the Model
    print("[INFO] Training Random Forest Classifier. This may take a moment...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    print("[INFO] Model training complete.")
    
    # 4. Save the Model to disk
    joblib.dump(model, 'model.pkl')
    print("[SUCCESS] Brain saved as 'model.pkl'. Ready for deployment.")

# Standard Python idiom to ensure the script runs only when executed directly
if __name__ == "__main__":
    train_and_save()