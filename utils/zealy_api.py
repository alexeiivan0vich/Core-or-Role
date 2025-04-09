import os
import aiohttp
from dotenv import load_dotenv

# Force reload environment variables
load_dotenv(override=True)

class ZealyAPI:
    def __init__(self):
        self.base_url = "https://api-v2.zealy.io/public"
        self.subdomain = "rollana"  # Zealy subdomain'iniz
        self.api_key = os.getenv('ZEALY_API_KEY')
        if not self.api_key:
            raise ValueError("ZEALY_API_KEY not found in .env file")
            
        self.headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        print(f"\nZealy API Başlatıldı:")
        print(f"API Key: {self.api_key[:5]}...{self.api_key[-5:]}")
        
    async def get_user_info(self, discord_id: str) -> dict:
        """Discord ID kullanarak kullanıcı bilgilerini getir"""
        url = f"{self.base_url}/communities/{self.subdomain}/users"
        params = {'discordId': discord_id}
        
        print(f"\nZealy API İsteği:")
        print(f"URL: {url}")
        print(f"Discord ID: {discord_id}")
        print(f"API Key: {self.api_key[:5]}...{self.api_key[-5:]}")  # API key'in sadece başı ve sonu
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as response:
                print(f"Status Code: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    print(f"Response: {data}")
                    return data
                else:
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    return None

    async def add_xp(self, user_id: str, amount: int, label: str = "Core or Roll", description: str = "Yazı-tura oyunu kazancı") -> bool:
        """Kullanıcıya XP ekle"""
        url = f"{self.base_url}/communities/{self.subdomain}/users/{user_id}/xp"
        payload = {
            "xp": amount,
            "label": label,
            "description": description
        }
        
        print(f"\nZealy API İsteği (POST - Add XP):")
        print(f"URL: {url}")
        print(f"User ID: {user_id}")
        print(f"Amount: {amount}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                print(f"Status Code: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    print(f"Response: {data}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    return False

    async def remove_xp(self, user_id: str, amount: int, label: str = "Core or Roll", description: str = "Yazı-tura oyunu kaybı") -> bool:
        """Kullanıcıdan XP sil"""
        url = f"{self.base_url}/communities/{self.subdomain}/users/{user_id}/xp"
        payload = {
            "xp": amount,
            "label": label,
            "description": description
        }
        
        print(f"\nZealy API İsteği (DELETE - Remove XP):")
        print(f"URL: {url}")
        print(f"User ID: {user_id}")
        print(f"Amount: {amount}")
        
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=self.headers, json=payload) as response:
                print(f"Status Code: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    print(f"Response: {data}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    return False
