from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
import joblib
import pickle
# import pandas as pd
# import numpy as np
from sklearn.ensemble import RandomForestClassifier
from django.db.models import Q
from rest_framework.response import Response
import os



class USERSSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    bloodTest_model = serializers.SerializerMethodField()
    diabtesTest_model = serializers.SerializerMethodField()
    parkinsonTest_model = serializers.SerializerMethodField()
    alzhimarTest_model = serializers.SerializerMethodField()
    heartTest_model = serializers.SerializerMethodField()
    class Meta :
        model = USERS
        fields = '__all__'
    def get_user(self, instance):
        return instance.user.username
    def get_user_id(self, instance):
        return instance.user.id
    def get_email(self, instance):
        return instance.user.email
    def get_bloodTest_model(self,instance):
        user_id = instance.user
        try :
            query_set = bloodTest.objects.get(user=user_id).result
        except :
            return None
        return str(query_set)

    def get_diabtesTest_model(self,instance):
        user_id = instance.user
        try :
            query_set = diabtesTest.objects.get(user=user_id).result
        except :
            return None
        return str(query_set)

    def get_parkinsonTest_model(self,instance):
        user_id = instance.user
        try :
            query_set = parkinsonTest.objects.get(user=user_id).result
        except :
            return None
        return str(query_set)

    def get_alzhimarTest_model(self,instance):
        user_id = instance.user
        try :
            query_set = alzhimarTest.objects.get(user=user_id).result
        except :
            return None
        return str(query_set)

    def get_heartTest_model(self,instance):
        user_id = instance.user
        try :
            query_set = heartTest.objects.get(user=user_id).result
        except :
            return None
        return str(query_set)


class bloodTestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(), )
    patient_name = serializers.SerializerMethodField()
    class Meta :
        model = bloodTest
        fields = '__all__'
    def get_patient_name(self,instance):
        return f"{instance.user.first_name} {instance.user.last_name}"

    def validate(self, data):
        age = data.get('age')
        bmi = data.get('bmi')
        glucouse = data.get('glucouse')
        insuline = data.get('insuline')
        homa = data.get('homa')
        leptin = data.get('leptin')
        adiponcetin = data.get('adiponcetin')
        resistiin = data.get('resistiin')
        mcp = data.get('mcp')

        if age < 0 or age > 100:
            raise serializers.ValidationError("Age must be between 0 and 100.")
        if bmi < 0 or bmi > 100:
            raise serializers.ValidationError("BMI must be between 0 and 100.")
        if glucouse < 0 or glucouse > 300:
            raise serializers.ValidationError("Glucose must be between 0 and 300.")
        if insuline < 0 or insuline > 20:
            raise serializers.ValidationError("Insuline must be between 0 and 20.")
        if homa < 0 or homa > 10:
            raise serializers.ValidationError("Homa must be between 0 and 10.")
        if leptin < 0 or leptin > 30:
            raise serializers.ValidationError("Leptin must be between 0 and 30.")
        if adiponcetin < 0 or adiponcetin > 30:
            raise serializers.ValidationError("Adiponcetin must be between 0 and 30.")
        if resistiin < 0 or resistiin > 30:
            raise serializers.ValidationError("Resistiin must be between 0 and 30.")
        if mcp < 0 or mcp > 30:
            raise serializers.ValidationError("MCP must be between 0 and 30.")

        return data
    def predict(self):
        data = self.validated_data
        age = data.get('age')
        bmi = data.get('bmi')
        glucouse = data.get('glucouse')
        insuline = data.get('insuline')
        homa = data.get('homa')
        leptin = data.get('leptin')
        adiponcetin = data.get('adiponcetin')
        resistiin = data.get('resistiin')
        mcp = data.get('mcp')
        all_data = [age, bmi, glucouse, insuline, homa, leptin, adiponcetin, resistiin, mcp]

        loaded_model = joblib.load(open("/home/IllAcc/illminor_backend/ml_models/bloodmodelRBF", 'rb'))
        print(os.getcwd())
        clf = loaded_model.predict([all_data])
        result = None
        if clf[0] == 0:
            result = "No Cancer"
        elif clf[0] == 1:
            result = "Cancer"

        # self.instance.result = result

        return result


class diabtesTestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(), )
    patient_name = serializers.SerializerMethodField()
    class Meta :
        model = diabtesTest
        fields = '__all__'
    def get_patient_name(self,instance):
        return f"{instance.user.first_name} {instance.user.last_name}"

    def validate(self, data):
        pregnancies = data.get('pregnancies')
        glucose = data.get('glucose')
        bloodpressure = data.get('bloodpressure')
        skinthickness = data.get('skinthickness')
        insulin = data.get('insulin')
        bmi = data.get('bmi')
        dpf = data.get('dpf')
        age = data.get('age')
        if pregnancies < 0 or pregnancies > 100:
            raise serializers.ValidationError("pregnancies must be between 0 and 100.")
        if glucose < 0 or glucose > 300:
            raise serializers.ValidationError("glucose must be between 0 and 300.")
        if bloodpressure < 0 or bloodpressure > 20:
            raise serializers.ValidationError("bloodpressure must be between 0 and 20.")
        if skinthickness < 0 or skinthickness > 10:
            raise serializers.ValidationError("skinthickness must be between 0 and 10.")
        if insulin < 0 or insulin > 30:
            raise serializers.ValidationError("insulin must be between 0 and 30.")
        if bmi < 0 or bmi > 30:
            raise serializers.ValidationError("bmi must be between 0 and 30.")
        if dpf < 0 or dpf > 30:
            raise serializers.ValidationError("dpf must be between 0 and 30.")
        if age < 0 or age > 100:
            raise serializers.ValidationError("Age must be between 0 and 100.")
        return data
    def predict(self):
        data = self.validated_data
        pregnancies = data.get('pregnancies')
        glucose = data.get('glucose')
        bloodpressure = data.get('bloodpressure')
        skinthickness = data.get('skinthickness')
        insulin = data.get('insulin')
        bmi = data.get('bmi')
        dpf = data.get('dpf')
        age = data.get('age')
        all_data = [pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, age,]

        loaded_model=pickle.load(open("ml_models/diabetes-prediction-rfc-model.pkl", "rb"))
        prediction = loaded_model.predict([all_data])
        result = None
        if int(prediction[0]) == 1:
            result = 'diabetic'
        elif int(prediction[0]) == 0:
            result = "not diabetic"
        return result

class parkinsonTestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(), )
    patient_name = serializers.SerializerMethodField()
    class Meta :
        model = parkinsonTest
        fields = '__all__'
    def get_patient_name(self,instance):
        return f"{instance.user.first_name} {instance.user.last_name}"
    def validate(self, data):
        MDVP_Fo_Hz = data.get('MDVP_Fo_Hz')
        MDVP_Fhi_Hz = data.get('MDVP_Fhi_Hz')
        MDVP_Flo_Hz = data.get('MDVP_Flo_Hz')
        MDVP_Jitter = data.get('MDVP_Jitter')
        MDVP_Jitter_Abs = data.get('MDVP_Jitter_Abs')
        MDVP_RAP = data.get('MDVP_RAP')
        MDVP_PPQ = data.get('MDVP_PPQ')
        Jitter_DDP = data.get('Jitter_DDP')
        MDVP_Shimmer = data.get('MDVP_Shimmer')
        MDVP_Shimmer_dB = data.get('MDVP_Shimmer_dB')
        Shimmer_APQ3 = data.get('Shimmer_APQ3')
        Shimmer_APQ5 = data.get('Shimmer_APQ5')
        MDVP_APQ = data.get('MDVP_APQ')
        Shimmer_DDA = data.get('Shimmer_DDA')
        NHR = data.get('NHR')
        HNR = data.get('HNR')
        RPDE = data.get('RPDE')
        DFA = data.get('DFA')
        spread1 = data.get('spread1')
        spread2 = data.get('spread2')
        D2 = data.get('D2')
        PPE = data.get('PPE')
        if MDVP_Fo_Hz < 0 or MDVP_Fo_Hz > 100:
            raise serializers.ValidationError("MDVP_Fo_Hz must be between 0 and 100.")
        if MDVP_Fhi_Hz < 0 or MDVP_Fhi_Hz > 300:
            raise serializers.ValidationError("MDVP_Fhi_Hz must be between 0 and 300.")
        if MDVP_Flo_Hz < 0 or MDVP_Flo_Hz > 20:
            raise serializers.ValidationError("MDVP_Flo_Hz must be between 0 and 20.")
        if MDVP_Jitter < 0 or MDVP_Jitter > 10:
            raise serializers.ValidationError("MDVP_Jitter must be between 0 and 10.")
        if MDVP_Jitter_Abs < 0 or MDVP_Jitter_Abs > 30:
            raise serializers.ValidationError("MDVP_Jitter_Abs must be between 0 and 30.")
        if MDVP_RAP < 0 or MDVP_RAP > 30:
            raise serializers.ValidationError("MDVP_RAP must be between 0 and 30.")
        if MDVP_PPQ < 0 or MDVP_PPQ > 30:
            raise serializers.ValidationError("MDVP_PPQ must be between 0 and 30.")
        if Jitter_DDP < 0 or Jitter_DDP > 30:
            raise serializers.ValidationError("Jitter_DDP must be between 0 and 30.")
        if MDVP_Shimmer < 0 or MDVP_Shimmer > 30:
            raise serializers.ValidationError("MDVP_Shimmer must be between 0 and 30.")

        if MDVP_Shimmer_dB < 0 or MDVP_Shimmer_dB > 30:
            raise serializers.ValidationError("MDVP_Shimmer_dB must be between 0 and 30.")

        if Shimmer_APQ3 < 0 or Shimmer_APQ3 > 30:
            raise serializers.ValidationError("Shimmer_APQ3 must be between 0 and 30.")

        if Shimmer_APQ5 < 0 or Shimmer_APQ5 > 30:
            raise serializers.ValidationError("Shimmer_APQ5 must be between 0 and 30.")

        if MDVP_APQ < 0 or MDVP_APQ > 30:
            raise serializers.ValidationError("Shimmer_APQ5 must be between 0 and 30.")

        if Shimmer_DDA < 0 or Shimmer_DDA > 30:
            raise serializers.ValidationError("Shimmer_APQ5 must be between 0 and 30.")

        if NHR < 0 or NHR > 30:
            raise serializers.ValidationError("NHR must be between 0 and 30.")

        if HNR < 0 or HNR > 30:
            raise serializers.ValidationError("HNR must be between 0 and 30.")

        if RPDE < 0 or RPDE > 30:
            raise serializers.ValidationError("RPDE must be between 0 and 30.")

        if DFA < 0 or DFA > 30:
            raise serializers.ValidationError("HNR must be between 0 and 30.")

        if spread1 < 0 or spread1 > 30:
            raise serializers.ValidationError("spread1 must be between 0 and 30.")

        if spread2 < 0 or spread2 > 30:
            raise serializers.ValidationError("spread2 must be between 0 and 30.")

        if D2 < 0 or D2 > 30:
            raise serializers.ValidationError("spread2 must be between 0 and 30.")

        if PPE < 0 or PPE > 30:
            raise serializers.ValidationError("spread2 must be between 0 and 30.")
        return data
    def predict(self):
        data = self.validated_data
        MDVP_Fo_Hz = data.get('MDVP_Fo_Hz')
        MDVP_Fhi_Hz = data.get('MDVP_Fhi_Hz')
        MDVP_Flo_Hz = data.get('MDVP_Flo_Hz')
        MDVP_Jitter = data.get('MDVP_Jitter')
        MDVP_Jitter_Abs = data.get('MDVP_Jitter_Abs')
        MDVP_RAP = data.get('MDVP_RAP')
        MDVP_PPQ = data.get('MDVP_PPQ')
        Jitter_DDP = data.get('Jitter_DDP')
        MDVP_Shimmer = data.get('MDVP_Shimmer')
        MDVP_Shimmer_dB = data.get('MDVP_Shimmer_dB')
        Shimmer_APQ3 = data.get('Shimmer_APQ3')
        Shimmer_APQ5 = data.get('Shimmer_APQ5')
        MDVP_APQ = data.get('MDVP_APQ')
        Shimmer_DDA = data.get('Shimmer_DDA')
        NHR = data.get('NHR')
        HNR = data.get('HNR')
        RPDE = data.get('RPDE')
        DFA = data.get('DFA')
        spread1 = data.get('spread1')
        spread2 = data.get('spread2')
        D2 = data.get('D2')
        PPE = data.get('PPE')
        all_data = [MDVP_Fo_Hz, MDVP_Fhi_Hz, MDVP_Flo_Hz, MDVP_Jitter, MDVP_Jitter_Abs, MDVP_RAP, MDVP_PPQ, Jitter_DDP, MDVP_Shimmer,
                    MDVP_Shimmer_dB, Shimmer_APQ3, Shimmer_APQ5, MDVP_APQ, Shimmer_DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
        loaded_model=joblib.load(open("ml_models/Predict_Parkinson.model", "rb"))
        # loaded_model=joblib.load("ml_models/Predict_Parkinson.model")

        prediction = loaded_model.predict([all_data])
        result = None
        if prediction == 0:
            result = "Uninfected"
        else:
            result = "infected"
        return result

class alzhimarTestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(), )
    patient_name = serializers.SerializerMethodField()
    class Meta :
        model = alzhimarTest
        fields = '__all__'
    def get_patient_name(self,instance):
        return f"{instance.user.first_name} {instance.user.last_name}"

    def validate(self, data):
        gender = data.get('gender')
        Age = data.get('Age')
        EDUC = data.get('EDUC')
        SES = data.get('SES')
        MMSE = data.get('MMSE')
        eTIV = data.get('eTIV')
        nWBV = data.get('nWBV')
        ASF = data.get('ASF')
        if gender < 0 or gender > 1:
            raise serializers.ValidationError("gender must be between 0 and 1.")
        if Age < 0 or Age > 100:
            raise serializers.ValidationError("Age must be between 0 and 100.")
        if EDUC < 0 or EDUC > 20:
            raise serializers.ValidationError("EDUC must be between 0 and 20.")
        if SES < 0 or SES > 100:
            raise serializers.ValidationError("SES must be between 0 and 10.")
        if MMSE < 0 or MMSE > 30:
            raise serializers.ValidationError("MMSE must be between 0 and 30.")
        if eTIV < 0 or eTIV > 30:
            raise serializers.ValidationError("eTIV must be between 0 and 30.")
        if nWBV < 0 or nWBV > 30:
            raise serializers.ValidationError("nWBV must be between 0 and 30.")
        if ASF < 0 or ASF > 100:
            raise serializers.ValidationError("ASF must be between 0 and 100.")
        return data
    def predict(self):
        data = self.validated_data
        gender = data.get('gender')
        age = data.get('Age')
        EDUC = data.get('EDUC')
        SES = data.get('SES')
        MMSE = data.get('MMSE')
        eTIV = data.get('eTIV')
        nWBV = data.get('nWBV')
        ASF = data.get('ASF')
        all_data = [gender, age, EDUC, SES, MMSE, eTIV, nWBV, ASF]
        scaler = pickle.load(open("ml_models/alzheimer.scl", "rb"))
        loaded_model = pickle.load(open(r"ml_models/alzheimer.model", "rb"))
        scaled_feature = scaler.transform([all_data])
        prediction = loaded_model.predict(scaled_feature)
        result = None
        if (prediction == 0):
            result = "Nondemented"
        elif (prediction == 1):
            result = "Demented"
        return result

class heartTestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(), )
    patient_name = serializers.SerializerMethodField()
    class Meta :
        model = heartTest
        fields = '__all__'
    def get_patient_name(self,instance):
        return f"{instance.user.first_name} {instance.user.last_name}"

    # def validate(self, data):
    #     age = data.get('age')
    #     sex = data.get('sex')
    #     cp = data.get('cp')
    #     trestbps = data.get('trestbps')
    #     chol = data.get('chol')
    #     fbs = data.get('fbs')
    #     restecg = data.get('restecg')
    #     thalach = data.get('thalach')
    #     exang = data.get('exang')
    #     oldpeak = data.get('oldpeak')
    #     slope = data.get('slope')
    #     ca = data.get('ca')
    #     thal = data.get('thal')
    #     if age < 0 or age > 100:
    #         raise serializers.ValidationError("age must be between 0 and 1.")
    #     if Age < 0 or Age > 100:
    #         raise serializers.ValidationError("Age must be between 0 and 100.")
    #     if EDUC < 0 or EDUC > 20:
    #         raise serializers.ValidationError("EDUC must be between 0 and 20.")
    #     if SES < 0 or SES > 100:
    #         raise serializers.ValidationError("SES must be between 0 and 10.")
    #     if MMSE < 0 or MMSE > 30:
    #         raise serializers.ValidationError("MMSE must be between 0 and 30.")
    #     if eTIV < 0 or eTIV > 30:
    #         raise serializers.ValidationError("eTIV must be between 0 and 30.")
    #     if nWBV < 0 or nWBV > 30:
    #         raise serializers.ValidationError("nWBV must be between 0 and 30.")
    #     if ASF < 0 or ASF > 100:
    #         raise serializers.ValidationError("ASF must be between 0 and 100.")
    #     return data
    def predict(self):
        data = self.validated_data

        Age = data.get('Age')
        print(Age)
        Sex = int(data.get('Sex'))
        ChestPainType = float(data.get('ChestPainType'))
        Cholesterol = float(data.get('Cholesterol'))
        FastingBS = float(data.get('FastingBS'))
        MaxHR = float(data.get('MaxHR'))
        ExerciseAngina = float(data.get('ExerciseAngina'))
        Oldpeak = float(data.get('Oldpeak'))
        ST_Slope = float(data.get('ST_Slope'))

        all_data = [Age, Sex, ChestPainType, Cholesterol, FastingBS, MaxHR,
                    ExerciseAngina, Oldpeak, ST_Slope]
        loaded_model = joblib.load("ml_models/HeartAttack_model.pkl")
        result = loaded_model.predict([all_data])
        if int(result[0]) == 1:
            result = 'Have a heart attack'
        elif int(result[0]) == 0:
            result = "don't have a heart attack"

        return result


