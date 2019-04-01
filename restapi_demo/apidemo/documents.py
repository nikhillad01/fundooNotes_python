from django_elasticsearch_dsl import DocType,Index
from .models import Notes
notes = Index('notes')
@notes.doc_type
class NotesDocument(DocType):
    class Meta:
        model=Notes
        fields=['id','title',
                'description','created_time','reminder','is_archived','for_color','trash','is_pinned']