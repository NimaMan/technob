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
        "youtube_link": "https://www.youtube.com/watch?v=oVfw8P0NOTA",
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
    },
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

amelie_lens = {"Tomorrowland Summer 2023":{
                "youtube_link": "https://www.youtube.com/watch?v=_Dy_Cn0HEZU", 
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
                "Exhale 78":{
                    'youtube_link': "", 
                    'info':'''
                        00.00 Irshad Hussein - Scorpion (Original Mix)
                        03.53 AIROD & Amelie Lens - Adrenaline
                        06.10 Adam Beyer - Desert Queen
                        09.48 Atheris - Kindergarten
                        12.44 Gabry Fasano - Chicago
                        15.45 Steve Shaden - Closure
                        18.59 Widerz - Space Machine
                        21.51 Charlie Sparks & Frazi.er - No Time For Hate
                        24.43 Analect - Precognition
                        28.13 Flour - Invasion
                        32.34 AIROD - Drumshock
                        33.30 Commander Sam - Are Am Psy
                        38.06 Sylvie Maziarz - Durch Die Nacht (MSKD Remix)
                        43.36 SWART - Trancender
                        49.03 La Kajofol - Ivresse
                        ''',
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


trym = {
    "Extrema 2022": {
        "youtube_link": "https://www.youtube.com/watch?v=ubVmJQG34BY",
        "info": '''
            0:00 Billy Gillies - Density
            2:50 Bitonal & MonoDynamic - Notaufnahme 2022 - N.O.B.A Remix
            5:16 Daniel Beknackt - Detection (N.O.B.A Remix)
            6:20 H! Dude - Olivette
            7:40 H! Dude - move your feet
            11:30 Aran Burn - Loco
            13:50 Dax J - Offending public morality
            15:40 Disguised - Frontal
            19:25 OGTS - Conjure Image
            24:16 Detatched From Reality - elMefti
            27:59 Tolouse - ANSBRO
            28:30 Scove - Kaltes Fieber
            32:43 Paul Denton - Stomp
            35:04 Scot Project - B3 (Believe In You)
            39:10 Mark Sherry-Total Eclipse (David Forbes Remix)
            41:05 David Forbes - Isolate (Extended Mix)
            43:30 La Bouche - Be My Lover (euro dance mix)
            44:30 Bollmann - Rampage
            49:45 MO-DO - Eins Zwei Polizei (remix ID?)
            51:42 NG Rezonance & Coulson (UK) - Resilience (Original Mix)
            57:40 Scot Project - H (Hypnotize)
            1:00:00 U96 - Club Bizarre 2k17 (UltraBooster Bootleg Remix)
            1:02:15 Around the World (MZPERX edit)
            ''',
        },
}


nine_nine = {
    "Awakenings 2022": {
    },

    "Apokalypse": {
        "youtube_link": "https://www.youtube.com/watch?v=GjdBEyLeclU",
        "info": '''
            0:35 TNT x DJ Isaac - Rave Now
            2:45 WZX_O & TECHSIA - Born To Rave
            5:47 Alex Farell - 3AM In Berlin
            12:23 Jacidorex & POPOF - Midnight Express
            16:01 SIKOTI - Make the Crowd Go
            18:50 Marco Leckbert - Sensitive Power
            21:31 HXIST - I'm So Afraid
            24:37 DJ Reiz - Dance Machine 96 (ID Edit)
            27:35 MSL-T - It's A Lifestyle
            30:17 PRYDIE - Transparency
            37:48 Luciid - Paro Hour
            42:26 Shadym - P.O.P.
            48:00 Fabrizio De Santis - Prometazina
            52:53 Fenrick - U Belong To Me
            56:09 Brennan Heart - I Love Haters
            58:38 MSL-T & ELECTRE - Hard Influences
            1:05:12 Djay D, Wain Johnstone - Edge Of Acid (ID Edit)
            1:08:07 JonJo Drake - Why People Take LSD
            1:11:15 Aaran Burn - Titan
            1:15:14 Luca Agnelli - Wait A Minute
            1:17:31 Rian Wood - Hard Generation
            1:20:58 RBX - Reverse Bass
            1:24:52 Jacidorex - Two Minded
            1:28:16 RBX - Smashes Heads
            1:32:07 Jacidorex - Titania
            1:34:04 TNT x Rudeejay - The Music Is Moving
            1:36:53 TNT & Ruffneck - Mindcontroller 2k20
            1:38:25 Wild Motherfuckers - Fuck It Up
            1:40:20 Wild Motherfuckers - Fuck It Up (ID Edit)
            1:42:55 TNT - Reverse The Bass
        ''',
        },
}


dax_j = {"Boiler Room 2022": {
    "youtube_link": "https://www.youtube.com/watch?v=2evgi1bbteA",

    "info": '''
    0:14 | Sera J - Freedom
    2:15 | Vince - Roll
    4:13 | Kashpitzky - Pursuit
    10:37 | VILLA - 6am Lovestory
    16:15 | Aaron Liberator & The Geezer - Reach For The Lazers
    21:52 | Ant & KN - Fast Lane
    23:06 | Pavel K. Novalis - Novitchok
    26:43 | Badah - Brutal Man
    30:35 | Dax J - The Train
    33:35 | Leftfield - Afroride
    39:50 | Decadence - Pass The Hoover
    42:42 | Guy McAffer - Smoke Out The Mole
    45:42 | Christopher Just - Petra 02 (Dax J Remix)
    52:11 | Siul - Acid Schizophrenia
    53:53 | Dax J - Brixton
    55:52 | ID.. Closed Awakenings with this one.
    59:00 | Infravision - Anthem
    '''    
    },

    "Arte Concert 2022": {
        "youtube_link": "https://www.youtube.com/watch?v=nbiaM9cGcJc",
        "info": '''
        0:00 | Hioll - Jerusalem Calling
        3:30 | Lucass P - Concours D’élégance
        4:30 | Ertax - Start From Hell
        7:30 | Benkhlifa - Perfekt Mistake
        10:15 | Nnamael - Ataraxia
        13:30 | Triple Drop - Keep Your World
        15:10 | DJ Cheses - Amargo
        17:05 | Dax J - China White (will be released on Monnom Black at August 19)
        21:10 | Umwelt - The Lost Dreamer
        24:20 | Lvgo - Vampire Complex
        27:00 | Acidless - Kiss Me
        30:00 | Juan Nuciforo - Hasta Las Manos
        32:00 | Aero - I Can’t Shoot
        35:30 | Dax J - Reshape The Future (will be released on Monnom Black at August 19)
        42:40 | Dax J - World Deception Alliance (will be released on Monnom Black at August 19)
        46:43 | Skryption - Get Ready
        49:10 | Sugar - Kværkhegn
        54:20 | Spokesman - Acid Creak (Pierre Reconstruction Mix)
        58:40 | Alt8 - Loop Da Loop (Chris Liberator & The Geezer Remix)
        1:01:15 | Vendex - Demon’s Souls
        1:08:40 | Dax J - Molotonic Beats
        1:11:14 | Big In Germany - G Is For Germany (Geezer’s “G Is For Geezer” Remix)
        1:14:50 | Valentino Kanzyani - House Soul
        1:17:48 | Dax J - The Train
        1:20:30 | NTBR & ÅMRTÜM - Im Paradis
        1:22:11 | Christopher Just - Petra 02 (Dax J Remix) (will be released on Monnom Black on the 30th of September)
        1:25:35 | Gat Decor - Passion (Naked Edit/Dax Edit)
        1:28:55 | Ryuji Takeuchi - West, Not East
        1:32:01 | Mauro Picotto - Baguette
        1:33:00 | Patrick DSP - Esh
        1:34:56 | Maxxi Rossi - Pulse Shaper
        1:37:05 | Dax J - Brixton (will be released on Monnom Black at August 19)
        1:41:15 | Hysteric Ego - Want Love (Remix)
        1:44:57 | Phrenetic System - Wayfarer
        1:48:40 | Sergy Casttle - Arpeggiator
        1:50:49 | Rocco & Heist - Paradise Rush (Tarrentella vs. Redank Mix)
        1:57:10 | Umwelt - Generation One
        2:01:45 | These Hidden Hands - SZ31X71 (Roly Porter Remix)
        '''
        },

    "Awakenings 2022": {
        "youtube_link": "https://www.youtube.com/watch?v=2evgi1bbteA",
        "info": '''
            1:34 | Cyborg X - Latino Expo
            3:00 | Masters of Disaster - No Headroom
            6:30 | Dax J - China White
            9:05 | Umwelt - Captive Universe
            11:20 | Nnamael - ATARAXIA
            14:12 | Andreas Kramer & Thomas Pogadl - Unsound
            16:19 | Thomas Krome - Bitches From Hell (Resurrection Edit)
            20:00 | Riino - What's matter
            22:00 | Umwelt - Generation One 
            26:10 | Ryuji Takeuchi - Dignity
            31:00 | Schall + Rauch - You See That Voice
            34:00 | Al-Faris & The Pagemaster - Fundamental
            37:00 | Sergy Castle - Come On Neng
            39:10 | Dax J - The Final Wavescape
            41:20 | BFVR - Birds Mansion (Umwelt Remix)
            44:20 | Track id unknown (maybe Ben Khlifa)
            46:50 | Aerial Mind - Riino
            50:10 | David Moleon - Cockroach rework - rework
            55:13 | Speedy J - Krekc
            56:30 | Dax J - Susumu remix (Unreleased)
            59:05 | Fractions - Hater Squad
            1:03:06 | Quartz - Calling
            1:05:00 | Ryuji Takeuchi - Nachtaktiv
            1:09:00 | Andreas Krämer & Thomas Pogadl - Lecker Mädche
            1:12:35 | Buzzi - Splash
            1:15:55 | Guy McAffer - Smoke Out The Mole
            1:18:25 | Umwelt - The Lost Dreamer
            1:21:55 | Dax J - Brixton
            1:27:00 | Frank Biazzi - Turbulence
            1:31:50 | Christopher Just - Petra 02 (Dax J Remix)
            1:34:55 | Primal - Truth Without Pain
            1:38:55 | Dax J - The Train
            1:40:40 | DJ Varsovie - Codeword Macumbar (Verset Zero Remix)
            1:43:00 | MK Ultra - Redline Hero
        '''
},
}


alignment = {
    "Verknipt 2023": {
        "youtube_link": "https://www.youtube.com/watch?v=grxklWG1Vfc",
        "info": '''
        0:05 Neika & Creeds - Run Away
        2:20 Eczodia - Devil's Motel
        4:54 Alignment - Close Your Eyes
        08:05 Storm - Different Power
        10:50 Alignment - The Sound
        15:55 Alignment - ID (Unreleased)
        19:33 Juul Exler - Illusion
        22:51 RBX - Fokkin Rave (unreleased)
        28:47 Kølab - Get Away
        29:37 Juul Exler - Detoxify
        31:57 Alignment - Malfunction (Unreleased)
        35:42 NYCO - Fucking Em Up
        39:22 Alignment - Attack
        43:10 Mr. Machine - In the Wood
        47:00 Renegade System - When I Rock
        49:55 Skryption - Hard Dreams
        53:00 CARV - Brembo
        56:25 STORM - Man Feel Alive
        59:33 Tiesto - Adagio For Strings (BYØRN Hard techno remix)
        1:02:25 CARV & DeGuzman - TempoPusher
        1:05:20 RAËL - Schmieren
        1:08:15 Protokseed - machine gun
        '''
    },
    "Verknipt Indoor 04-02-2023":{
        "youtube_link":"https://www.youtube.com/watch?v=x43ToCZzEm8&t=3766s",
        "info":
        '''
        0:00:00 STORM - Man Feel Alive
        0:03:54 SMAC-U - Trainwreck
        0:08:15 AnGy KoRe, Gabriel Padrevita, Simox - Smoke
        0:12:29 Basswell, 74185# - Fusion
        0:13:57 CARV, DeGuzman - TempoPusher
        0:17:19 Alignment - Close Your Eyes
        0:20:42 Alignment - Gravitation [Unreleased]
        0:24:01 Alignment - System Failure [Unreleased]
        0:28:23 PISAPIA (IT) - Hybrid Boom
        0:31:36 AnGy KoRe, Gabriel Padrevita - Turn Me On
        0:34:52 Luca Agnelli - Here We Go Again
        0:36:20 Alignment - Attack
        0:40:29 Alignment - Fight For A New World
        0:42:59 Mr.Machine - In The Wood
        0:47:44 O.B.I. - Get Em High
        0:50:21 Alignment - The Sound
        0:54:34 Viper Diva - Love & Riot
        0:59:01 Alignment - You Can't Control Me
        1:01:54 Scove, Veyla - Mayhem
        1:05:11 LÄUFF - Lightning (Funk Tribu Remix)
        1:09:45 1luu feat. Lauterkach - Beryllium
        ''',
    },
}


ceza = {'Ders al': "https://www.youtube.com/watch?v=rP2X839Bm9U", 
}


Adriatique = {
    "Printworks":{
        "youtube_link":"https://www.youtube.com/watch?v=GPuZwMmd4YI",
        },

    "Tomorrowland 2023":{
        "youtube_link": "https://www.youtube.com/watch?v=XkVC62yzxlg", 
        "info": '''
                24:00 ANOTR & Abel Balder - Relax My Eyes (Restricted Edit)
                31:30 Jos & Eli - ID
                36:50 Adriatique - The Future Is Unknown
                40:30 ID - ID
                46:40 Eynka & Adriatique - Beyond Us (Hatshepsut Version)
                52:00 Pryda - The Return
                58:00 ID ft. Braev - Feel
                1:03:00 The Irrepressibles - The Most Beautiful Boy (Felsmann + Tiley Reinterpretation) (Aaron Hibell Edit)
                1:07:00 RÜFÜS DU SOL - On My Knees (Adriatique Remix)
                1:14:00 Ae:ther & Benjamin Yellowitz - Dynamite 
                1:20:30 ID - ID
                1:25:00 Adriatique & WhoMadeWho - Miracle
            ''',
        },

    }