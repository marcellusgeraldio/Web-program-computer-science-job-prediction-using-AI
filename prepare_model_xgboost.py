import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

print("--- Memulai Proses Persiapan Model XGBoost Final (dengan Urutan Kolom) ---")

# 1. Muat dataset baru Anda
try:
    df = pd.read_csv('cleaned_cs_students.csv')
    print(f"Berhasil memuat dataset baru. Jumlah data: {len(df)} baris.")
except FileNotFoundError:
    print("ERROR: Pastikan file 'cleaned_cs_students.csv' ada di folder yang sama.")
    exit()

# 2. Lakukan pengelompokan kelas
career_to_group_map = {
    'Web Developer': 'Web Development', 'Frontend Developer': 'Web Development', 'Backend Developer': 'Web Development', 'Fullstack Developer': 'Web Development',
    'Ai Engineer': 'AI & Data', 'Machine Learning Engineer': 'AI & Data', 'Data Scientist': 'AI & Data', 'Data Analyst': 'AI & Data', 'Business Intelligence': 'AI & Data', 'Database Administrator': 'AI & Data',
    'Nlp Research Scientist': 'AI & Data', 'Ai Researcher': 'AI & Data', 'Bioinformatician': 'AI & Data', 'Machine Learning Researcher': 'AI & Data', 'Nlp Engineer': 'AI & Data', 'Computer Vision Engineer': 'AI & Data', 'Geospatial Analyst': 'AI & Data',
    'Software Engineer': 'Software Engineering', 'Software Developer': 'Software Engineering', 'System Architect': 'Software Engineering', 'Qa Engineer': 'Software Engineering', 'Distributed Systems Engineer': 'Software Engineering',
    'Mobile Developer': 'Mobile Development', 'Android Developer': 'Mobile Development', 'Ios Developer': 'Mobile Development', 'Mobile App Developer': 'Mobile Development',
    'Cybersecurity Analyst': 'Cybersecurity', 'Security Engineer': 'Cybersecurity', 'Information Security Analyst': 'Cybersecurity', 'Ethical Hacker': 'Cybersecurity', 'Data Privacy Specialist': 'Cybersecurity', 'Digital Forensics Specialist': 'Cybersecurity', 'Security Analyst': 'Cybersecurity',
    'Game Developer': 'Game & Graphics', 'Graphics Programmer': 'Game & Graphics', 'Vr Developer': 'Game & Graphics',
    'Cloud Engineer': 'Cloud & Infra', 'Network Engineer': 'Cloud & Infra', 'Devops Engineer': 'Cloud & Infra', 'Cloud Solutions Architect': 'Cloud & Infra',
    'Ux Designer': 'UI/UX & Product', 'Product Manager': 'UI/UX & Product', 'Seo Specialist': 'UI/UX & Product',
    'Blockchain Engineer': 'Emerging Tech', 'Robotics Engineer': 'Emerging Tech', 'Embedded Software Engineer': 'Emerging Tech', 'Iot Developer': 'Emerging Tech', 'Quantum Computing Researcher': 'Emerging Tech',
    'Healthcare It Specialist': 'Specialized IT'
}
df['Career_Group'] = df['Future Career'].apply(lambda x: career_to_group_map.get(x, 'Other'))

# 3. Preprocessing dan Menyiapkan Encoders
print("Menyiapkan dan menyimpan encoders...")
encoders = {}
skill_mapping = {'Basic': 0, 'Average': 1, 'Strong': 2}
df['Python'] = df['Python'].map(skill_mapping)
df['SQL'] = df['SQL'].map(skill_mapping)
df['Java'] = df['Java'].map(skill_mapping)
categorical_columns_to_encode = ['Gender', 'Major', 'Interested Domain', 'Projects']
for col in categorical_columns_to_encode:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le
le_target = LabelEncoder()
df['Career_Group'] = le_target.fit_transform(df['Career_Group'])
encoders['Career_Group'] = le_target
joblib.dump(encoders, 'encoders_xgb.joblib')
print("File 'encoders_xgb.joblib' berhasil disimpan.")

# 4. Finalisasi Data dan Simpan Urutan Kolom
X = df.drop(columns=['Student ID', 'Name', 'Future Career', 'Career_Group'])
y = df['Career_Group']

# --- [LANGKAH BARU YANG KRUSIAL] ---
# Simpan daftar dan urutan kolom yang benar ke dalam file
model_columns = X.columns.tolist()
joblib.dump(model_columns, 'model_columns.joblib')
print("Urutan kolom model telah disimpan ke 'model_columns.joblib'.")
# ------------------------------------

# 5. Latih dan Simpan Model
print("Melatih model XGBoost final pada seluruh data...")
best_params = {'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 100}
final_model = xgb.XGBClassifier(random_state=42, **best_params)
final_model.fit(X, y)
joblib.dump(final_model, 'xgboost_model.joblib')
print("Model 'xgboost_model.joblib' berhasil disimpan.")
print("\nPersiapan Selesai!")

