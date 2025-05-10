from django.db import models

class Flashcard(models.Model):
    word = models.CharField(max_length=100)
    phonetic = models.CharField(max_length=100)
    definition = models.TextField()
    example_sentence = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word
