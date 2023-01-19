import os
import sys
import py
import musicpy as mp
import time
import numpy

os.environ['PATH'] = os.pathsep.join(os.environ['PATH'].split(os.pathsep)[:-1])
os.environ['PATH'] += os.pathsep + os.path.dirname(__file__)
from . import fluidsynth
from pydub import AudioSegment
from io import BytesIO
from copy import deepcopy as copy

try:
    mp.pygame.mixer.quit()
    mp.pygame.mixer.init(44100, -16, 2, 1024)
    mp.pygame.mixer.set_num_channels(1000)
except mp.pygame.error:
    has_audio_interface = False


def play_sound(audio, mode=0, wait=False):
    if mp.pygame.mixer.get_busy():
        mp.pygame.mixer.stop()
    current_audio = audio
    if mode == 0:
        if current_audio.channels == 1:
            current_audio = current_audio.set_frame_rate(44100).set_channels(2)
        current_sound_object = mp.pygame.mixer.Sound(
            buffer=current_audio.raw_data)
        current_sound_object.play()
        if wait:
            while mp.pygame.mixer.get_busy():
                mp.pygame.time.delay(10)
    elif mode == 1:
        capture = get_capture()
        try:
            current_file = BytesIO()
            current_audio.export(current_file, format='wav')
            current_sound_object = mp.pygame.mixer.Sound(file=current_file)
        except:
            current_path = os.getcwd()
            os.chdir(os.path.dirname(__file__))
            current_audio.export('temp.wav', format='wav')
            current_sound_object = mp.pygame.mixer.Sound(file='temp.wav')
            os.remove('temp.wav')
            os.chdir(current_path)
        current_sound_object.play()
        if wait:
            while mp.pygame.mixer.get_busy():
                mp.pygame.time.delay(10)
        reset_capture(capture)


def stop():
    mp.pygame.mixer.stop()


def bar_to_real_time(bar, bpm, mode=0):
    # return time in ms
    return int(
        (60000 / bpm) * (bar * 4)) if mode == 0 else (60000 / bpm) * (bar * 4)


def real_time_to_bar(time, bpm):
    return (time / (60000 / bpm)) / 4


def velocity_to_db(vol):
    if vol == 0:
        return -100
    return mp.math.log(vol / 127, 10) * 20


def percentage_to_db(vol):
    if vol == 0:
        return -100
    return mp.math.log(abs(vol / 100), 10) * 20


def apply_fadeout(current_chord, decay, fixed_decay, new=True):
    if isinstance(current_chord, mp.piece):
        temp = copy(current_chord)
        if isinstance(decay, list):
            for i in range(len(temp.tracks)):
                apply_fadeout(each, decay[i], fixed_decay, False)
        else:
            for each in temp.tracks:
                apply_fadeout(each, decay, fixed_decay, False)
        return temp
    temp = copy(current_chord) if new else current_chord
    if fixed_decay:
        if isinstance(decay, list):
            for i in range(len(temp.notes)):
                each = temp.notes[i]
                if isinstance(each, mp.note):
                    each.duration += decay[i]
        else:
            for each in temp.notes:
                if isinstance(each, mp.note):
                    each.duration += decay
    else:
        if isinstance(decay, list):
            for i in range(len(temp.notes)):
                each = temp.notes[i]
                if isinstance(each, mp.note):
                    each.duration += each.duration * decay[i]
        else:
            for each in temp.notes:
                if isinstance(each, mp.note):
                    each.duration += each.duration * decay
    return temp


def get_timestamps(current_chord,
                   bpm,
                   ignore_other_messages=False,
                   pan=None,
                   volume=None):
    for i in range(len(current_chord.notes)):
        current = current_chord.notes[i]
        if isinstance(current, mp.pitch_bend) and current.start_time is None:
            current.start_time = sum(current_chord.interval[:i])
    noteon_part = [
        general_event(
            'noteon',
            bar_to_real_time(sum(current_chord.interval[:i]), bpm, 1) / 1000,
            current_chord.notes[i]) for i in range(len(current_chord.notes))
        if isinstance(current_chord.notes[i], mp.note)
    ]
    noteoff_part = [
        general_event(
            'noteoff',
            bar_to_real_time(
                sum(current_chord.interval[:i]) +
                current_chord.notes[i].duration, bpm, 1) / 1000,
            current_chord.notes[i]) for i in range(len(current_chord.notes))
        if isinstance(current_chord.notes[i], mp.note)
    ]
    pitch_bend_part = [
        general_event('pitch_bend',
                      bar_to_real_time(i.start_time, bpm, 1) / 1000, i)
        for i in current_chord.notes if isinstance(i, mp.pitch_bend)
    ]
    result = noteon_part + noteoff_part + pitch_bend_part
    if not ignore_other_messages:
        other_messages_part = [
            general_event('message',
                          bar_to_real_time(i.start_time, bpm, 1) / 1000, i)
            for i in current_chord.other_messages
        ]
        result += other_messages_part
    if pan:
        pan_part = [
            general_event(
                'message',
                bar_to_real_time(i.start_time, bpm, 1) / 1000,
                mp.event('control_change',
                         channel=i.channel,
                         control=10,
                         value=i.value)) for i in pan
        ]
        result += pan_part
    if volume:
        volume_part = [
            general_event(
                'message',
                bar_to_real_time(i.start_time, bpm, 1) / 1000,
                mp.event('control_change',
                         channel=i.channel,
                         control=7,
                         value=i.value)) for i in volume
        ]
        result += volume_part
    result.sort(key=lambda s: (s.start_time, s.event_type))
    return result


def get_capture():
    try:
        capture = py.io.StdCaptureFD(out=True, in_=False)
    except:
        capture = None
    return capture


def reset_capture(capture):
    if capture is not None:
        capture.reset()


def process_effect(sound, effects, **kwargs):
    current_args = kwargs
    for each in effects:
        each.process_unknown_args(**current_args)
        sound = each.process(sound)
    return sound


def set_effect(sound, *effects):
    if len(effects) == 1:
        current_effect = effects[0]
        if not isinstance(current_effect, effect):
            if isinstance(current_effect, effect_chain):
                effects = current_effect.effects
            else:
                effects = list(current_effect)
        else:
            effects = list(effects)
    else:
        effects = list(effects)
    sound.effects = effects
    return sound


def check_effect(sound):
    return hasattr(sound, 'effects') and isinstance(sound.effects,
                                                    list) and sound.effects


def adsr_func(sound, attack, decay, sustain, release):
    change_db = percentage_to_db(sustain)
    result_db = sound.dBFS + change_db
    if attack > 0:
        sound = sound.fade_in(attack)
    if decay > 0:
        sound = sound.fade(to_gain=result_db, start=attack, duration=decay)
    else:
        sound = sound[:attack].append(sound[attack:] + change_db)
    if release > 0:
        sound = sound.fade_out(release)
    return sound


class effect:

    def __init__(self, func, name=None, *args, unknown_args=None, **kwargs):
        self.func = func
        if name is None:
            name = 'effect'
        self.name = name
        self.parameters = [args, kwargs]
        if unknown_args is None:
            unknown_args = {}
        self.unknown_args = unknown_args

    def process(self, sound, *args, unknown_args=None, **kwargs):
        if args or kwargs or unknown_args:
            return self.func(*args, **kwargs, **unknown_args)
        else:
            return self.func(sound, *self.parameters[0], **self.parameters[1],
                             **self.unknown_args)

    def process_unknown_args(self, **kwargs):
        for each in kwargs:
            if each in self.unknown_args:
                self.unknown_args[each] = kwargs[each]

    def __call__(self, *args, unknown_args=None, **kwargs):
        temp = copy(self)
        temp.parameters[0] = args + temp.parameters[0][len(args):]
        temp.parameters[1].update(kwargs)
        if unknown_args is None:
            unknown_args = {}
        temp.unknown_args.update(unknown_args)
        return temp

    def new(self, *args, unknown_args=None, **kwargs):
        temp = copy(self)
        temp.parameters = [args, kwargs]
        temp.parameters[1].update(kwargs)
        if unknown_args is None:
            unknown_args = {}
        temp.unknown_args = unknown_args
        return temp

    def __repr__(self):
        return f'[effect]\nname: {self.name}\nparameters: {self.parameters} unknown arguments: {self.unknown_args}'


class effect_chain:

    def __init__(self, *effects):
        self.effects = list(effects)

    def __call__(self, sound):
        sound.effects = self.effects
        return sound

    def __repr__(self):
        return f'[effect chain]\neffects:\n' + '\n\n'.join(
            [str(i) for i in self.effects])


class general_event:

    def __init__(self, event_type, start_time, value=None, other=None):
        self.event_type = event_type
        self.start_time = start_time
        if self.start_time < 0:
            self.start_time = 0
        self.value = value
        self.other = other

    def __repr__(self):
        return f'[general event] type: {self.event_type}  start_time: {self.start_time}s  value: {self.value}  other: {self.other}'


class sf2_loader:

    def __init__(self, file=None):
        self.file = []
        self.synth = fluidsynth.Synth()
        self.apply_synth_settings()
        self.sfid_list = []
        self._current_channel = 0
        self.current_sfid = 1
        self.current_bank = 0
        self.current_preset = 0
        if file:
            self.load(file)

    def change_setting(self, parameter, value):
        self.synth.setting(f'synth.{parameter}', value)

    def apply_synth_settings(self):
        self.change_setting('gain', 0.2)
        self.change_setting('reverb.active', 0)
        reverb_parameters = ['damp', 'level', 'room-size', 'width']
        current_reverb_values = [0.0, 0.9, 0.2, 0.5]
        chorus_parameters = ['depth', 'level', 'nr', 'speed']
        current_chorus_values = [8.0, 2.0, 3, 0.3]
        for i, each in enumerate(reverb_parameters):
            self.change_setting(f'reverb.{each}', current_reverb_values[i])
        self.change_setting('chorus.active', 0)
        for i, each in enumerate(chorus_parameters):
            self.change_setting(f'chorus.{each}', current_chorus_values[i])

    @property
    def current_channel(self):
        return self._current_channel

    @current_channel.setter
    def current_channel(self, value):
        self._current_channel = value
        current_channel_info = self.synth.program_info(value)
        if current_channel_info[0] == 0:
            self.synth.sfont_select(value, self.sfid_list[0])
            current_channel_info = self.find_channel_info(value)
        self.current_sfid, self.current_bank, self.current_preset = current_channel_info

    def find_channel_info(self, value):
        capture = get_capture()
        current_channel_info = self.synth.program_info(value)
        current_sfid = current_channel_info[0]
        current_bank = current_channel_info[1]
        if current_sfid == 0:
            current_sfid = self.sfid_list[0]
        for i in range(128):
            select_status = self.synth.program_select(value, current_sfid,
                                                      current_bank, i)
            if select_status != -1:
                current_channel_info = self.synth.program_info(value)
                break
        reset_capture(capture)
        return current_channel_info

    def __repr__(self):
        return f'''[soundfont loader]
loaded soundfonts: {self.file}
soundfonts id: {self.sfid_list}
current channel: {self.current_channel}
current soundfont id: {self.current_sfid}
current soundfont name: {os.path.basename(self.file[self.sfid_list.index(self.current_sfid)]) if self.file and self.current_sfid != 0 else ""}
current bank number: {self.current_bank}
current preset number: {self.current_preset}
current preset name: {self.get_current_instrument()}'''

    def change(self,
               channel=None,
               sfid=None,
               bank=None,
               preset=None,
               correct=True,
               hide_warnings=True,
               mode=0):
        if hide_warnings:
            capture = get_capture()
        select_status = 0
        if channel is not None:
            if mode == 0:
                self.change_channel(channel)
        else:
            channel = self.current_channel
        current_channel_info = self.synth.program_info(channel)
        if current_channel_info[0] == 0:
            self.synth.sfont_select(channel, self.sfid_list[0])
            current_channel_info = self.find_channel_info(channel)
        current_sfid, current_bank, current_preset = current_channel_info
        if sfid is not None:
            self.change_sfid(sfid, channel)
        else:
            sfid = current_sfid
        if bank is not None:
            self.change_bank(bank, channel)
        else:
            bank = current_bank
        if preset is not None:
            if isinstance(preset, str):
                instruments, instruments_ind = self.get_all_instrument_names(
                    sfid=current_sfid,
                    bank=current_bank,
                    return_mode=1,
                    get_ind=True)
                if preset in instruments:
                    preset = instruments_ind[instruments.index(preset)]
                else:
                    preset = -1
            select_status = self.synth.program_select(channel, sfid, bank,
                                                      preset)
            if select_status == -1:
                if correct:
                    self.synth.program_select(channel, current_sfid,
                                              current_bank, current_preset)
                    if channel == self.current_channel:
                        self.current_sfid = current_sfid
                        self.current_bank = current_bank
                        self.current_preset = current_preset
                else:
                    if channel == self.current_channel:
                        self.current_preset = preset
            else:
                if channel == self.current_channel:
                    self.current_preset = preset
        if hide_warnings:
            reset_capture(capture)
        return select_status

    def change_preset(self, preset, channel=None):
        if channel is None:
            channel = self.current_channel
        current_channel_info = self.synth.program_info(channel)
        if current_channel_info[0] == 0:
            self.synth.sfont_select(channel, self.sfid_list[0])
            current_channel_info = self.find_channel_info(channel)
        current_sfid, current_bank, current_preset = current_channel_info
        if isinstance(preset, str):
            instruments, instruments_ind = self.get_all_instrument_names(
                sfid=current_sfid,
                bank=current_bank,
                return_mode=1,
                get_ind=True)
            if preset in instruments:
                current_ind = instruments_ind[instruments.index(preset)]
                self.synth.program_select(channel, current_sfid, current_bank,
                                          current_ind)
                if channel == self.current_channel:
                    self.current_preset = current_ind
        else:
            self.synth.program_select(channel, current_sfid, current_bank,
                                      preset)
            if channel == self.current_channel:
                self.current_preset = preset

    def change_bank(self, bank, channel=None):
        if channel is None:
            channel = self.current_channel
        self.synth.bank_select(channel, bank)
        if channel == self.current_channel:
            self.current_bank = bank
        capture = get_capture()
        self.synth.program_select(channel, *self.synth.program_info(channel))
        reset_capture(capture)

    def change_channel(self, channel):
        self.current_channel = channel

    def change_sfid(self, sfid, channel=None):
        if channel is None:
            channel = self.current_channel
        self.synth.sfont_select(channel, sfid)
        if channel == self.current_channel:
            self.current_sfid = sfid
        capture = get_capture()
        self.synth.program_select(channel, *self.synth.program_info(channel))
        reset_capture(capture)

    def change_soundfont(self, name, channel=None):
        if name in self.file:
            ind = self.file.index(name)
            self.change_sfid(self.sfid_list[ind], channel)
        else:
            names = [os.path.basename(i) for i in self.file]
            if name in names:
                ind = names.index(name)
                self.change_sfid(self.sfid_list[ind], channel)

    def __lt__(self, preset):
        if isinstance(preset, tuple) and len(preset) == 2:
            self.change(preset=preset[0], bank=preset[1])
        else:
            self.change(preset=preset)

    def __mod__(self, channel):
        self.change_channel(channel)

    def get_current_instrument(self):
        if self.valid_channel(self.current_channel):
            result = self.synth.channel_info(self.current_channel)[3]
        else:
            result = ''
        if isinstance(result, bytes):
            result = result.decode('utf-8')
        return result

    def get_instrument_name(self,
                            sfid=None,
                            bank=None,
                            preset=None,
                            hide_warnings=True):
        if fluidsynth.fluid_sfont_get_preset:
            if sfid is None:
                sfid = self.current_sfid
            if bank is None:
                bank = self.current_bank
            if preset is None:
                preset = self.current_preset
            try:
                result = self.synth.sfpreset_name(sfid, bank, preset)
            except:
                result = None
            return result
        channel = self.current_channel
        current_sfid = copy(self.current_sfid)
        current_bank = copy(self.current_bank)
        current_preset = copy(self.current_preset)
        select_status = self.change(channel,
                                    sfid,
                                    bank,
                                    preset,
                                    hide_warnings=hide_warnings)
        result = self.synth.channel_info(channel)[3]
        self.change(channel,
                    current_sfid,
                    current_bank,
                    current_preset,
                    hide_warnings=hide_warnings)
        if select_status != -1:
            if isinstance(result, bytes):
                result = result.decode('utf-8')
            return result

    def get_all_instrument_names(self,
                                 sfid=None,
                                 bank=None,
                                 max_num=128,
                                 get_ind=False,
                                 mode=0,
                                 return_mode=0,
                                 hide_warnings=True):
        if hide_warnings:
            capture = get_capture()
        if fluidsynth.fluid_sfont_get_preset:
            preset_mode = 0
        else:
            preset_mode = 1
            current_channel = self.current_channel
            current_sfid = copy(self.current_sfid)
            current_bank = copy(self.current_bank)
            current_preset = copy(self.current_preset)
            self.change(current_channel, sfid, bank, hide_warnings=False)
        result = []
        if get_ind:
            ind = []
        for i in range(max_num):
            try:
                if preset_mode == 0:
                    current_name = self.get_instrument_name(
                        sfid=sfid, bank=bank, preset=i, hide_warnings=False)
                else:
                    current_name = self.get_instrument_name(
                        preset=i, hide_warnings=False)
                if current_name:
                    result.append(current_name)
                    if get_ind:
                        ind.append(i)
            except:
                pass
        if preset_mode == 1:
            self.change(current_channel,
                        current_sfid,
                        current_bank,
                        ind[0] if get_ind and mode == 1 else current_preset,
                        hide_warnings=False)
        else:
            if get_ind and mode == 1:
                self.change(preset=ind[0], hide_warnings=False)
        if hide_warnings:
            reset_capture(capture)
        if get_ind:
            if return_mode == 0:
                return {ind[i]: result[i] for i in range(len(result))}
            elif return_mode == 1:
                return result, ind
        else:
            return result

    def all_instruments(self,
                        max_bank=129,
                        max_preset=128,
                        sfid=None,
                        hide_warnings=True):
        if hide_warnings:
            capture = get_capture()
        if fluidsynth.fluid_sfont_get_preset:
            preset_mode = 0
        else:
            preset_mode = 1
            current_sfid = copy(self.current_sfid)
            if sfid is not None:
                self.change_sfid(sfid)
        instruments = {}
        for i in range(max_bank):
            current_bank = {}
            for j in range(max_preset):
                try:
                    if preset_mode == 0:
                        current_name = self.get_instrument_name(
                            sfid=sfid, bank=i, preset=j, hide_warnings=False)
                    else:
                        current_name = self.get_instrument_name(
                            bank=i, preset=j, hide_warnings=False)
                    if current_name:
                        current_bank[j] = current_name
                except:
                    pass
            if current_bank:
                instruments[i] = current_bank
        if preset_mode == 1:
            if sfid is not None:
                self.change_sfid(current_sfid)
        if hide_warnings:
            reset_capture(capture)
        return instruments

    def channel_info(self, channel=None):
        if channel is None:
            channel = self.current_channel
        return self.synth.program_info(channel)

    def get_preset_name(self, channel=None):
        if channel is None:
            channel = self.current_channel
        if self.valid_channel(channel):
            return self.synth.channel_info(channel)[3]

    def get_preset(self, channel=None):
        if channel is None:
            channel = self.current_channel
        return self.synth.program_info(channel)[2]

    def get_bank(self, channel=None):
        if channel is None:
            channel = self.current_channel
        return self.synth.program_info(channel)[1]

    def get_sfid(self, channel=None):
        if channel is None:
            channel = self.current_channel
        return self.synth.program_info(channel)[0]

    def init_channel(self, channel):
        self.synth.sfont_select(channel, self.sfid_list[0])
        self.find_channel_info(channel)

    def export_note(self,
                    note_name,
                    duration=2,
                    decay=1,
                    volume=100,
                    channel=0,
                    start_time=0,
                    sample_width=2,
                    channels=2,
                    frame_rate=44100,
                    name=None,
                    format='wav',
                    get_audio=False,
                    effects=None,
                    bpm=80,
                    export_args={}):
        whole_arrays = []
        if not isinstance(note_name, mp.note):
            current_note = mp.N(note_name)
        else:
            current_note = note_name
        note_name = current_note.degree
        if start_time > 0:
            whole_arrays.append(
                self.synth.get_samples(int(frame_rate * start_time)))
        self.synth.noteon(channel, note_name, volume)
        whole_arrays.append(self.synth.get_samples(int(frame_rate * duration)))
        self.synth.noteoff(channel, note_name)
        whole_arrays.append(self.synth.get_samples(int(frame_rate * decay)))
        audio_array = numpy.concatenate(whole_arrays, axis=None)
        current_samples = fluidsynth.raw_audio_string(audio_array)
        current_audio = AudioSegment.from_raw(BytesIO(current_samples),
                                              sample_width=sample_width,
                                              channels=2,
                                              frame_rate=frame_rate)
        if channels == 1:
            current_audio = current_audio.set_channels(1)
        self.synth.get_samples(int(frame_rate))
        if effects:
            current_audio = process_effect(current_audio, effects, bpm=bpm)
        elif check_effect(current_note):
            current_audio = process_effect(current_audio,
                                           current_note.effects,
                                           bpm=bpm)
        if name is None:
            name = f'{current_note}.{format}'
        if not get_audio:
            current_audio.export(name, format=format, **export_args)
        else:
            return current_audio

    def export_chord(self,
                     current_chord,
                     decay=0.5,
                     channel=0,
                     start_time=0,
                     piece_start_time=0,
                     sample_width=2,
                     channels=2,
                     frame_rate=44100,
                     name=None,
                     format='wav',
                     bpm=80,
                     get_audio=False,
                     fixed_decay=True,
                     effects=None,
                     pan=None,
                     volume=None,
                     length=None,
                     extra_length=None,
                     export_args={}):
        if fixed_decay:
            if not isinstance(decay, list):
                decay = real_time_to_bar(decay * 1000, bpm)
            else:
                decay = [real_time_to_bar(i * 1000, bpm) for i in decay]
        whole_length = bar_to_real_time(current_chord.bars(), bpm, 1) / 1000
        whole_length_with_decay = bar_to_real_time(
            apply_fadeout(current_chord, decay, fixed_decay).bars(), bpm,
            1) / 1000
        current_chord = copy(current_chord)
        current_chord.normalize_tempo(bpm=bpm)
        if piece_start_time != 0:
            current_chord.apply_start_time_to_changes(-piece_start_time,
                                                      msg=True)
            if pan:
                pan = copy(pan)
                for each in pan:
                    each.start_time -= piece_start_time
                    if each.start_time < 1:
                        each.start_time = 1
            if volume:
                volume = copy(volume)
                for each in volume:
                    each.start_time -= piece_start_time
                    if each.start_time < 1:
                        each.start_time = 1

        current_timestamps = get_timestamps(current_chord,
                                            bpm,
                                            pan=pan,
                                            volume=volume)
        current_timestamps_length = len(current_timestamps)
        if length:
            current_whole_length = length * 1000
        else:
            current_whole_length = (start_time +
                                    whole_length_with_decay) * 1000
            if extra_length:
                current_whole_length += extra_length * 1000
        current_silent_audio = AudioSegment.silent(
            duration=current_whole_length)

        channel_dict = {}

        for i in range(current_timestamps_length):
            current = current_timestamps[i]
            each = current.value
            if current.event_type == 'noteon' and (check_effect(each)
                                                   or hasattr(each, 'decay')):
                current_note_decay = getattr(each, 'decay', 1)
                current_note_audio = self.export_note(
                    each,
                    duration=bar_to_real_time(each.duration, bpm, 1) / 1000,
                    decay=current_note_decay,
                    volume=each.volume,
                    channel=channel,
                    start_time=0,
                    sample_width=sample_width,
                    channels=channels,
                    frame_rate=frame_rate,
                    format=format,
                    get_audio=True,
                    effects=getattr(each, 'effects', None),
                    bpm=bpm)
                current_silent_audio = current_silent_audio.overlay(
                    current_note_audio,
                    position=(start_time + current.start_time) * 1000)

        whole_arrays = []
        if start_time > 0:
            whole_arrays.append(
                self.synth.get_samples(int(frame_rate * start_time)))
        for k in range(current_timestamps_length):
            current = current_timestamps[k]
            each = current.value
            if current.event_type == 'noteon':
                if not check_effect(each):
                    current_channel = each.channel if each.channel is not None else channel
                    self.synth.noteon(current_channel, each.degree,
                                      each.volume)
            elif current.event_type == 'noteoff':
                if not check_effect(each):
                    current_channel = each.channel if each.channel is not None else channel
                    self.synth.noteoff(current_channel, each.degree)
            elif current.event_type == 'pitch_bend':
                current_channel = each.channel if each.channel is not None else channel
                self.synth.pitch_bend(current_channel, each.value)
            elif current.event_type == 'message':
                if each.type == 'control_change':
                    current_channel = each.channel if each.channel is not None else channel
                    if each.control == 0 and current_channel not in channel_dict:
                        channel_dict[current_channel] = self.channel_info(
                            current_channel)
                    self.synth.cc(current_channel, each.control, each.value)
                elif each.type == 'program_change':
                    current_channel = each.channel if each.channel is not None else channel
                    if not self.valid_channel(current_channel):
                        self.change_sfid(self.sfid_list[0], current_channel)
                    if current_channel not in channel_dict:
                        channel_dict[current_channel] = self.channel_info(
                            current_channel)
                    current_channel_info = self.synth.program_info(
                        current_channel)
                    self.synth.program_change(current_channel, each.program)
                    self.synth.program_select(current_channel,
                                              current_channel_info[0],
                                              current_channel_info[1],
                                              each.program)
            if k != current_timestamps_length - 1:
                append_time = current_timestamps[
                    k + 1].start_time - current.start_time
                whole_arrays.append(
                    self.synth.get_samples(int(frame_rate * append_time)))
        remain_times = whole_length_with_decay - whole_length
        if remain_times > 0:
            whole_arrays.append(
                self.synth.get_samples(int(frame_rate * remain_times)))

        audio_array = numpy.concatenate(whole_arrays, axis=None)
        current_samples = fluidsynth.raw_audio_string(audio_array)
        current_audio = AudioSegment.from_raw(BytesIO(current_samples),
                                              sample_width=sample_width,
                                              channels=2,
                                              frame_rate=frame_rate)
        if channels == 1:
            current_audio = current_audio.set_channels(1)
        current_silent_audio = current_silent_audio.overlay(current_audio)
        self.synth.get_samples(int(frame_rate))
        if effects:
            current_silent_audio = process_effect(current_silent_audio,
                                                  effects,
                                                  bpm=bpm)
        elif check_effect(current_chord):
            current_silent_audio = process_effect(current_silent_audio,
                                                  current_chord.effects,
                                                  bpm=bpm)

        self.set_channel_info(channel_dict)
        if name is None:
            name = f'Untitled.{format}'
        if not get_audio:
            current_silent_audio.export(name, format=format, **export_args)
        else:
            return current_silent_audio

    def export_piece(self,
                     current_chord,
                     decay=0.5,
                     sample_width=2,
                     channels=2,
                     frame_rate=44100,
                     name=None,
                     format='wav',
                     get_audio=False,
                     fixed_decay=True,
                     effects=None,
                     clear_program_change=False,
                     length=None,
                     extra_length=None,
                     track_lengths=None,
                     track_extra_lengths=None,
                     export_args={},
                     show_msg=False):
        decay_is_list = (isinstance(decay, list))
        current_chord = copy(current_chord)
        current_chord.normalize_tempo()
        current_chord.apply_start_time_to_changes(
            [-i for i in current_chord.start_times], msg=True, pan_volume=True)
        bpm = current_chord.bpm
        if clear_program_change:
            current_chord.clear_program_change()
        if length:
            whole_duration = length * 1000
        else:
            whole_duration = apply_fadeout(current_chord, decay,
                                           fixed_decay).eval_time(
                                               bpm, mode='number') * 1000
            if extra_length:
                whole_duration += extra_length * 1000
        silent_audio = AudioSegment.silent(duration=whole_duration)
        track_number = len(current_chord.tracks)
        for i in range(track_number):
            if show_msg:
                print(f'rendering track {i+1}/{track_number} ...')
            each = current_chord.tracks[i]
            current_start_time = bar_to_real_time(current_chord.start_times[i],
                                                  bpm, 1)
            current_pan = current_chord.pan[i]
            current_volume = current_chord.volume[i]
            current_instrument = current_chord.instruments_numbers[i]
            # instrument of a track of the piece type could be preset or [preset, bank, (sfid)]
            current_channel = current_chord.channels[
                i] if current_chord.channels else i
            current_sfid, current_bank, current_preset = self.channel_info(
                current_channel)
            if current_sfid == 0:
                self.change_sfid(self.sfid_list[0], current_channel)
                current_sfid, current_bank, current_preset = self.channel_info(
                    current_channel)
            if isinstance(current_instrument, int):
                current_instrument = [current_instrument - 1, current_bank]
            else:
                current_instrument = [current_instrument[0] - 1
                                      ] + current_instrument[1:]
            self.change(channel=current_channel,
                        sfid=(current_instrument[2]
                              if len(current_instrument) > 2 else None),
                        bank=current_instrument[1],
                        preset=current_instrument[0],
                        mode=1)
            current_audio = self.export_chord(
                each, decay if not decay_is_list else decay[i],
                current_channel, 0, 0, sample_width, channels, frame_rate,
                None, format, bpm, True, fixed_decay,
                each.effects if check_effect(each) else None, current_pan,
                current_volume,
                None if not track_lengths else track_lengths[i],
                None if not track_extra_lengths else track_extra_lengths[i])
            silent_audio = silent_audio.overlay(current_audio,
                                                position=current_start_time)
            self.change(current_channel,
                        current_sfid,
                        current_bank,
                        current_preset,
                        mode=1)
        self.synth.get_samples(int(frame_rate))
        if effects:
            silent_audio = process_effect(silent_audio, effects, bpm=bpm)
        elif check_effect(current_chord):
            silent_audio = process_effect(silent_audio,
                                          current_chord.effects,
                                          bpm=bpm)

        if show_msg:
            print('rendering finished')
        if name is None:
            name = f'Untitled.{format}'
        if not get_audio:
            silent_audio.export(name, format=format, **export_args)
        else:
            return silent_audio

    def export_midi_file(self,
                         current_chord,
                         decay=0.5,
                         sample_width=2,
                         channels=2,
                         frame_rate=44100,
                         name=None,
                         format='wav',
                         get_audio=False,
                         fixed_decay=True,
                         effects=None,
                         clear_program_change=False,
                         instruments=None,
                         length=None,
                         extra_length=None,
                         track_lengths=None,
                         track_extra_lengths=None,
                         export_args={},
                         show_msg=False,
                         **read_args):
        current_chord = mp.read(current_chord, **read_args)
        if instruments:
            current_chord.change_instruments(instruments)
        result = self.export_piece(current_chord, decay, sample_width,
                                   channels, frame_rate, name, format, True,
                                   fixed_decay, effects, clear_program_change,
                                   length, extra_length, track_lengths,
                                   track_extra_lengths, export_args, show_msg)

        if name is None:
            name = f'Untitled.{format}'
        if not get_audio:
            result.export(name, format=format, **export_args)
        else:
            return result

    def play_note(self,
                  note_name,
                  duration=2,
                  decay=1,
                  volume=100,
                  channel=0,
                  start_time=0,
                  sample_width=2,
                  channels=2,
                  frame_rate=44100,
                  name=None,
                  format='wav',
                  effects=None,
                  bpm=80,
                  export_args={},
                  wait=False):
        current_audio = self.export_note(note_name, duration, decay, volume,
                                         channel, start_time, sample_width,
                                         channels, frame_rate, name, format,
                                         True, effects, bpm, export_args)
        play_sound(current_audio, wait=wait)

    def play_chord(self,
                   current_chord,
                   decay=0.5,
                   channel=0,
                   start_time=0,
                   piece_start_time=0,
                   sample_width=2,
                   channels=2,
                   frame_rate=44100,
                   name=None,
                   format='wav',
                   bpm=80,
                   fixed_decay=True,
                   effects=None,
                   pan=None,
                   volume=None,
                   length=None,
                   extra_length=None,
                   export_args={},
                   wait=False):
        current_audio = self.export_chord(current_chord, decay, channel,
                                          start_time, piece_start_time,
                                          sample_width, channels, frame_rate,
                                          name, format, bpm, True, fixed_decay,
                                          effects, pan, volume, length,
                                          extra_length, export_args)
        play_sound(current_audio, wait=wait)

    def play_piece(self,
                   current_chord,
                   decay=0.5,
                   sample_width=2,
                   channels=2,
                   frame_rate=44100,
                   name=None,
                   format='wav',
                   fixed_decay=True,
                   effects=None,
                   clear_program_change=False,
                   length=None,
                   extra_length=None,
                   track_lengths=None,
                   track_extra_lengths=None,
                   export_args={},
                   show_msg=False,
                   wait=False):
        current_audio = self.export_piece(
            current_chord, decay, sample_width, channels, frame_rate, name,
            format, True, fixed_decay, effects, clear_program_change, length,
            extra_length, track_lengths, track_extra_lengths, export_args,
            show_msg)
        play_sound(current_audio, wait=wait)

    def play_midi_file(self,
                       current_chord,
                       decay=0.5,
                       sample_width=2,
                       channels=2,
                       frame_rate=44100,
                       name=None,
                       format='wav',
                       fixed_decay=True,
                       effects=None,
                       clear_program_change=False,
                       instruments=None,
                       length=None,
                       extra_length=None,
                       track_lengths=None,
                       track_extra_lengths=None,
                       export_args={},
                       show_msg=False,
                       wait=False,
                       **read_args):
        current_audio = self.export_midi_file(
            current_chord, decay, sample_width, channels, frame_rate, name,
            format, True, fixed_decay, effects, clear_program_change,
            instruments, length, extra_length, track_lengths,
            track_extra_lengths, export_args, show_msg, **read_args)
        play_sound(current_audio, wait=wait)

    def export_sound_modules(self,
                             channel=None,
                             sfid=None,
                             bank=None,
                             preset=None,
                             start='A0',
                             stop='C8',
                             duration=6,
                             decay=1,
                             volume=127,
                             sample_width=2,
                             channels=2,
                             frame_rate=44100,
                             format='wav',
                             folder_name='Untitled',
                             effects=None,
                             bpm=80,
                             name=None,
                             show_full_path=False,
                             export_args={}):
        try:
            os.mkdir(folder_name)
            os.chdir(folder_name)
        except:
            os.chdir(folder_name)
        current_channel = copy(self.current_channel)
        current_sfid = copy(self.current_sfid)
        current_bank = copy(self.current_bank)
        current_preset = copy(self.current_preset)
        self.change(channel, sfid, bank, preset)
        if not isinstance(start, mp.note):
            start = mp.N(start)
        if not isinstance(stop, mp.note):
            stop = mp.N(stop)
        current_sf2 = self.file[self.sfid_list.index(self.current_sfid)]
        if not show_full_path:
            current_sf2 = os.path.basename(current_sf2)
        for i in range(start.degree, stop.degree + 1):
            current_note = str(mp.degree_to_note(i))
            if name is None:
                current_name = None
            else:
                if isinstance(name, list):
                    current_name = name[i] + f'.{format}'
                else:
                    current_name = name(str(current_note)) + f'.{format}'
            print(
                f'exporting {current_note} of {current_sf2}, bank {self.current_bank}, preset {self.current_preset}'
            )
            self.export_note(current_note,
                             duration=duration,
                             decay=decay,
                             volume=volume,
                             channel=self.current_channel,
                             sample_width=sample_width,
                             channels=channels,
                             frame_rate=frame_rate,
                             format=format,
                             effects=effects,
                             bpm=bpm,
                             name=current_name,
                             export_args=export_args)
        print('exporting finished')
        self.change(current_channel, current_sfid, current_bank,
                    current_preset)

    def load(self, file):
        capture = get_capture()
        try:
            current_sfid = self.synth.sfload(file)
        except:
            reset_capture(capture)
            raise ValueError('Invalid SoundFont file')
        if current_sfid == -1:
            reset_capture(capture)
            raise ValueError('Invalid SoundFont file')
        reset_capture(capture)
        self.sfid_list.append(current_sfid)
        self.file.append(file)
        if len(self.file) == 1:
            self.synth.system_reset()
            self.change_channel(0)

    def unload(self, ind):
        if ind > 0:
            ind -= 1
        del self.file[ind]
        current_sfid = self.sfid_list[ind]
        self.synth.sfunload(current_sfid)
        del self.sfid_list[ind]

    def set_channel_info(self, channel_dict):
        for each, value in channel_dict.items():
            self.change(each, *value, mode=1)

    def valid_channel(self, channel):
        return self.synth.program_info(channel)[0] != 0

    def reset_all_channels(self):
        self.synth.system_reset()
        self.current_sfid, self.current_bank, self.current_preset = self.channel_info(
        )

    def pause(self):
        mp.pygame.mixer.pause()

    def unpause(self):
        mp.pygame.mixer.unpause()

    def stop(self):
        mp.pygame.mixer.stop()


class sf2_player:

    def __init__(self, file=None):
        self.file = []
        self.synth = fluidsynth.Synth()
        self.apply_synth_settings()
        self.sfid_list = []
        self.playing = False
        if file:
            self.load(file)
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            self.default_audio_driver = 'dsound'
        elif sys.platform == 'linux':
            self.default_audio_driver = 'alsa'
        elif sys.platform == 'darwin':
            self.default_audio_driver = 'coreaudio'
        else:
            self.default_audio_driver = None
        if self.default_audio_driver:
            self.synth.setting('audio.driver', self.default_audio_driver)

    def __repr__(self):
        return f'''[soundfont player]
loaded soundfonts: {self.file}
soundfonts id: {self.sfid_list}'''

    def load(self, file):
        capture = get_capture()
        try:
            current_sfid = self.synth.sfload(file)
        except:
            reset_capture(capture)
            raise ValueError('Invalid SoundFont file')
        if current_sfid == -1:
            reset_capture(capture)
            raise ValueError('Invalid SoundFont file')
        self.synth.system_reset()
        reset_capture(capture)
        self.sfid_list.append(current_sfid)
        self.file.append(file)

    def unload(self, ind):
        if ind > 0:
            ind -= 1
        del self.file[ind]
        current_sfid = self.sfid_list[ind]
        self.synth.sfunload(current_sfid)
        del self.sfid_list[ind]

    def change_setting(self, parameter, value):
        self.synth.setting(f'synth.{parameter}', value)

    def apply_synth_settings(self):
        self.change_setting('gain', 0.2)
        self.change_setting('reverb.active', 0)
        reverb_parameters = ['damp', 'level', 'room-size', 'width']
        current_reverb_values = [0.0, 0.9, 0.2, 0.5]
        chorus_parameters = ['depth', 'level', 'nr', 'speed']
        current_chorus_values = [8.0, 2.0, 3, 0.3]
        for i, each in enumerate(reverb_parameters):
            self.change_setting(f'reverb.{each}', current_reverb_values[i])
        self.change_setting('chorus.active', 0)
        for i, each in enumerate(chorus_parameters):
            self.change_setting(f'chorus.{each}', current_chorus_values[i])

    def play_midi_file(self, filename):
        if not self.synth.midi_driver:
            self.synth.start()
        if self.playing:
            self.synth.play_midi_stop()
        self.synth.play_midi_file(filename)
        self.playing = True

    def pause(self):
        if self.playing:
            self.synth.play_midi_pause()

    def unpause(self):
        if self.playing:
            self.synth.play_midi_unpause()

    def stop(self):
        if self.playing:
            self.synth.play_midi_stop()
            self.playing = False

    def set_tempo(self, bpm, tempo_type=1):
        if fluidsynth.fluid_player_set_tempo:
            self.synth.player_set_tempo(tempo_type, bpm)

    def set_default_audio_driver(self, driver):
        self.default_audio_driver = driver
        if self.default_audio_driver:
            self.synth.setting('audio.driver', self.default_audio_driver)

    def set_pos(self, ticks):
        self.synth.player_seek(ticks)

    def get_current_tick(self):
        return self.synth.get_current_tick()

    def get_total_ticks(self):
        return self.synth.get_total_ticks()

    def get_current_tempo(self):
        return self.synth.get_current_tempo()

    def get_current_bpm(self):
        return self.synth.get_current_bpm()

    def get_status(self):
        return self.synth.get_status()


reverse = effect(lambda s: s.reverse(), 'reverse')
offset = effect(lambda s, bar, bpm: s[bar_to_real_time(bar, bpm, 1):],
                'offset',
                unknown_args={'bpm': None})
fade_in = effect(lambda s, duration: s.fade_in(duration), 'fade in')
fade_out = effect(lambda s, duration: s.fade_out(duration), 'fade out')
fade = effect(
    lambda s, duration1, duration2=0: s.fade_in(duration1).fade_out(duration2),
    'fade')
adsr = effect(adsr_func, 'adsr')
