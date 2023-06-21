from asgiref.sync import sync_to_async

from django.db import models
from django.db.models import Q


class BaseModel(models.Model):
    class Meta:
        abstract = True

    create_date = models.DateTimeField(null=True, auto_now_add=True)
    last_update = models.DateTimeField(null=True, auto_now=True)

    @classmethod
    @sync_to_async
    def update_by_id(cls, id, data):
        rec = cls.objects.filter(id=id)
        rec.update(**data)
        return cls.objects.get(id=id)

    @classmethod
    @sync_to_async
    def create_record(cls, data):
        rec = cls.objects.create(**data)
        return rec


class Topic(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    @classmethod
    @sync_to_async
    def find_by_name(cls, name):
        return cls.objects.get(name=name)

    @classmethod
    @sync_to_async
    def all_topics(cls):
        records = cls.objects.values_list('name')
        if records:
            return [i[0] for i in records]
        return None

    def __str__(self):
        return self.name


class Question(BaseModel):
    name = models.CharField(max_length=255)
    topic = models.ForeignKey(
        Topic,
        related_name='questions',
        on_delete=models.CASCADE
    )

    @classmethod
    @sync_to_async
    def find_by_name(cls, name):
        return cls.objects.select_related('topic').get(name=name)

    @classmethod
    @sync_to_async
    def filter_by_name(cls, name):
        records = cls.objects.select_related('topic').filter(name__icontains=name).order_by('name')

        if records:
            return list(records)
        return None

    @classmethod
    @sync_to_async
    def find_by_topic(cls, topic):
        records = cls.objects.select_related('topic').filter(
            topic__name__icontains=topic
        ).order_by('name')

        if records:
            return list(records)
        return None

    def __str__(self):
        return f'{self.topic.name} - {self.name}'


class Answer(BaseModel):
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )
    name = models.TextField()
    is_correct = models.BooleanField(default=False)

    @classmethod
    @sync_to_async
    def find_by_question(cls, question):
        records = cls.objects.select_related('question').filter(
            question__name__icontains=question
        ).order_by('is_correct').values_list('name', 'is_correct')

        if records:
            return list(records)
        return None

    def __str__(self):
        return f'{self.question.name} - {self.name} - {self.is_correct}'
