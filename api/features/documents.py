from django_elasticsearch_dsl import Index, Document, fields
from django_elasticsearch_dsl.registries import registry

from api.features.models import Post

post_index = Index('posts')


@post_index.document
@registry.register_document
class PostDocument(Document):
    user = fields.TextField(attr='user')
    text = fields.TextField(attr='text')

    class Index:
        name = 'posts'

    class Django:
        model = Post
