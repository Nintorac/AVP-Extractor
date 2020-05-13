#%%
import soundfile as snd
import numpy as np
from pathlib import Path
from contextlib import suppress
from uuid import uuid4
import csv
root_path = Path('.')
out_path = Path('extracted')

out_path.mkdir()

uuid = lambda: uuid4().hex

abbr_type_map = {

    'hhc': 'hihat-closed',
    'hho': 'hihat-open',
    'kd': 'kick',
    'sd': 'snare',
}

# %%

for path in root_path.rglob('*.csv'):
    
    wav_path  = path.with_suffix('.wav')
    audio, sample_rate = snd.read(wav_path.as_posix())

    data = csv.reader(open(path.as_posix()), delimiter=',')
    time, percuss_type = zip(*data)

    time = np.array([float(t) for t in time])

    sample_no = np.round(time * sample_rate).astype('intp')

    for start, finish, p_type in zip(sample_no[:-1], sample_no[1:], percuss_type):

        p_type = p_type.strip()

        if p_type=='':
            print(path)
            continue

        p_type = abbr_type_map.get(p_type, None)

        if p_type is None:
            continue

        clip = audio[start:finish]

        clip_folder = out_path.joinpath(p_type)

        with suppress(FileExistsError):
            clip_folder.mkdir()
        
        clip_path = clip_folder.joinpath(uuid()).with_suffix('.wav')
        snd.write(clip_path.as_posix(), clip, sample_rate)




# %%
