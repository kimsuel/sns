from django.forms import model_to_dict
from django_elasticsearch_dsl import Index, Document, fields
from django_elasticsearch_dsl.registries import registry

from api.features.models import Post

post_index = Index('posts')


@post_index.document
@registry.register_document
class PostDocument(Document):
    user = fields.ObjectField(attr='get_user_data')
    text = fields.TextField(attr='text')

    class Index:
        name = 'posts'

    class Django:
        model = Post

    def get_user_data(self, instance):
        return model_to_dict(instance.user, fields=['id', 'username'])
