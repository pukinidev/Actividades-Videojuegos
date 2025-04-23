from src.engine.services.images_service import ImagesService
from src.engine.services.sound_service import SoundService
from src.engine.services.text_service import TextService

class ServiceLocator:
    images_service = ImagesService()
    sound_service = SoundService()
    text_service = TextService()
    
    