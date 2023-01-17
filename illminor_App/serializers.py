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
    chestTest_model = serializers.SerializerMethodField()
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

    def get_chestTest_model(self,instance):
        user_id = instance.user
        try :
            query_set = chestTest.objects.get(user=user_id).result
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

        loaded_model = joblib.load(open("ml_models/bloodmodelRBF", 'rb'))
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

class chestTestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(), )
    patient_name = serializers.SerializerMethodField()
    class Meta :
        model = chestTest
        fields = '__all__'
    def get_patient_name(self,instance):
        return f"{instance.user.first_name} {instance.user.last_name}"

    # def predict(self):
    #     data = self.validated_data
    #
    #     chest_pic = data['chest_pic']
    #     chest_pic = os.path.join(os.getcwd()+f"/media/chest_image/{chest_pic}")
    #     modedl_path = r"ml_models/chestExploration.hdf5"
    #     model = keras.models.load_model(modedl_path)
    #     gray_image = cv2.imread(chest_pic, 0)
    #     resized_image = cv2.resize(gray_image, (100, 100))
    #     scaled_image = resized_image.astype("float32") / 255.0
    #     sample_batch = scaled_image.reshape(1, 100, 100, 1)  # 1 image, 100, 100 dim , 1 no of chanels
    #     result = model.predict(sample_batch)
    #     result[result >= 0.5] = 1  # Normal
    #     result[result < 0.5] = 0  # Pneimonia
    #     if result[0][0] == 1:
    #         result = "Normal"
    #     else:
    #         result = "Pneimonia"
    #     return result

