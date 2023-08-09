import random
import string
import time
from .models import UserProfile


def generate_random_invite_code():
    
    """Генерируем код из шести букв и цифр"""
        
    characters = string.ascii_letters + string.digits
    code_length = 6
    while True:
        invite_code = ''.join(random.choice(characters) for _ in range(code_length))
        if not UserProfile.objects.filter(referral_code=invite_code).exists():
            return invite_code
        
def send_code(self):
        
        """
        Здесь могла бы быть логика отправки кода, 
        например, через Twillio или похожий сервис, 
        но в ТЗ написано - имитировать, поэтому просто 
        возвращаем наш ненастоящий код
        """
        
        time.sleep(5)
        
        return '1234aa'