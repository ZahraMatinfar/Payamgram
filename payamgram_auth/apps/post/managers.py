from django.db.models.query import QuerySet


class PostManager(QuerySet):
    def update(self, *args, **kwargs):
        return super().update()
