import os
import json
import datetime
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Autenticación con Firebase
cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])
cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. Fecha de la rueda
today_str = datetime.date.today().strftime("%Y-%m-%d")

# 3. Lógica de mercado
bonos_data = [
    {"ticker": "AO27", "name": "Bono USD 2027 L.Arg", "currency": "MEP", "px": 97.50, "tir": 3.30, "duration": 1.05, "paridad": "97.5%", "vto": "29/10/2027", "var1d": -0.10, "vol": 4500000},
    {"ticker": "AL29", "name": "Bono USD 2029 L.Arg", "currency": "MEP", "px": 51.10, "tir": 13.30, "duration": 1.45, "paridad": "85.0%", "vto": "09/07/2029", "var1d": 0.15, "vol": 12000000},
    {"ticker": "GD29", "name": "Bono USD 2029 L.NY", "currency": "MEP", "px": 52.40, "tir": 9.05, "duration": 1.46, "paridad": "87.1%", "vto": "09/07/2029", "var1d": -0.30, "vol": 8900000},
    {"ticker": "AL30", "name": "Bono USD 2030 L.Arg", "currency": "MEP", "px": 52.05, "tir": 14.10, "duration": 1.88, "paridad": "81.2%", "vto": "09/07/2030", "var1d": 0.54, "vol": 25000000},
    {"ticker": "GD30", "name": "Bono USD 2030 L.NY", "currency": "MEP", "px": 54.35, "tir": 12.60, "duration": 1.91, "paridad": "84.8%", "vto": "09/07/2030", "var1d": 0.79, "vol": 18000000},
    {"ticker": "AO28", "name": "Bono USD 2028 L.Arg", "currency": "MEP", "px": 87.10, "tir": 16.10, "duration": 1.96, "paridad": "87.1%", "vto": "31/10/2028", "var1d": 0.57, "vol": 6400000},
    {"ticker": "AN29", "name": "Bono USD 2029 L.Arg", "currency": "MEP", "px": 82.45, "tir": 16.70, "duration": 2.81, "paridad": "80.7%", "vto": "30/11/2029", "var1d": 0.31, "vol": 3200000},
    {"ticker": "AO29", "name": "Bono USD 2029 L.Arg", "currency": "MEP", "px": 81.00, "tir": 16.90, "duration": 2.81, "paridad": "81.0%", "vto": "31/10/2029", "var1d": 0.97, "vol": 4100000},
    {"ticker": "GD38", "name": "Bono USD 2038 L.NY", "currency": "MEP", "px": 75.60, "tir": 12.90, "duration": 4.50, "paridad": "74.7%", "vto": "09/07/2038", "var1d": 0.73, "vol": 5400000},
    {"ticker": "AE38", "name": "Bono USD 2038 L.Arg", "currency": "MEP", "px": 69.75, "tir": 15.45, "duration": 4.33, "paridad": "69.0%", "vto": "09/01/2038", "var1d": 1.02, "vol": 4200000},
    {"ticker": "AL35", "name": "Bono USD 2035 L.Arg", "currency": "MEP", "px": 66.45, "tir": 14.80, "duration": 5.31, "paridad": "55.8%", "vto": "09/07/2035", "var1d": 0.68, "vol": 9500000},
    {"ticker": "GD35", "name": "Bono USD 2035 L.NY", "currency": "MEP", "px": 71.50, "tir": 13.90, "duration": 5.38, "paridad": "70.8%", "vto": "09/07/2035", "var1d": 0.77, "vol": 11000000},
    {"ticker": "AL41", "name": "Bono USD 2041 L.Arg", "currency": "MEP", "px": 61.87, "tir": 14.50, "duration": 5.53, "paridad": "51.4%", "vto": "09/07/2041", "var1d": 1.26, "vol": 3400000},
    {"ticker": "GD41", "name": "Bono USD 2041 L.NY", "currency": "MEP", "px": 66.80, "tir": 12.75, "duration": 5.73, "paridad": "66.3%", "vto": "09/07/2041", "var1d": 1.28, "vol": 3900000},
    {"ticker": "GD46", "name": "Bono USD 2046 L.NY", "currency": "MEP", "px": 62.10, "tir": 12.15, "duration": 6.10, "paridad": "67.7%", "vto": "09/07/2046", "var1d": 1.80, "vol": 2800000},
    {"ticker": "S30S6", "name": "Lecap Sep 2026", "currency": "ARS", "px": 117.41, "tir": 24.15, "duration": 0.08, "paridad": "100.0%", "vto": "30/09/2026", "var1d": 0.05, "vol": 32000000},
    {"ticker": "S30O6", "name": "Lecap Oct 2026", "currency": "ARS", "px": 133.05, "tir": 22.36, "duration": 0.16, "paridad": "100.0%", "vto": "30/10/2026", "var1d": 0.18, "vol": 28000000},
    {"ticker": "S30N6", "name": "Lecap Nov 2026", "currency": "ARS", "px": 124.83, "tir": 26.82, "duration": 0.25, "paridad": "100.0%", "vto": "30/11/2026", "var1d": 0.10, "vol": 21000000}
]

ons_data = [
       {"ticker": "YMCIO", "name": "YPF Clase 16 2026", "currency": "MEP", "px": 102.10, "tir": 6.85, "duration": 0.85, "paridad": "101.5%", "vto": "30/09/2026", "var1d": 0.05, "vol": 7400000},
       {"ticker": "YMCX",  "name": "YPF Clase 39 2027", "currency": "MEP", "px": 101.80, "tir": 7.40, "duration": 1.45, "paridad": "100.9%", "vto": "15/12/2027", "var1d": 0.10, "vol": 6200000},
       {"ticker": "YMCHO", "name": "YPF Clase 28 2029", "currency": "MEP", "px": 98.40,  tir: 8.20, "duration": 2.80, "paridad": "98.8%",  vto: "30/06/2029", var1d: -0.15, "vol": 8900000},
       {"ticker": "YMCQO", "name": "YPF Clase 35 2031", "currency": "MEP", "px": 96.20,  tir: 8.75, "duration": 3.90, "paridad": "97.1%",  vto: "01/06/2031", var1d: 0.25, "vol": 5100000},
       {"ticker": "MGC1O", "name": "Pampa Energía Clase 9 2026", "currency": "MEP", "px": 101.90, "tir": 6.95, "duration": 1.10, "paridad": "101.0%", "vto": "08/12/2026", var1d: 0.00, "vol": 4800000},
       {"ticker": "MGC9O", "name": "Pampa Energía Clase 18 2029", "currency": "MEP", "px": 99.10, "tir": 7.70, "duration": 2.65, "paridad": "99.4%", "vto": "15/04/2029", var1d: 0.08, "vol": 6400000},
       {"ticker": "PAC1O", "name": "Pan American Energy 2027", "currency": "MEP", "px": 103.50, "tir": 6.40, "duration": 1.25, "paridad": "102.3%", "vto": "27/11/2027", var1d: -0.05, "vol": 9200000},
       {"ticker": "PNDCO", "name": "Pan American Energy 2032", "currency": "MEP", "px": 99.80, "tir": 7.55, "duration": 4.10, "paridad": "99.2%", "vto": "30/04/2032", var1d: 0.12, "vol": 4100000},
       {"ticker": "TLC1O", "name": "Telecom Argentina 2027", "currency": "MEP", "px": 99.80, "tir": 8.40, "duration": 1.75, "paridad": "99.2%", "vto": "18/07/2027", var1d: 0.20, "vol": 5300000},
       {"ticker": "TLCMO", "name": "Telecom Argentina 2031", "currency": "MEP", "px": 95.70, "tir": 8.95, "duration": 3.80, "paridad": "96.5%", "vto": "15/09/2031", var1d: -0.30, "vol": 3600000},
       {"ticker": "VSC3O", "name": "Vista Energy Clase 3 2027", "currency": "MEP", "px": 102.40, "tir": 6.70, "duration": 1.30, "paridad": "101.8%", "vto": "24/02/2027", var1d: 0.10, "vol": 7100000},
       {"ticker": "VSC4O", "name": "Vista Energy Clase 4 2029", "currency": "MEP", "px": 98.90, "tir": 7.60, "duration": 2.70, "paridad": "99.0%", "vto": "10/08/2029", var1d: 0.18, "vol": 5900000},
       {"ticker": "RCCBO", "name": "Arcor Clase 18 2027", "currency": "MEP", "px": 104.10, "tir": 6.10, "duration": 1.15, "paridad": "103.2%", "vto": "09/10/2027", var1d: -0.02, "vol": 4200000},
       {"ticker": "IRC1O", "name": "IRSA Clase 14 2028", "currency": "MEP", "px": 101.40, "tir": 7.85, "duration": 2.10, "paridad": "100.8%", "vto": "22/06/2028", var1d: -0.12, "vol": 3100000},
       {"ticker": "CAC2O", "name": "Cresud Clase 43 2027", "currency": "MEP", "px": 100.50, "tir": 7.95, "duration": 1.40, "paridad": "100.1%", "vto": "12/03/2027", var1d: 0.00, "vol": 2400000},
       {"ticker": "CP33O", "name": "CGC Clase 33 2028", "currency": "MEP", "px": 97.20, "tir": 8.60, "duration": 2.35, "paridad": "97.9%", "vto": "10/11/2028", var1d: 0.40, "vol": 2900000},
       {"ticker": "TTC2O", "name": "Tecpetrol Clase 2 2027", "currency": "MEP", "px": 102.80, "tir": 6.65, "duration": 1.35, "paridad": "102.1%", "vto": "18/05/2027", var1d: -0.08, "vol": 3800000}
   ]

payload = {
    "fecha": today_str,
    "timestamp": firestore.SERVER_TIMESTAMP,
    "bonos": bonos_data,
    "ons": ons_data
}

# 4. Guardar en Firestore
db.collection("market_data").document(today_str).set(payload)
print(f"Datos de mercado para {today_str} guardados correctamente.")
