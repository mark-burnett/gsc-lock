from . import models
from rest_framework import serializers

import datetime


class TimeDeltaField(serializers.FloatField):
    default_error_messages = {
        'invalid': "'%s' could not be cast as a timedelta object",
    }

    def from_native(self, value):
        validated_value = serializers.FloatField.from_native(self, value)
        try:
            return datetime.timedelta(seconds=validated_value)
        except TypeError, ValueError:
            msg = self.error_messages['invalid'] % value
            raise serializers.ValidationError(msg)

    def to_native(self, value):
        return value.total_seconds()


class RequestSerializer(serializers.HyperlinkedModelSerializer):
    current_status = serializers.SerializerMethodField('get_current_status')
    timeout = TimeDeltaField()
    resource = serializers.PrimaryKeyRelatedField()

#    requester_data = serializers.DictWithMetadata()

    class Meta:
        model = models.Request
        fields = ('url', 'current_status', 'resource', #'requester_data',
                'timeout')

    def get_current_status(self, obj):
        return obj.statuses.latest('timestamp').get_type_display()

    def validate_timeout(self, attrs, source):
        if attrs[source].total_seconds() < 0:
            raise serializers.ValidationError('timeout cannot be negative')
        return attrs


class LockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lock
