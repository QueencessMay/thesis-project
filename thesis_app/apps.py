from django.apps import AppConfig
from transformers import DistilBertTokenizerFast, TFDistilBertForSequenceClassification

class ThesisAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'thesis_app'

    def ready(self):
        path_without = 'FiouReia/distilbert_uncased_trained_with_game_reviews'
        self.model_without = TFDistilBertForSequenceClassification.from_pretrained(path_without)
        path_with = 'FiouReia/distilbert_uncased_trained_with_game_reviews_emojis_emoticons'
        self.model_with = TFDistilBertForSequenceClassification.from_pretrained(path_with)
        self.tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
