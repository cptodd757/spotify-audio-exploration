import numpy as np 
import matplotlib.pyplot as plt
import config

def visualize_segments(segments,name="noname"):
    times = np.array([])
    pitches = np.array([])
    pitch_strengths = np.array([])
    for segment in segments:

        ###IF WANT TOP N PITCHES:
        n = 2
        top_pitches = np.flip(np.argsort(segment["pitches"]))[:n]
        top_pitches_strengths = [segment["pitches"][i] for i in top_pitches]
        
        ###IF WANT PITCHES ABOVE A CERTAIN THRESHOLD:
        # threshold = .4
        # p = np.array(segment["pitches"])
        # top_pitches = np.argwhere(p > threshold).flatten()
        # top_pitches_strengths = p[top_pitches]
        # print(p,top_pitches,top_pitches_strengths)

        n = len(top_pitches)
        time = segment["start"]

        lower = 0
        upper = 20
        if time < lower:
            continue
        if time > upper:
            break

        pitches = np.append(pitches,top_pitches)
        pitch_strengths = np.append(pitch_strengths,top_pitches_strengths)
        for i in range(n):
            times = np.append(times,time)

    plt.scatter(times,pitches,marker="s",s=100,c=pitch_strengths, cmap='Purples')
    plt.yticks(range(12), config.pitch_names)
    plt.savefig(name + '.png')
    plt.show()