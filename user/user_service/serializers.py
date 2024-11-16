from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'phone_number', 'address', 'is_active','image']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            address=validated_data.get('address', ''),
            is_active=validated_data.get('is_active', True)
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        user = User.objects.filter(email=email).first()
        if user: 
            if user.check_password(password):
                return user
            else:
                raise serializers.ValidationError('Invalid password.')
        else:
            raise serializers.ValidationError('User does not exist.')


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'phone_number', 'address','password']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user

        # Kiểm tra mật khẩu cũ
        if not user.check_password(value):
            raise serializers.ValidationError('Incorrect old password.')

        return value

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        # Kiểm tra mật khẩu mới và xác nhận mật khẩu mới
        if new_password != confirm_new_password:
            raise serializers.ValidationError("New passwords do not match.")

        # Xác thực mật khẩu mới
        try:
            validate_password(new_password, self.context['request'].user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return data

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']

        # Cập nhật mật khẩu mới
        user.set_password(new_password)
        user.save()


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'address']

    def update(self, instance, validated_data):
        # Cập nhật các trường của đối tượng instance với dữ liệu đã xác thực
        instance.username = validated_data.get('username', instance.username)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        
        return instance
