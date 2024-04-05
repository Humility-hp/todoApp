from .models import Item
from rest_framework import serializers

# using a serializer to convert my data to the type i want
class ListSerializers(serializers.ModelSerializer):
 class Meta:
  model = Item
  fields = '__all__'
