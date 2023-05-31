from rest_framework import serializers

from apps.data_source.integrations.constants import SourceSearchTypeEnum


class InputSearchBookSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_null=True)
    external_id = serializers.CharField(required=False, allow_null=True)
    subtitle = serializers.CharField(required=False, allow_null=True)
    editor = serializers.CharField(required=False, allow_null=True)
    category = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)
    publication_date = serializers.CharField(required=False, allow_null=True)
    author = serializers.CharField(required=False, allow_null=True)


class InputCreateBookSerializer(serializers.Serializer):
    book_id = serializers.CharField(required=True)
    source = serializers.ChoiceField(
        choices=[
            SourceSearchTypeEnum.GOOGLE_SEARCH.value,
            SourceSearchTypeEnum.OPEN_LIBRARY_SEARCH.value
        ]
    )
