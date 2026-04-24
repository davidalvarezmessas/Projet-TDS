import os
import random
import numpy as np
import matplotlib.pyplot as plt

from scipy.io.wavfile import read
from algorithm import *

# ----------------------------------------------
# Run the script
# ----------------------------------------------
if __name__ == '__main__':

    # 1: Load the database
    with open('songs.pickle', 'rb') as handle:
        database = pickle.load(handle)

    # 2: Encoder
    nperseg=128
    noverlap=32
    min_distance=50
    time_window=1.
    freq_window=1500
    encoder = Encoding(nperseg=nperseg, noverlap=noverlap, 
      min_distance=min_distance,
      time_window=time_window, 
      freq_window=freq_window)
      
   
    # 3: Randomly get an extract from one of the songs of the database
    songs = [item for item in os.listdir('Projet-TDS\samples') if item.endswith('.wav')]
    song = random.choice(songs)
    print('Selected song: ' + song[:-4])
    filename = 'Projet-TDS/samples/' + song

    fs, s = read(filename)
    #tstart = np.random.randint(20, 90)
    #On modifie la définition de tstart pour éviter de récupérer des extrait de moins de 10 secondes voir vide
    song_duration = len(s) / fs
    max_start = max(1, int(song_duration - 10))
    tstart = np.random.randint(0, max_start)
    tmin = int(tstart*fs)
    duration = int(10*fs)

    # 4: Use the encoder to extract a signature from the extract
    encoder.process(fs, s[tmin:tmin + duration])
    hashes = encoder.hashes

    print("Recherche en cours")
    best_match = None
    best_score = 0
    for item in database:
        matcher = Matching(hashes1=hashes, hashes2=item['hashcodes'])
        print (f"Comparaison avec {item['song']}, score={matcher.max_count}")
        if matcher.max_count > best_score:
            best_score = matcher.max_count
            best_match = item['song']
    
    if best_match:
        print(f'\n Pour le morceau recherché : {song[:-4]} on a :')
        print(f"Morceau identifié : {best_match} (score={best_score})")
        # To display, need to recompute the matcher for the best
        for item in database:
            if item['song'] == best_match:
                matcher = Matching(hashes1=hashes, hashes2=item['hashcodes'])
                break
        print("Affichage du nuage de points :")
        matcher.display_scatterplot()
        print("Affichage de l'histogramme :")
        matcher.display_histogram()
    else:
        print(f"\nAucun morceau correspondant trouvé, best_score={best_score}")
        
        
    filename = "Projet-TDS/secret_sample.wav"
    fs, s = read(filename)
    encoder.process(fs, s)
    hashes = encoder.hashes
    print("Recherche en cours pour le morceau secret")
    best_match = None
    best_score = 0
    for item in database:
        matcher = Matching(hashes1=hashes, hashes2=item['hashcodes'])
        print(f"Comparaison avec {item['song']}, score={matcher.max_count}")
        if matcher.max_count > best_score:
            best_score = matcher.max_count
            best_match = item['song']
    
    if best_match:
        print(f"\n Morceau identifié : {best_match} (score={best_score})")
        # To display, need to recompute the matcher for the best
        for item in database:
            if item['song'] == best_match:
                matcher = Matching(hashes1=hashes, hashes2=item['hashcodes'])
                break
        print("Nuage de points :")
        matcher.display_scatterplot()
        print("Histogramme :")
        matcher.display_histogram()
    else:
        print(f"\nAucun morceau trouvé, meilleur score={best_score}")