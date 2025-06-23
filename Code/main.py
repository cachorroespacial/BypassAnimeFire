import aiohttp
import os
import asyncio
from time import sleep


YELLOW = '\033[33m'
BLUE = '\033[36m'
BLUE_ = '\033[94m'
RED = '\033[91m'
RED_ = '\033[31m'
WHITE = '\033[37m'
GREEN = '\033[92m'
PURPLE = '\033[49;35m'

class bypass:
    def __init__(self):
        pass
    
    """
    Here it generates the download URL, following the pattern of animefire URLs.

    """
    def generate_download_link(self, anime_name, episode_number, quality, server_index):
        base_url = f"https://lightspeedst.net/{server_index}/mp4/{anime_name}/{quality}/{episode_number}.mp4"
        download_link = base_url
        download_link += f"?type=video/mp4&title=[AnimeFire.plus]%20{anime_name.replace('-', ' ').title()}%20-%20Episódio%20{episode_number}%20({quality.upper()})"
        return download_link

    
    def generate_multiple_links(self, anime_name, episode_number):
        qualities = ["hd", "sd"]  
        server_indexes = [f"s{i}" for i in range(1, 11)]  
        links = {quality: [] for quality in qualities}  
        
        for server_index in server_indexes:
            for quality in qualities:
                
                link = self.generate_download_link(anime_name, episode_number, quality, server_index)
                links[quality].append(link)
        
        return links
    
    """
    In this part, it checks if the generated URL is valid, if so, it returns it.

    """
    async def check_link_validity(self, session, link):
        try:
            async with session.head(link) as response:
                
                if response.status == 200:
                    return link
        except Exception:
            return None
        return None

    
    async def find_download_links(self, anime_name, episode_number):
        links = self.generate_multiple_links(anime_name, episode_number)
        valid_links = {"hd": None, "sd": None}

        
        async with aiohttp.ClientSession() as session:
            
            for quality in ["hd", "sd"]:
                for link in links[quality]:
                    download_url = await self.check_link_validity(session, link)
                    if download_url:
                        valid_links[quality] = download_url
                        break  

        
        if valid_links["hd"] and valid_links["sd"]:
            print(f"{GREEN}[SUCCESS]{WHITE} Link found for {BLUE}{anime_name}{WHITE} - Episode {BLUE}{episode_number}{WHITE}:")
            print(f"{GREEN}HD:{PURPLE} {valid_links['hd']}{WHITE}")
            print(f"{GREEN}SD:{PURPLE} {valid_links['sd']}{WHITE}")
        elif valid_links["hd"]:
            print(f"{GREEN}[SUCCESS]{WHITE} Link found for {BLUE}{anime_name}{WHITE} - Episode {BLUE}{episode_number}{WHITE} (HD): {PURPLE}{valid_links['hd']}{WHITE}")
        elif valid_links["sd"]:
            print(f"{GREEN}[SUCCESS]{WHITE} Link found for {BLUE}{anime_name}{WHITE} - Episode {BLUE}{episode_number}{WHITE} (SD): {PURPLE}{valid_links['sd']}{WHITE}")
        else:
            print(f"{RED}[ERROR]{WHITE} No valid download link found for the episode.")


def main():

    def animation(text, delay=0.003):
        for char in text:
            print(char, end='', flush=True)
            sleep(delay)

    animation(f"""
{PURPLE}██████  ██    ██ ██████   █████  ███████ ███████   {WHITE}   █████  ███    ██ ██ ███    ███ ███████{BLUE} ███████ ██ ██████  ███████  
{PURPLE}██   ██  ██  ██  ██   ██ ██   ██ ██      ██        {WHITE}  ██   ██ ████   ██ ██ ████  ████ ██     {BLUE} ██      ██ ██   ██ ██      
{PURPLE}██████    ████   ██████  ███████ ███████ ███████   {WHITE}  ███████ ██ ██  ██ ██ ██ ████ ██ █████  {BLUE} █████   ██ ██████  █████   
{PURPLE}██   ██    ██    ██      ██   ██      ██      ██   {WHITE}  ██   ██ ██  ██ ██ ██ ██  ██  ██ ██     {BLUE} ██      ██ ██   ██ ██      
{PURPLE}██████     ██    ██      ██   ██ ███████ ███████   {WHITE}  ██   ██ ██   ████ ██ ██      ██ ███████{BLUE} ██      ██ ██   ██ ███████
{WHITE}_________________________________________________________________________________________________________________________

""", 0.003)
    
    anime_name = input(f"{WHITE}Enter the name of the anime: ").strip().lower().replace(" ", "-")
    episode_number = input(f"{WHITE}Enter episode number: ").strip()

    try:
        episode_number = int(episode_number)
    except ValueError:
        print(f"{RED}[ERROR]{WHITE} The episode number must be a numeric value. Please try again!")
        return

    downloader = bypass()
    asyncio.run(downloader.find_download_links(anime_name, episode_number))

if __name__ == "__main__":
    main()
