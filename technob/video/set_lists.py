from dataclasses import dataclass, field
from typing import List

@dataclass
class SonginSet:
    order: int
    start_time_seconds: int
    artist: str
    song_name: str
    search_name: str


class Tracklist:
    youtube_link: str
    songs: List[SonginSet] = field(default_factory=list)
    
    def __init__(self, data):
        self.youtube_link = data["youtube_link"]
        self.songs = self.get_songs_info(data["info"])

    @staticmethod
    def get_songs_info(info):
        info_lines = info.strip().split("\n")
        songs = []
        
        for order, line in enumerate(info_lines, 1):
            cleaned_line = line.strip()
            parts = cleaned_line.split(" ", 1)
            start_time_range = parts[0]
            song_name_with_end = parts[1] if len(parts) > 1 else ""
            
            # Extracting artist and song name
            if " - " in song_name_with_end:
                artist, song_name = song_name_with_end.split(" - ", 1)
            else:
                artist = ""
                song_name = song_name_with_end

            artist = artist.strip()
            song_name = song_name.strip()
            
            start_time_parts = start_time_range.split(':')
            
            # Convert start time to seconds
            if len(start_time_parts) == 3:  # hours:minutes:seconds
                hours, minutes, seconds = start_time_parts
                total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
            else:  # minutes:seconds
                minutes, seconds = start_time_parts
                total_seconds = int(minutes) * 60 + int(seconds)
            
            # Concatenating artist and song name for the search_name
            search_name = f"{artist} {song_name}" if artist else song_name
            
            song_details = SonginSet(order=order, start_time_seconds=total_seconds, artist=artist, song_name=song_name, search_name=search_name)
            songs.append(song_details)
        
        return songs
        

kobosil = {
    "Time Warp 2023":
    { "youtube_link": "https://www.youtube.com/watch?v=Z3Z4X6Z3Z4Y",
    "info": '''
    0:00:45 No Neim Lost In The Dark
    0:02:14 Svetec, Sikztah - Phoenix (Original Mix)
    0:05:12 Forbidden Out of Order
    0:07:23 SuturaThe Reaper (O.B.I Remix)
    0:09:30 bastet - Disaster Rave
    0:32:00 Minor Dott - OUTSTANDING (unreleased)
    0:41:20 Geck-o - Go Higher Go Faster (Original Mix)
    0:47:14 Vizionn - Control (Original Mix)
    0:57:30 Bastet - Witching Hill (Original Mix)
    1:04:26 Matthew & Arkus - P.Life in Cube
    1:13:18 Nobody - Eat Shit and Schranz (Revisit)
    1:21:39 PETDuo - Hyped Demons (Andreas Kraemer RMX)
    1:24:22 Crime, Gyko Killa - Killa
    1:26:07 Ben Techy - On The Dance Floor
    1:29:21 Luciid - Vault
    1:36:00 Dambro - Rage on the Dancefloor
    1:40:10 Wiccuwa - Dark Tide (Original Mix)
    1:42:06 Luckes - Manera (Original Mix)
    1:46:00 O.B.I - Wir sind die nacht (unreleased)
    1:52:42 In Verruf - (Unreleased)
    ''',
    "other_links":{"https://www.youtube.com/watch?v=EYb_zhgd70U": "svetec - indifference ",
                    "https://www.youtube.com/watch?v=0sDNJ-UzwSE": "Petersardi - smile on the face", 
                    "https://www.youtube.com/watch?v=u4CAW92_4AU": "Vizionn - Control (Original Mix)", 
                    "https://www.youtube.com/watch?v=42yhUyqsFdE": "Farrago - Hardship",
                },

        }
    }


reinier = {
    "Time Warp 2023": {
        "youtube_link": None,
        "info": '''
        00:00 Lucid - Zerstörer
        00:36 Reinier Zonneveld - Move your body to the beat
        01:32 Creeds - Push Up (Tino Boa Rmx)
        15:30 Mha Iri - Bam Bam Bam
        30:20 AVB - Serenity remix
        31:40 Armin van Buuren - Serenity (remix)
        36:00 Reinier Zonneveld - CSE
        40:45 Reinier Zonneveld & Sjaak - ID
        47:00 Noneoftheabove & AERT - Pussy Peak
        52:00 unknown - interstellar theme remix
        01:00:44 Joe Goddard - Music Is The Answer (Reinier Zonneveld Remix)
        01:05:22 Reinier Zonneveld & D-Devils - Dance w/ the devil (The 6th gate) [Reinier Zonneveld remix]
        01:09:00 The Romantics - Talking in your sleep (RZ remix)
        01:17:00 Benni Benassi - Satisfaction
        01:26:30 Reinier Zonneveld & Kiki Solvej - Keine liebe, keine rave
        01:31:00 DJ Promo - My underground madness
        01:33:03 Age of Love - Age of Love [some RMX or sped up version]
        01:36:00 Reinier Zonneveld & Angerfist - Fist on Acid
        01:41:00 Miro - Shining (Reinier Zonneveld RMX)
        01:47:47 Reinier Zonneveld - Rave dan
        01:50:40 Reinier Zonneveld - Old school
        01:54:47 RZ - Hard Gaan
        01:54:47 Dustin Zahn - Stranger to stability(Len Faki RMX) [sped up and altered version]
        '''
    }
}


amber_roos_Tomorrowland = {"Tomorrowland Summer 2023":{ "youtube_link": "https://www.youtube.com/watch?v=GzkugkDQPoM", 
                                    "info":
                                        '''
                                        ''',
                                    },
                }

indira_paganotto_Tomorrowland = {"Tomorrowland Summer 2023":{ "youtube_link":"https://www.youtube.com/watch?v=BapBHKMYk0E&t=397s", 
                                        "info":
                                            '''
                                            ''',
                                        }

                        }

amelie_lens = {"Tomorrowland Summer 2023":{"youtube_link": "https://www.youtube.com/watch?v=_Dy_Cn0HEZU", 
                                 "info":'''
                                    3:14 Steve Shaden Florida
                                    8:20 Amelie Lens - Radiance
                                    10:35 Luix Spectrum & Loco13 - Blessing (Pitch! Remix)
                                    13:30 Decky Scott - Evil Intent
                                    17:15 Danielle Ciuro Bring It Back
                                    18:45 Robert Curtis - The Butterfly Effect 
                                    21:30 Portex - Addiction
                                    22:40 Sopik - Free Your Mind
                                    25:00 OnTune & Indecent Noise - Transmission Control
                                    27:15 Frankyeffe - Touch Me
                                    31:00 Basswell - Massive Attack
                                    34:20 Cherry Moon Trax - The House Of House (Thomas Schumacher Remix)
                                    37:30 CARV - Masked Rules
                                    41:05 Members Of Mayday - The Mayday Anthem (Thomas Schumacher Remix)
                                    45:20 Amelie Lens - Feel It
                                    48:20 Le Shuuk & B-Stylezz - Konje
                                    50:50 Aamourocean - This Is The Way (unreleased)
                                    53:35 Zombie Nation - Kernkraft 400 (ID Remix)
                                    55:40 Bastet - Fuck Style
                                    56:50 Amelie Lens - You And Me
                                    '''
                                },

               "Tomorrowland Winter 2023":{"youtube_link":"https://www.youtube.com/watch?v=vuBhxwCCbyw", 
                                 "info":
                                    '''
                                    '''
                                 },
                                 
               }


tale_of_us = {"Tomorrowland 2023":{
    "youtube_link": "https://www.youtube.com/watch?v=RcZU-a5WrRg",
    "info":'''
            00:00 Anyma & Chris Avantgarde - Simulation
            3:09 MRAK & David Lindmer - Their Law
            6:41 Argy & Anyma ft. Magnus - Higher Power
            10:21 Kevin de Vries & Mau P  - Metro
            15:10 Anyma & Rebūke - Syren
            18:51 MRAK - We Don't Follow
            22:16 Lana Del Rey - Say Yes To Heaven (Anyma Remix)
            26:09 MRAK - ID
            29:15 Massano - ID
            34:09 Chris Avantgarde - Perception
            39:00 Anyma ft. Sevdaliza - Samsara
            44:00 Depeche Mode - Ghosts Again (Massano Remix)
            48:51 Pryda - The Return
            53:55 Argy & Omnya - Aria
            57:30 ATB - 9PM (Till I Come)
        '''
} }
 

charlotte_de_witte = {
    "Ultra 2023":{
        "youtube_link": "https://www.youtube.com/watch?v=IDp8e3rDaQA",
        "info":'''
            0:07 Erso - Send the Signal (Intro Mix) [PROSPECT]
            2:00 Charlotte de Witte - High Street [KNTXT]
            7:00 Alignment - Nothingness [KNTXT]
            10:10 Charlotte de Witte - ID
            15:00 Push vs. Rebel Boy - Blue Shadow [BONZAI CLASSICS]
            19:15 Charlotte de Witte & Enrico Sangiuliano - Reflection [NINETOZERO]
            24:00 Jens Lissat & Bonzai All Stars - Imagination [BONZAI CLASSICS]
            28:00 Age Of Love - The Age Of Love (Charlotte de Witte & Enrico Sangiuliano Remix) [DIKI]
            33:00 Charlotte de Witte - Overdrive [KNTXT]
            38:00 DJ Jordan - Elements Of Joy [KMSELECTION]
            41:30 Alignment - Deep Space [KNTXT]
            44:40 The Rocketman & VE/RA - Love & Peace [3RD DALE UNIVERSE]
            49:35 Creeds - Push Up [RAVE ALERT]
            52:40 Vintage Culture - Bros (ID Remix) [SPINNIN']
            58:00 DJ Jordan - Positive Vibes (N.O.B.A Remix) [ITHICA RECORDS]
            '''
        },
 }



deWitte_urls = ["https://www.youtube.com/watch?v=1-ZU3bCEGqQ"
        "https://www.youtube.com/watch?v=GTYxbtDZBkU", 
        "https://www.youtube.com/watch?v=uxNjgtFTkLE",
        "https://www.youtube.com/watch?v=1-ZU3bCEGqQ",        
        ]

reiner_urls = ["https://www.youtube.com/watch?v=ovUWIjDBRTc", 
               "https://www.youtube.com/watch?v=uoPY8E16l-M",
               "https://www.youtube.com/watch?v=2evgi1bbteA",
               "https://www.youtube.com/watch?v=aSJi-SLaxLY",
               "https://www.youtube.com/watch?v=l2nn7nROf9I",
               "https://www.youtube.com/watch?v=bdFbYI0DS6Q",
               "https://www.youtube.com/watch?v=fwDwDp6001Y",
               "https://www.youtube.com/watch?v=ueDAul3ohhY",
               "https://www.youtube.com/watch?v=oSBUD45A-Gw",
               "https://www.youtube.com/watch?v=xU3Ipr1ntzw",
               "https://www.youtube.com/watch?v=xSJEwuhkQIk",
               "https://www.youtube.com/watch?v=DerCBfz5GQ0",
               "https://www.youtube.com/watch?v=1NuMjbkyCcA",
               "https://www.youtube.com/watch?v=NGnNZtBV1N8",
               "https://www.youtube.com/watch?v=80DR8XH-k-k",
               "https://www.youtube.com/watch?v=bWKUhgpVG1o",
               ]

             
ceza_urls = ["https://www.youtube.com/watch?v=rP2X839Bm9U", 
]


misc_urls = {"put the name": "https://www.youtube.com/watch?v=ND3KvTOkXbw", 
             "its_better_when_we_fake_it": "https://www.youtube.com/watch?v=ETm-GvXbh30",
             "oguz_golden_szn": 'https://www.youtube.com/watch?v=AfjoYWA1lOs', 
             "klungkluster_die_welt": "https://www.youtube.com/watch?v=8dercZbT3Tw",
             }

