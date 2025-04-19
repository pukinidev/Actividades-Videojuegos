from src.engine.services.images_service import ImagesService
from src.engine.services.sound_service import SoundService

class ServiceLocator:
    images_service = ImagesService()
    sound_service = SoundService()
    
    