from flask import Flask, render_template, jsonify, request
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Sample ESG data and ESI data
esg_data = {
    "State": ["Manipur", "Sikkim", "Tripura", "Nagaland", "Mizoram", "Arunachal Pradesh",
              "Chhattisgarh", "Orissa", "Uttaranchal", "Assam", "Meghalaya", "Jharkhand",
              "Kerala", "Bihar", "Jammu & Kashmir", "Goa", "Madhya Pradesh", "Maharashtra",
              "West Bengal", "Tamil Nadu", "Himachal Pradesh", "Karnataka", "Andhra Pradesh",
              "Rajasthan", "Haryana", "Uttar Pradesh", "Gujarat", "Punjab"],
    "Environmental Score": [80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 50, 60, 70, 80, 30, 25, 20, 15, 10, 5, 45, 40],
    "Social Score": [85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 55, 65, 75, 85, 35, 30, 25, 20, 15, 10, 50, 45],
    "Governance Score": [90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 60, 70, 80, 90, 40, 35, 30, 25, 20, 15, 55, 50]
}

esi_data = {
    "State": ["Manipur", "Sikkim", "Tripura", "Nagaland", "Mizoram", "Arunachal Pradesh",
              "Chhattisgarh", "Orissa", "Uttaranchal", "Assam", "Meghalaya", "Jharkhand",
              "Kerala", "Bihar", "Jammu & Kashmir", "Goa", "Madhya Pradesh", "Maharashtra",
              "West Bengal", "Tamil Nadu", "Himachal Pradesh", "Karnataka", "Andhra Pradesh",
              "Rajasthan", "Haryana", "Uttar Pradesh", "Gujarat", "Punjab"],
    "Combined ESI": [78, 74, 72, 66, 62, 58, 54, 48, 43, 38, 33, 28, 23, 18, 13, 8, 53, 64, 70, 76, 32, 28, 23, 18, 13, 8, 47, 44]
}

# Convert data to DataFrames
esg_df = pd.DataFrame(esg_data)
esi_df = pd.DataFrame(esi_data)

# Prepare the dataset for the model
merged_df = pd.merge(esg_df, esi_df, on="State")
X = merged_df[['Environmental Score', 'Social Score', 'Governance Score']]
y = merged_df['Combined ESI']

# Train a RandomForestRegressor model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations_by_sector', methods=['POST'])
def recommendations_by_sector():
    sector = request.form.get('sector')
    print(f"Received sector: {sector}")  # Debug print
    
    # Define sector-specific logic for recommendations
    if sector == 'solar_energy':
        recommended_states = esi_df.sort_values(by='Combined ESI', ascending=False).head(5)
    elif sector == 'sustainable_agriculture':
        recommended_states = esi_df.sort_values(by='Combined ESI', ascending=True).head(5)
    elif sector == 'wind_energy':
        # Add specific logic for wind energy
        recommended_states = esi_df.sort_values(by='Combined ESI', ascending=False).head(5)
    elif sector == 'hydropower':
        # Add specific logic for hydropower
        recommended_states = esi_df.sort_values(by='Combined ESI', ascending=True).head(5)
    elif sector == 'bioenergy':
        # Add specific logic for bioenergy
        recommended_states = esi_df.sort_values(by='Combined ESI', ascending=False).head(5)
    else:
        recommended_states = esi_df.sort_values(by='Combined ESI', ascending=False).head(5)
    
    print(f"Recommendations: {recommended_states}")  # Debug print
    return jsonify(recommended_states.to_dict(orient='records'))

@app.route('/risk_assessment', methods=['GET'])
def risk_assessment():
    sector = request.args.get('sector')
    print(f"Received sector: {sector}")  # Debug print
    
    # Define sector-specific logic for risk assessment
    if sector == 'solar_energy':
        trend = "Growing"
        risk = "Low Risk"
    elif sector == 'sustainable_agriculture':
        trend = "Stable"
        risk = "Moderate Risk"
    elif sector == 'wind_energy':
        trend = "Growing"
        risk = "Moderate Risk"
    elif sector == 'hydropower':
        trend = "Stable"
        risk = "Low Risk"
    elif sector == 'bioenergy':
        trend = "Growing"
        risk = "High Risk"
    else:
        trend = "Unknown"
        risk = "Unknown Risk"
    
    print(f"Trend: {trend}, Risk: {risk}")  # Debug print
    return jsonify({"trend": trend, "risk": risk})

if __name__ == '__main__':
    app.run(debug=True)
