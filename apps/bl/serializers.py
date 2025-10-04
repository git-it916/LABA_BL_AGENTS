from rest_framework import serializers

class RunBLSerializer(serializers.Serializer):
    as_of = serializers.DateField()
    benchmark = serializers.CharField()
    tau = serializers.FloatField(default=0.05)
    delta = serializers.FloatField(default=2.5)
