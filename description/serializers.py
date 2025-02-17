from rest_framework import serializers

class GenerateDescriptionSerializer(serializers.Serializer):
    sku_id = serializers.CharField()
    tone = serializers.ChoiceField(choices=[
        ('продающий', 'продающий'),
        ('формальный', 'формальный'),
        ('дружелюбный', 'дружелюбный')
    ])
    language = serializers.CharField(default='ru')
    exclude_keywords = serializers.ListField(
        child=serializers.CharField(), required=False, default=[]
    )
    include_keywords = serializers.ListField(
        child=serializers.CharField(), required=False, default=[]
    )

