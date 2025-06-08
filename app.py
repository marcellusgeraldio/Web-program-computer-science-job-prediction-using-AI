from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)
CORS(app)

# Muat SEMUA aset: model, encoders, dan urutan kolom
print("Memuat model, encoders, dan urutan kolom...")
try:
    model = joblib.load("xgboost_model.joblib")
    encoders = joblib.load("encoders_xgb.joblib")
    model_columns = joblib.load("model_columns.joblib") # Memuat daftar urutan kolom
    print("Semua aset berhasil dimuat.")
except FileNotFoundError:
    print("ERROR: Pastikan file 'xgboost_model.joblib', 'encoders_xgb.joblib', dan 'model_columns.joblib' ada.")
    model = None
    encoders = None
    model_columns = None

@app.route('/predict', methods=['POST'])
def predict():
    if not all([model, encoders, model_columns]):
        return jsonify({'error': 'Aset model tidak termuat dengan lengkap!'}), 500

    data = request.get_json()
    print(f"Data diterima: {data}")

    try:
        input_df = pd.DataFrame([data])
        
        # Preprocessing data input
        skill_mapping = {'Basic': 0, 'Average': 1, 'Strong': 2}
        input_df['Python'] = input_df['Python'].map(skill_mapping)
        input_df['SQL'] = input_df['SQL'].map(skill_mapping)
        input_df['Java'] = input_df['Java'].map(skill_mapping)

        for col, encoder in encoders.items():
            if col in input_df.columns and col != 'Career_Group':
                try:
                    input_df[col] = encoder.transform(input_df[col])
                except Exception:
                    input_df[col] = -1 
        
        # --- [PERBAIKAN UTAMA] ---
        # Pastikan DataFrame memiliki semua kolom yang dibutuhkan model, isi dengan 0 jika tidak ada
        for col in model_columns:
            if col not in input_df.columns:
                input_df[col] = 0
        
        # Susun ulang kolom DataFrame agar sama persis dengan urutan saat training
        input_df = input_df[model_columns]
        # ---------------------------
        
        print(f"Data setelah di-preprocess dan diurutkan: {input_df.to_dict()}")

        # Dapatkan Top 3 Prediksi
        probabilities = model.predict_proba(input_df)[0]
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        
        top_3_results = []
        for i in top_3_indices:
            class_name = encoders['Career_Group'].inverse_transform([i])[0]
            probability = round(probabilities[i] * 100, 1)
            top_3_results.append({
                "group": class_name,
                "probability": f"{probability}%"
            })
        
        print(f"Hasil Top 3 Prediksi: {top_3_results}")
        return jsonify({'prediction': top_3_results})

    except Exception as e:
        import traceback
        print(f"Error saat preprocessing atau prediksi: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)

