from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
import joblib



class USERSSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    class Meta :
        model = USERS
        fields = '__all__'
    def get_user(self, instance):
        return instance.user.username
    def get_user_id(self, instance):
        return instance.user.id
    def get_email(self, instance):
        return instance.user.email


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

        loaded_model = joblib.load(open("ml_models/bloodmodelRBF", 'rb'))
        clf = loaded_model.predict([all_data])
        result = None
        if clf[0] == 0:
            result = "No Cancer"
        elif clf[0] == 1:
            result = "Cancer"

        # self.instance.result = result

        return result





class bloodTestSerializer(serializers.ModelSerializer):
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
        age = data.get('age')
        pregnancies = data.get('pregnancies')
        glucose = data.get('glucose')
        bloodpressure = data.get('bloodpressure')
        skinthickness = data.get('skinthickness')
        insulin = data.get('insulin')
        bmi = data.get('bmi')
        dpf = data.get('dpf')

        if age < 0 or age > 100:
            raise serializers.ValidationError("Age must be between 0 and 100.")
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

        return data
    def predict(self):
        data = self.validated_data
        age = data.get('age')
        pregnancies = data.get('pregnancies')
        glucose = data.get('glucose')
        bloodpressure = data.get('bloodpressure')
        skinthickness = data.get('skinthickness')
        insulin = data.get('insulin')
        bmi = data.get('bmi')
        dpf = data.get('dpf')
        all_data = [age, bmi, pregnancies, glucose, bloodpressure, skinthickness, insulin,dpf,]

        loaded_model = joblib.load(open("ml_models/bloodmodelRBF", 'rb'))
        clf = loaded_model.predict([all_data])
        result = None
        if clf[0] == 0:
            result = "No Cancer"
        elif clf[0] == 1:
            result = "Cancer"

        # self.instance.result = result

        return result




