from django.db.models.signals import post_migrate
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(post_migrate)
def run_post_migrate_setup(sender, **kwargs):
    # Import the functions here to avoid circular imports
    from .views import silent_nltk_download, profanity
    logger.info("Running post-migrate setup: NLTK downloads and loading profanity words...")
    silent_nltk_download('punkt')
    silent_nltk_download('stopwords')
    try:
        profanity.load_censor_words()
        logger.info("Successfully loaded profanity censor words.")
    except Exception as e:
        logger.error(f"Error loading profanity censor words: {e}")
