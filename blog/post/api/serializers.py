from rest_framework import serializers

from post.models import Post


# class PostSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=200)
#     content = serializers.CharField(max_length=200)


class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='post:detail',
        lookup_field='slug'
    )

    # username = serializers.SerializerMethodField(method_name='username_new')

    username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "user",
            "title",
            "content",
            "image",
            "url",
            "created_date",
            "modified_by",
            "username"
        ]

    def get_username(self, obj):
        return str(obj.user.username)

    # def username_new(self, obj):
    #     return str(obj.user.username)


class PostUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
        ]

    # def save(self, **kwargs):
    #     print("save")
    #     return True
    #
    # def create(self, validated_data):
    #     print("create")
    #     print(validated_data["title"])
    #     del validated_data['user']
    #     ## x kişiye mail atma işleme
    #     ## bir hesaptan para çekme işlemi
    #     ## sistemdeki bir taskın tetiklemesi sağlanalabilir
    #     return Post.objects.create(user=self.context["request"].user, **validated_data)
    #
    # def update(self, instance, validated_data):
    #     print("update çalıştı..")
    #     ## x kişiye mail atma işleme
    #     ## bir hesaptan para çekme işlemi
    #     ## sistemdeki bir taskın tetiklemesi sağlanalabilir
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.save()
    #
    #     return instance
    #
    # def validate_title(self, value):
    #     if value == "selcuk":
    #         raise serializers.ValidationError("bu değer girilemez")
    #     return value
    #
    # def validate(self, attrs):
    #     if attrs["title"] == "hulya":
    #         raise serializers.ValidationError("olmazzz")
    #     return attrs
