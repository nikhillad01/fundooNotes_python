from django_elasticsearch_dsl import DocType,Index
from .models import Notes
notes = Index('notes')
@notes.doc_type
class NotesDocument(DocType):
    class Meta:
        model=Notes
        fields=['title',
                'description','created_time']