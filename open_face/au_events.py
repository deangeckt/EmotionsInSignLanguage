import os
import numpy as np
import matplotlib.pyplot as plt

au_list = ['AU01_r', 'AU02_r', 'AU04_r', 'AU05_r', 'AU06_r', 'AU07_r', 'AU09_r', 'AU10_r',
           'AU12_r', 'AU15_r', 'AU17_r', 'AU01_c', 'AU02_c', 'AU04_c', 'AU05_c', 'AU06_c', 'AU07_c',
           'AU09_c', 'AU10_c', 'AU12_c', 'AU14_c', 'AU15_c', 'AU17_c', 'AU28_c']
au_fix_thresholds = {'AU01_r': 2, 'AU02_r': 2, 'AU04_r': 1.25, 'AU05_r': 2, 'AU06_r': 1.9,
                     'AU07_r': 1.25, 'AU09_r': 2, 'AU10_r': 1.8, 'AU12_r': 2, 'AU15_r': 2,
                     'AU17_r': 1.75
                     }

non_bin_aus = [au for au in au_list if au.endswith('r')]
bin_aus = [au for au in au_list if au.endswith('c')]
num_of_segments = 3


class AuEvents:
    def __init__(self, au_id, vid_id):
        self.vid_id = vid_id
        self.au_id = au_id

        self.is_bin_au = au_id in bin_aus
        self.events = {}
        for i in range(num_of_segments):
            self.events[i] = []

        # Thresholds
        self.min_wd = 4  # min num of frames above dy threshold

        # calculating during process
        self.dy_au_th = None
        self.au = None
        self.segments = None
        self.segments_len = None

        self.start_idx = -1
        self.end_idx = -1

    def __add_event(self, segment_idx):
        # validate event length
        if self.end_idx - self.start_idx < self.min_wd:
            return

        idx_offset = sum(self.segments_len[0:segment_idx])
        in_seg_start = self.start_idx - idx_offset
        in_seg_end = self.end_idx - idx_offset

        intensity = np.mean(self.segments[segment_idx][in_seg_start:in_seg_end])
        self.events[segment_idx].append({'s': self.start_idx,
                                         'e': self.end_idx,
                                         'i': intensity})
        self.start_idx = -1
        self.end_idx = -1

    def __segment_event(self, segment, segment_idx):
        idx_offset = sum(self.segments_len[0:segment_idx])
        self.start_idx = -1
        self.end_idx = -1

        for idx, v in enumerate(segment):
            frame_idx = idx + idx_offset
            if v >= self.dy_au_th and v > 0:
                if self.start_idx == -1:
                    self.start_idx = frame_idx
            else:
                if self.start_idx != -1:
                    self.end_idx = frame_idx
                    self.__add_event(segment_idx)

        # segment ended during an event
        if self.start_idx != -1:
            self.end_idx = len(segment) - 1 + idx_offset
            self.__add_event(segment_idx)

    def plot_events(self, save=False):
        if self.is_bin_au:
            return
        fig = plt.figure(figsize=(4, 5))
        all_events = [item for sublist in self.events.values() for item in sublist]
        st_idx = [m['s'] for m in all_events]
        en_idx = [m['e'] for m in all_events]
        zeros = [0] * len(st_idx)
        plt.scatter(x=st_idx, y=zeros, color='green')
        plt.scatter(x=en_idx, y=zeros, color='red')

        plt.axhline(y=self.dy_au_th, color='purple', linestyle='-')
        for st in st_idx:
            plt.axvline(x=st, color='green', ls='--')
        for en in en_idx:
            plt.axvline(x=en, color='red', ls='--')

        plt.plot(self.au, label=self.au_id)
        plt.legend()
        title = f"{self.vid_id}-{self.au_id}"
        plt.title(title)

        if save:
            os.makedirs("events_plots", exist_ok=True)
            plt.savefig(f"events_plots/{title}.png")
        else:
            plt.show()
        plt.close(fig)

    def process(self, au: np.ndarray):
        self.au = au
        if self.is_bin_au:
            return None

        self.dy_au_th = np.mean(self.au) * au_fix_thresholds[self.au_id]
        self.segments = np.array_split(au, num_of_segments)
        self.segments_len = [len(s) for s in self.segments]

        for idx, segment in enumerate(self.segments):
            self.__segment_event(segment, idx)

        response = {}
        for e in self.events:
            intensities = [se['i'] for se in self.events[e]]
            response[f"e{e}_i"] = np.mean(intensities) if intensities else 0
            response[f"e{e}_a"] = len(intensities)
        return response
