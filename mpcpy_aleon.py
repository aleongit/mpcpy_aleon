# -*- coding: utf-8 -*-

#Aleix Leon

#imports ______________________________________________
import os
from datetime import date
import pickle
import re
import time

import eyed3
from eyed3 import id3
from eyed3 import load

#eyeD3 is a Python tool for working with audio files, specifically MP3 files containing ID3 metadata 
#https://stackoverflow.com/questions/8948/accessing-mp3-metadata-with-python
#https://eyed3.readthedocs.io/en/latest/

#https://www.codestudyblog.com/cnb2001/0123194106.html
#os.system： gets the return value of the program execution command.
#os.popen： gets the output of the program execution command.
#commands： gets the return value and the output of the command.
#os.system('comanda')

#result = os.popen('cat /etc/passwd')
#print(result.read())

#mpd
#music_directory		"/home/aleon/Music"
#playlist_directory		"/var/lib/mpd/playlists"

#mpc
#mpc load file.m3u      *carregar fitxer playlist
#mpc playlist           *llista cançons playlist
#mpc lsplaylist         *llista de playlists
#mpc status
#mpc volume 30
#mpc play [position]
#mpc seek [%]
#mpc random

#constants ______________________________________________
AUTOR = "Aleon"
DIR_MUSIC = '/home/aleon/Music'
DIR_PLAYLIST = '/home/aleon/playlists'
FILE_INFO = 'info.txt'
FILE_ALBUMS = 'albums'
FILE_ESTAT = 'estat_reproductor.txt'
FILE_LLISTES = 'playlists.txt'
FILE_LLISTA = 'playlist.txt'
INFO_TXT = ['Gènere', 'Any', 'Autor']
INFO_DEF = ['Desconegut\n', str(date.today().year)+'\n', 'Desconegut\n']
VOLUM = 30

MENU = {'INTRO':'  Play/Pause',
        '>':'         Següent',
        '<':'        Anterior',
        '+[N]':'      + Volum',
        '-[N]':'      - Volum',
        'r':'   Random on/off',
        'A':'          Àlbums',
        'L':'   Load Playlist',
        'C':'  Crear Playlist',
        'R':'           Reset',
        '0':'          Sortir'}

MENU_PLAYLIST = {'1':'Gènere',
                '2':'Autor',
                '3':'Anys',
                '4':'Reproduccions',
                '5':'Paraula',
                '6':'Àlbum',
                '0':'<<'}

MENU_EDITA = {
    'E':'Editar àlbum',
    'I':'Info MP3',
    '-':'Eliminar cançons',
    '+':'Afegir cançons eliminades',
    '0':'<<'
    }

#classes objecte ______________________________________________
#classe àlbum
class Album(object):
    #constructor per defecte
    def __init__(self):
        self.ruta = 'PATH'
        self.mp3 = [] #llista cançons àlbum
        self.genere ='GEN'
        self.any = 'ANY'
        self.autor = 'AUTOR'
        self.reproduccions = 0
        self.borrades = []
    #print objecte
    def __str__(self):
        return "\nGènere: %s\n\
Any: %s\n\
Autor: %s\n\
Reproduccions: %s\n\
Ruta: %s\n\
Cançons: %s\n\
Borrades: %s\n" %(self.genere, self.any, 
                self.autor, self.reproduccions, self.ruta, len(self.mp3), self.borrades)
    #genera llista per fitxer m3u
    #EXTM3U
    #/home/aleon/Music/Pirat's Sound Sistema/Pirat's Sound Sistema - Em Bull La Sang/12 - Ploren D'n'Bass.mp3
    #/home/aleon/Music/Pirat's Sound Sistema/Pirat's Sound Sistema - Sants Sistema/11 - A Cada Somni.mp3
    #/home/aleon/Music/41 - Amanda Blank - Make It, Take It.mp3
    def genera_m3u(self):
        """
        ll = []
        for mp3 in self.mp3:
            ll.append(self.ruta + '/' + mp3)
        return ll
        """
        return [ self.ruta + '/' + mp3 + '\n' for mp3 in self.mp3 ]

    def genera_m3u_cerca(self, cerca):
        return [ self.ruta + '/' + mp3 + '\n' for mp3 in self.mp3 if cerca.lower() in mp3.lower()  ]
    
    def update_cops(self, mp3):
        #print( mp3 in self.mp3)
        if mp3 in self.mp3:
            self.reproduccions += 1
    
    def update_info(self, ll):
        self.genere = ll[0]
        self.any = ll[1]
        self.autor = ll[2]

    def borra_mp3(self,pos):
        self.borrades.append(self.mp3.pop(pos))

    def recupera_mp3(self,pos):
        self.mp3.append(self.borrades.pop(pos))

#funcions ______________________________________________
def existeix_fitxer(fitxer):
    try:
        with open(fitxer, "r", encoding="utf8") as f:
            ok = True
    except IOError:
        ok = False
    return ok

def print_fitxer(fitxer):
    print("\n*FITXER TXT*")
    with open(fitxer, "r", encoding="utf8") as f:
        print(f.read())

#obrim fitxer w, afegim i tanquem
def guarda_fitxer(fitxer,ll):    
    with open(fitxer, "w", encoding="utf8") as f:
        f.writelines(ll) 

def llegeix_fitxer(fitxer):
    with open(fitxer, "r", encoding="utf8") as f:
        #la capçalera no l'agafo
        ll = f.readlines()
    return ll

def print_albums(dic):
    for k,v in dic.items():
        #print("%s -> %s" %(k,v))
        print(k)
        print(v)
    print()

def conta_fitxers(base, ext):
    #ls *.mp3 2> /dev/null | wc -l
    #entre "" nom fitxer
    bash = 'ls "' + base + '"/*.' + ext +' 2> /dev/null | wc -l'
    #print(type(mp3)) #int

    #n = os.system(bash)
    #amb os.system no es pot capturar la sortida de la comanda
    #os.popen si
    resultat = os.popen(bash).read()
    return int(resultat)

def crea_album(base,files,ll):
        #crea objecte àlbum
        album = Album() #nou objecte àlbum

        #atributs album
        album.ruta = base

        #filtro només mp3
        #print(files[0][-3:])
        mp3 = [el for el in files if el[-3:] == 'mp3']
        #print(mp3)
        #print('fitxers mp3',len(mp3))

        album.mp3 = mp3
        #trec últim caràcter \n
        album.genere = ll[0][:-1]
        album.any = ll[1][:-1]
        album.autor = ll[2][:-1]

        return album

def guarda_pickle(fitxer, albums):
    #print('guarda_pickle ', albums)
    outfile = open(fitxer,'wb')
    pickle.dump(albums, outfile)
    outfile.close()

def load_estat(fitxer):
    #llegir fitxer estat_reproductor.txt
    #fitxer estat ?
    #print( existeix_fitxer(fitxer) )
    
    #si hi és, carrega estat
    if existeix_fitxer(fitxer):
        estat = llegeix_fitxer(fitxer)
        #print(estat)

        #si només 1 línia, estat buit
        if len(estat) > 1:

            #canço estat / línia 1 fitxer
            playing = estat[1]
            ini = playing.find('#') + len('#')
            fi = playing.find('/')
            track = playing[ini:fi]
            #print(track)

            #posició %
            playing = estat[1]
            ini = playing.find('(') + len('(')
            fi = playing.find('%')
            pos = playing[ini:fi+1]
            #print(pos)

            #volum 30

            #mpc play 1 | mpc seek 5% | mpc volum 30
            bash = 'mpc play %s | mpc seek %s | mpc volum %s' %(track, pos, VOLUM)
            os.system(bash)

def print_menu():
    #mètode print(" %s " %(variable))
    print()
    for k,v in MENU.items():
        print("%s  %s" %(k,v))
    print()

def llegeix_playlists():
    fitxer = FILE_LLISTES
    #mpc a fitxer
    os.system('mpc lsplaylist > ' + fitxer)   #mpc lsplaylist / llista de playlists
    #de fitxer a ll, treure \n
    ll = [el[:-1] for el in llegeix_fitxer(fitxer)]
    return ll

#llegir nom llista en curs guardada a fitxer estat_reproductor.txt
def llegeix_playlist():
    ll = []
    fitxer = FILE_LLISTA
    if existeix_fitxer(fitxer):
        ll = llegeix_fitxer(fitxer)[0][:-1]
    return ll

def print_info(albums):
    print(f"\nWINAMP v2021 by {AUTOR}")
    #print(f"Fitxer impo/expo  : {FITXER}")
    print(f"Àlbums: {len(albums)}")
    #mpc playlist                       *llista cançons playlist
    #os.system('mpc lsplaylist')         #mpc lsplaylist / llista de playlists
    print(f"Playlists: {llegeix_playlists()}")
    print(f"Playlist actual: {llegeix_playlist()}")
    os.system('mpc status')             #mpc status

def menu_playlist():
    #mètode print(" %s " %(variable))
    print(f"\nCrear llista Reproducció\n------------------------")
    for k,v in MENU_PLAYLIST.items():
        print("%s -> %s" %(k,v))
    print()

def menu_edita():
    #mètode print(" %s " %(variable))
    print(f"\nEditar Àlbum\n------------------------")
    for k,v in MENU_EDITA.items():
        print("%s -> %s" %(k,v))
    print()

#genera un menú donada una llista
def genera_menu(ll):

    if len(ll) > 0:
        print()
        for i in range(len(ll)):
            print("%s -> %s" %(i+1,ll[i]))
        print()
    else:
        print('\n* LLISTA BUIDA *\n')

def llegeix_generes(albums):
    return list(set([ v.genere for k,v in albums.items() ]))

def llegeix_autors(albums):
    return list(set([ v.autor for k,v in albums.items() ]))

def llegeix_anys(albums):
    return list(set([ v.any for k,v in albums.items() ]))

def llegeix_cops(albums):
    return list(set([ v.reproduccions for k,v in albums.items() ]))

def llegeix_noms_albums(albums):
    return [ k for k in albums ]

def reproduccions_album():
    
    #mpc current -f %file% --> nom fitxer mp3
    bash = f'mpc current -f %file%'
    mp3_actual = os.popen(bash).read()
    
    #depurar song obtinguda
    #Creedence Clearwater Revival/The Best Of _ CD 2/17 Molina.mp3
    #buscar últim /
    #rfind() retorna pos últim, sinó el troba -1
    pos =  mp3_actual.rfind('/') + 1
    #print(pos)
    mp3_actual = mp3_actual[pos:-1]
    
    #per a cada objecte àlbum, mira si cançó actual en cançons àlbum
    for k,v in albums.items():
        v.update_cops(mp3_actual)

def valida_anys(cad, anys):
    ok = False
    a1 = cad[0:4]
    a2 = cad[5:]
    #print(a1,a2)

    #len 4
    if len(a1)==4 and len(a2)==4:
        #digits
        try:
            a1 = int(a1)
            a2 = int(a2)
            #dins llista anys
            ll = [ any for any in anys if int(any) >= a1 and int(any) <= a2 ]
            #print(ll)
            if len(ll) > 0:
                ok = True
            else:
                print('\n* FATAL ERROR * no anys trobats\n')
        except:
            print('\n* FATAL ERROR * no digits [DDDD DDDD]\n')
    else:
        print('\n* FATAL ERROR * format incorrecte [AAAA AAAA]\n')
    return ok

#separador definit
def valida_cops(cad, cops):
    ok = False

    #valida len cadena, mínim 3 (0 1)
    if len(cad) >= 3:
        sep = " "
        cad = cad.split(sep)
        n1 = cad[0]
        n2 = cad[1]
        #print(n1,n2)
        
        #si digits
        try:
            n1 = int(n1)
            n2 = int(n2)
            #dins llista cops
            ll = [ cop for cop in cops if cop >= n1 and cop <= n2 ]
            #print(ll)
            if len(ll) > 0:
                ok = True
            else:
                print('\n* FATAL ERROR * no trobat intèrval\n')
        except:
            print('\n* FATAL ERROR * no digits [D D]\n')
    else:
        print('\n* FATAL ERROR * format incorrecte [N N]\n')

    return ok

def nom_playlist(val):
    #depurem nom llista ja que mpc peta amb espais i caràcters especials
    nom = val.replace(' ', '')      #treure tots els espais
    #nom = val.split(' ')[0]                                 #primera paraula abans 1r espai
    nom = ''.join(char for char in nom if char.isalnum())   #.isalnum() si alfanumèric
    return nom

def crea_playlist(val,tipus):
    #ini
    #print(val,tipus)
    if tipus == 'ANY':            
        a1 = int(val[0:4])
        a2 = int(val[5:])
    elif tipus == 'COPS':
        sep = ' '
        #print(type(val))
        val = val.split(sep)
        n1 = int(val[0])
        n2 = int(val[1])

    #inicialitzem llista per fitxer m3u
    ll = ['#EXTM3U\n']

    #recupera cançons objecte àlbum
    for k,v in albums.items():
        #print(k)
        if tipus == 'GEN':
            if val == v.genere:
                ll += v.genera_m3u()
            nom = nom_playlist(val)
        elif tipus == 'AUTOR':
            if val == v.autor:
                ll += v.genera_m3u()
            nom = nom_playlist(val)
        elif tipus =='ANY':
            if int(v.any) >= a1 and int(v.any) <= a2:
                ll += v.genera_m3u()
            nom = str(a1) + '_' + str(a2)
        elif tipus == 'COPS':
            if v.reproduccions >= n1 and v.reproduccions <= n2:
                ll += v.genera_m3u()
            nom = str(n1) + '_' + str(n2)
        elif tipus == 'CERCA':
            ll += v.genera_m3u_cerca(val)
            nom = 'cerca_' + val
        elif tipus == 'ALBUM':
            if val == k:
                print(val, k)
                ll += v.genera_m3u()
            nom = nom_playlist(val)

    #print(ll)
    #si llista no buida, guardem fitxer m3u a carpeta playlist
    if len(ll) > 1:
        fitxer = DIR_PLAYLIST + '/' + nom + '.m3u'
        guarda_fitxer(fitxer,ll)

        #update mpc
        os.system('mpc update')

        print('\n* PLAYLIST %s CREADA *' %nom)

    else:
        print('\n* PLAYLIST BUIDA, NO CREADA *')

    #input('tecla per continuar...')

    return '0'

def load_playlist(playlist):
    
    #mpc clear llista en curs
    os.system('mpc clear')

    #mpc load llista
    os.system('mpc load ' + playlist)

    #mpc play llista
    os.system('mpc play 1')

    #update_reproducció àlbum de canço en curs
    reproduccions_album()

    #no hi ha cap opció mpc que mostri llista actual en curs
    #print('guardem playlist =',playlist)
    bash = f'echo {playlist} > {FILE_LLISTA}'
    os.system(bash)     

    return '0'

def get_metadades(fitxer):
    
    #gènere / any / autor
    ll = []
    
    # eyed3
    audiofile = eyed3.load(fitxer)
    ll.append(str(audiofile.tag.genre) + '\n')
    ll.append(str(audiofile.tag.getBestDate()) + '\n')
    if audiofile.tag.album_artist == None:
        ll.append(str(audiofile.tag.artist) + '\n')
    else:
        ll.append(str(audiofile.tag.album_artist) + '\n')

    return ll

"""
a) init_dir(): Aquesta funció només serà cridada per la funció reset() 
i té com a objectius:
 . Recórrer tots els directoris del “music directory” per buscar fitxers .mp3. 
    http://www.sromero.org/wiki/programacion/tutoriales/python/recorrer_arbol
 . Per cada directori on hi trobi, com a mínim, un .mp3 
        crea un objecte tipus àlbum i el guarda al diccionari, 
    utilitzant el nom del directori com a clau. 
    { “Àlbum1”: objecte, “Àlbum3”: objecte, “Àlbum4”: objecte, “Àlbum5”: objecte, “Àlbum6”: objecte }. 
    En principi no hi pot haver dos àlbums amb el mateix nom.
   Guardar el diccionari d’àlbums en un fitxer per poder restaurar-lo 
        el pròxim cop que obrim el programa.
"""

#init_dir(): Aquesta funció només serà cridada per la funció reset()
def init_dir():

    #init albums
    albums = {}

    #recòrrer tots els directoris sota un path
    #print('bases _______________________________')
    for base, dirs, files in os.walk(DIR_MUSIC):
        #print(base, type(base))     #directori base, str
        #print(dirs, type(dirs))     #dirs del dir base, list
        #print(files, type(files))   #fitxers del dir base, list

        #número fitxers mp3
        n_mp3 = conta_fitxers(base,'mp3')
        #print(type(n_mp3))
        #print(n_mp3)

        #input('* PAUSE *')
        
        #si hi ha mp3 a carpeta
        #print(n_mp3 > 0)
        if n_mp3 > 0 :
            fitxer = base + '/' + FILE_INFO
            
            #info.txt ?
            #print( existeix_fitxer(fitxer) )
            
            #si no hi és, crea fitxer per defecte
            #crear info.txt obtenim metadades del 1r track
            #print(files[0])
            
            #1r mp3 carpeta
            fitxer_mp3 = base + '/' + files[0]
            #print(fitxer_mp3)

            try:
                info_album = get_metadades(fitxer_mp3)
            except:
                info_album = INFO_DEF
            #print(info_album)

            if not existeix_fitxer(fitxer):
                #print('* FATAL ERROR* no hi ha ' + fitxer)
                guarda_fitxer(fitxer, info_album)
                #print( llegeix_fitxer(fitxer) )

            #contingut fitxer info.txt
            ll = llegeix_fitxer(fitxer)
            #print(ll)
            #print( len(ll) )

            album = crea_album(base,files,ll)
            
            #nom carpeta
            nom = base.split('/')[-1]
            #print(nom)

            #afegir objecte a diccionari amb clau .nom
            albums[nom] = album

    #print(albums)

    #Pickling files
    guarda_pickle(FILE_ALBUMS, albums)

    return albums

"""
b) init(): Aquesta funció serà cridada cada cop que s’executi 
el programa reproductorDAW.py. Té com a objectius:
 . Llegir el fitxer on hi ha els àlbums i carregar els àlbums. 
Si no existeix el fitxer, crea un diccionari àlbums buit.
 . Llegir l’estat on s’havia quedat el reproductor al tancar-lo l’últim cop, 
llegint el fitxer estat_reproductor.txt, escrit per la funció sortir(). 
Si el fitxer existeix, reproduirà el número de cançó i posició (en percentatge) 
on estava l’últim cop, amb volum 30 per defecte.
"""

def init():
    albums = {}

    #fitxer albums (albums) ?
    fitxer = FILE_ALBUMS
    #print( existeix_fitxer(fitxer) )
    
    #si no hi és, diccionari buit
    #if not existeix_fitxer(fitxer):
    #    print('* FATAL ERROR* no hi ha ' + fitxer)
        #Pickling files amb diccionari buit
    #    guarda_pickle(FILE_ALBUMS)

    if existeix_fitxer(fitxer):
        #Unpickling files
        infile = open(FILE_ALBUMS,'rb')
        albums = pickle.load(infile)
        infile.close()

    #carrega estat
    load_estat(FILE_ESTAT)

    #print('init() ', albums)

    return albums

"""
c) reset(): Aqueta funció només la cridarem quan afegim noves cançons 
o nous directoris dins la carpeta de música o si s’ha produït algun error. 
. Eliminarà tots els àlbums i llistes de reproducció del directori “playlist_directory”.
. Cridarà la funció init_dir().
. Reinicialitzarà el servei mpd “/etc/init.d/mpd restart” 
    i actualitzarà el mpc “mpc update”.
. Cridarà la funció init().
"""

def reset():
    #eliminar playlists
    #mpc
    #mpc clear
    bash = 'mpc clear'
    os.system(bash)

    #eliminar playlist directori
    #rm /home/aleon/Playlist/*.*
    bash = 'rm %s/*.*'%(DIR_PLAYLIST)
    os.system(bash)

    #fitxer playlist none
    bash = f'echo None > {FILE_LLISTA}'
    os.system(bash) 

    #init_dir
    init_dir()

    #restart mpd, cal ser root
    #systemctl restart mpd
    bash = 'systemctl restart mpd'
    os.system(bash)

    #update mpc
    os.system('mpc update')

    #init
    albums = init()
    
    return albums

"""
d) sortir(): A l’hora d’aturar el nostre programa Python, aquesta funció ha de:
. Guardar l’estat del reproductor en un fitxer anomenat estat_reproductor.txt. 
Aquesta informació la podeu extreure a partir de la sortida de la comanda 
“mpc status” i, per exemple, la podeu derivar directament en un fitxer de text:
    text='mpc status > '+directori+"estat_reproductor.txt"
    os.system(text)
. Actualitzar el fitxer dels àlbums. 
Principalment, servirà per actualitzar el número de cops 
    que s’ha reproduït cada àlbum. 
Per simplificar-ho, incrementarem aquest nombre d’un àlbum 
    cada cop que utilitzem una de les seves cançons per crear 
    una llista de reproducció.
"""

def sortir(albums):
    #guardar estat_reproductor.txt
    #mpc status > estat_reproductor.txt
    bash = 'mpc status > ' + FILE_ESTAT
    os.system(bash)

    #update fitxer albums
    #Pickling files
    guarda_pickle(FILE_ALBUMS, albums)

    #mpc stop
    os.system('mpc stop')

#eyed3
#https://stackoverflow.com/questions/24841191/get-mp3-play-time-using-eye3d-with-python
def track_info(filename):
    """Module Built To Read ID3 Track Data."""
    tag = id3.Tag()
    tag.parse(filename)
    a = load(filename)
    print("# {}".format('=' * 78))
    print("Track Name:     {}".format(tag.title))
    print("Track Artist:   {}".format(tag.artist))
    print("Track Album:    {}".format(tag.album))
    print("Track Duration: {}".format(duration_from_seconds(a.info.time_secs)))
    print("Track Number:   {}".format(tag.track_num))
    print("Track BitRate:  {}".format(a.info.bit_rate))
    print("Track BitRate:  {}".format(a.info.bit_rate_str))
    print("Sample Rate:    {}".format(a.info.sample_freq))
    print("Mode:           {}".format(a.info.mode))
    print("# {}".format('=' * 78))
    input()
    print("Album Artist:         {}".format(tag.album_artist))
    print("Album Year:           {}".format(tag.getBestDate()))
    print("Album Recording Date: {}".format(tag.recording_date))
    print("Album Type:           {}".format(tag.album_type))
    print("Disc Num:             {}".format(tag.disc_num))
    print("Artist Origin:        {}".format(tag.artist_origin))
    print("# {}".format('=' * 78))
    input()
    print("Artist URL:         {}".format(tag.artist_url))
    print("Audio File URL:     {}".format(tag.audio_file_url))
    print("Audio Source URL:   {}".format(tag.audio_source_url))
    print("Commercial URL:     {}".format(tag.commercial_url))
    print("Copyright URL:      {}".format(tag.copyright_url))
    print("Internet Radio URL: {}".format(tag.internet_radio_url))
    print("Publisher URL:      {}".format(tag.publisher_url))
    print("Payment URL:        {}".format(tag.payment_url))
    print("# {}".format('=' * 78))
    input()
    print("Publisher: {}".format(tag.publisher))
    print("Original Release Date: {}".format(tag.original_release_date))
    print("Play Count: {}".format(tag.play_count))
    print("Tagging Date: {}".format(tag.tagging_date))
    print("Release Date: {}".format(tag.release_date))
    print("Terms Of Use: {}".format(tag.terms_of_use))
    print("isV1: {}".format(tag.isV1()))
    print("isV2: {}".format(tag.isV2()))
    print("BPM: {}".format(tag.bpm))
    print("Cd Id: {}".format(tag.cd_id))
    print("Composer: {}".format(tag.composer))
    print("Encoding date: {}".format(tag.encoding_date))
    print("# {}".format('=' * 78))
    input()
    print("Genre: {}".format(tag.genre.name))
    print("Non Std Genre Name: {}".format(tag.non_std_genre.name))
    print("Genre ID: {}".format(tag.genre.id))
    print("Non Std Genre ID: {}".format(tag.non_std_genre.id))
    print("LAME Tag:       {}".format(a.info.lame_tag))
    print("# {}".format('=' * 78))
    input()
    print("Header Version: {}".format(tag.header.version))
    print("Header Major Version: {}".format(tag.header.major_version))
    print("Header Minor Version: {}".format(tag.header.minor_version))
    print("Header Rev Version: {}".format(tag.header.rev_version))
    print("Header Extended: {}".format(tag.header.extended))
    print("Header Footer: {}".format(tag.header.footer))
    print("Header Experimental: {}".format(tag.header.experimental))
    print("Header SIZE: {}".format(tag.header.SIZE))
    print("Header Tag Size: {}".format(tag.header.tag_size))
    print("Extended Header Size: {}".format(tag.extended_header.size))
    print("# {}".format('=' * 78))
    input()
    print("File Name: {}".format(tag.file_info.name))
    print("File Tag Size: {}".format(tag.file_info.tag_size))
    print("File Tag Padding Size: {}".format(tag.file_info.tag_padding_size))
    print("File Read Only: {}".format(tag.read_only))
    print("File Size: {}".format(a.info.size_bytes))
    print("Last Modified: {}".format(time.strftime('%Y-%m-%d %H:%M:%S',
                                     time.localtime(tag.file_info.mtime))))
    print("Last Accessed: {}".format(time.strftime('%Y-%m-%d %H:%M:%S',
                                     time.localtime(tag.file_info.atime))))
    print("# {}".format('=' * 78))


def duration_from_seconds(s):
    """Module to get the convert Seconds to a time like format."""
    s = s
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    timelapsed = "{:01d}:{:02d}:{:02d}:{:02d}".format(int(d),
                                                      int(h),
                                                      int(m),
                                                      int(s))
    return timelapsed



#test ______________________________________________________________
#test print
#print(albums)
#print(albums["Pirat's Sound Sistema - Sants Sistema"])
#print(albums["Music"])


#programa ______________________________________________________________
if __name__ == "__main__":
    #inicialtzem
    albums = init()
    op = ''
    #playlist = llegeix_playlist(FILE_LLISTA)
    
    while op != '0':
        
        #ini llistes
        generes = llegeix_generes(albums)
        autors = llegeix_autors(albums)
        anys = llegeix_anys(albums)
        anys.sort()
        cops = llegeix_cops(albums)
        cops.sort()
        playlists = llegeix_playlists()
        noms_albums = llegeix_noms_albums(albums)
        
        #print_albums(albums)
        print_info(albums)
        print_menu()
        op = input("opció: ")
        if op.upper() in MENU.keys() or op == '':
            #print("opció vàlida")
            if op == '':
                    os.system('mpc toggle')
            elif op == '>':
                    os.system('mpc next')
            elif op == '<':
                    os.system('mpc prev')
            elif op == '+':
                    os.system('mpc volume +1')
            elif op == '-':
                    os.system('mpc volume -1')
            elif op == 'r':
                    os.system('mpc random')
            elif op.upper() == 'A':
                opa = ''
                while opa != '0':
                    genera_menu(noms_albums)
                    opa = input("Àlbum NUM [<< 0] : ")
                    if opa in [str(i) for i in range(1,len(noms_albums)+1)]:
                        #info album
                        key = noms_albums[int(opa)-1]
                        print(key)
                        print(albums[key])
                        #input('tecla per continuar...')                   
                        opb = ''
                        while opb != '0':
                            menu_edita()
                            opb = input("opció: ").upper()
                            if opb in MENU_EDITA.keys() or opb == '':
                                #editar info.txt d'album i carpeta
                                if opb.upper() == 'E':
                                    ll = []
                                    #1
                                    opc = ''
                                    while opc == '':
                                        opc = input(f'Gènere [{albums[key].genere}]: ')
                                        if opc == '':
                                            #mantenim igual
                                            opc = albums[key].genere
                                        else:
                                            #valida?
                                            pass
                                    ll.append(opc)
                                    #2
                                    opc = ''
                                    while opc == '':
                                        opc = input(f'Any [{albums[key].any}]: ')
                                        if opc == '':
                                            #mantenim igual
                                            opc = albums[key].any
                                        else:
                                            #valida?
                                            #print('regexp ', re.fullmatch('\d{4,4}', opc))
                                            r = re.fullmatch('\d{4,4}', opc)
                                            if not r:
                                                opc = ''
                                    ll.append(opc)
                                    #3
                                    opc = ''
                                    while opc == '':
                                        opc = input(f'Autor [{albums[key].autor}]: ')
                                        if opc == '':
                                            #mantenim igual
                                            opc = albums[key].autor
                                        else:
                                            #valida?
                                            pass
                                    ll.append(opc)
                                    
                                    #update album
                                    #print(ll)
                                    albums[key].update_info(ll)
                                    
                                    #update info.txt
                                    fitxer = albums[key].ruta + '/' + FILE_INFO                               
                                    if existeix_fitxer(fitxer):
                                        llfitxer = [el + '\n' for el in ll ]
                                        #print(llfitxer)
                                        guarda_fitxer(fitxer, llfitxer)
                                                                #eliminar
                                #llistar i metadata mp3
                                elif opb.upper() == 'I':
                                    opc = ''
                                    while opc != '0':
                                        #llistar mp3
                                        genera_menu(albums[key].mp3)
                                        opc = input("Info MP3 NUM [<< 0] : ")
                                        if opc in [str(i) for i in range(1,len(albums[key].mp3)+1)]:
                                            path_mp3 = albums[key].ruta + '/' + albums[key].mp3[int(opc)-1]
                                            print(path_mp3)
                                            #audiofile = eyed3.load(path_mp3)
                                            track_info(path_mp3)
                                #eliminar
                                elif opb == '-':
                                    opc = ''
                                    while opc != '0':
                                        #llistar mp3
                                        genera_menu(albums[key].mp3)
                                        opc = input("Elimina NUM [<< 0] : ")
                                        if opc in [str(i) for i in range(1,len(albums[key].mp3)+1)]:
                                            print(f"\n* Eliminada NUM {opc} *\n")
                                            albums[key].borra_mp3(int(opc)-1)
                                #afegir
                                elif opb == '+':
                                    opc = ''
                                    while opc != '0':
                                        #llistar mp3 borrades
                                        genera_menu(albums[key].borrades)
                                        opc = input("Afegeix NUM [<< 0] : ")
                                        if opc in [str(i) for i in range(1,len(albums[key].borrades)+1)]:
                                            print(f"\n* Afegida NUM {opc} *\n")
                                            albums[key].recupera_mp3(int(opc)-1)

            elif op.upper() == 'L':
                opa = ''
                while opa != '0':
                    genera_menu(playlists)
                    opa = input("opció [<< 0] : ")
                    if opa in [str(i) for i in range(1,len(playlists)+1)]:
                        #print('* ok playlist *')
                        opa = load_playlist(playlists[int(opa)-1])
            elif op.upper() == 'C':
                    opa = ''
                    while opa != '0':
                        menu_playlist()
                        opa = input("opció: ").lower()
                        if opa in MENU_PLAYLIST.keys():
                            #crear playlist gènere
                            if opa == '1':
                                opb = ''
                                while opb != '0':
                                    print(generes)
                                    genera_menu(generes)
                                    opb = input("opció [<< 0] : ")
                                    if opb in [str(i) for i in range(1,len(generes)+1)]:
                                        #print('* ok gènere *')
                                        opb = crea_playlist(generes[int(opb)-1],'GEN')
                            #crear playlist autor
                            elif opa == '2':
                                opb = ''
                                while opb != '0':
                                    print(autors)
                                    genera_menu(autors)
                                    opb = input("opció [<< 0] : ")
                                    if opb in [str(i) for i in range(1,len(autors)+1)]:
                                        #print('* ok autor *')
                                        opb = crea_playlist(autors[int(opb)-1],'AUTOR')
                            #crear playlist intèrval anys
                            elif opa == '3':
                                    opb = ''
                                    while opb != '0':
                                        print(anys)
                                        opb = input("\nde ANY a ANY [<< 0] : ")
                                        if valida_anys(opb,anys):
                                            opb = crea_playlist(opb,'ANY')
                            #crear playlist intèrval reproduccions
                            elif opa == '4':
                                    opb = ''
                                    while opb != '0':
                                        print(cops)
                                        opb = input("\nde NUM a NUM [<< 0] : ")
                                        if valida_cops(opb,cops):
                                            opb = crea_playlist(opb,'COPS')
                            #crear playlist segons paraula
                            elif opa == '5':
                                    opb = ''
                                    while opb != '0':
                                        opb = input("Paraula [<< 0] : ")
                                        if opb != '' and opb != '0':
                                            opb = crea_playlist(opb,'CERCA')
                                                        #crear playlist segons paraula
                            elif opa == '6':
                                    opb = ''
                                    while opb != '0':
                                        print(noms_albums)
                                        print('\nT -> * TOTS *', end='')
                                        genera_menu(noms_albums)
                                        opb = input("opció [<< 0] : ")
                                        if opb in [str(i) for i in range(1,len(noms_albums)+1)]:
                                            #print('* ok album *')
                                            opb = crea_playlist(noms_albums[int(opb)-1],'ALBUM')
                                        elif opb.upper() == 'T':
                                            #print('tots!')
                                            for nom in noms_albums:
                                                opb = crea_playlist(nom, 'ALBUM')

            elif op == 'R':
                    albums = reset()
                    #print('return reset() ', albums)
            elif op == '0':
                    sortir(albums)
        else:
            #opció vol +/- enter
            print(op)
            if op[0]=='+' and op[1:] in [str(n) for n in range(100+1)]:
                #print(op[0])
                #print(op[1:])
                os.system(f'mpc volume +{op[1:]}')
            elif op[0]=='-' and op[1:] in [str(n) for n in range(100+1)]:
                #print(op[0])
                #print(op[1:])
                os.system(f'mpc volume -{op[1:]}')
            else:
                print("\n*FATAL ERROR* opció no vàlida\n")
