from musicpy import *
from difflib import SequenceMatcher

# database

INTERVAL = {
    0: '纯一度',
    1: '小二度',
    2: '大二度',
    3: '小三度',
    4: '大三度',
    5: '纯四度',
    6: '减五度',
    7: '纯五度',
    8: '小六度',
    9: '大六度',
    10: '小七度',
    11: '大七度',
    12: '纯八度',
    13: '小九度',
    14: '大九度',
    17: '纯十一度',
    20: '小十三度',
    21: '大十三度'
}

chordTypes = database.match({
    ('大三和弦', 'major', 'M', 'maj', 'majorthird'): ((4, 7), ),
    ('小三和弦', 'minor', 'm', 'minorthird', 'min', '-'): ((3, 7), ),
    ('大七和弦', 'maj7', 'M7', 'major7th', 'majorseventh'): ((4, 7, 11), ),
    ('小七和弦', 'm7', 'min7', 'minor7th', 'minorseventh', '-7'): ((3, 7, 10), ),
    ('属七和弦(大小七和弦)', '7', 'dom7', 'dominant7', 'germansixth'): ((4, 7, 10), ),
    ('小大七和弦', 'minormajor7', 'minor major 7', 'mM7'): ((3, 7, 11), ),
    ('减三和弦', 'dim', 'o'): ((3, 6), ),
    ('减七和弦', 'dim7', 'o7'): ((3, 6, 9), ),
    ('半减七和弦', 'half-diminished7', 'ø7', 'ø', 'half-diminished', 'm7b5'):
    ((3, 6, 10), ),
    ('增三和弦', 'aug', 'augmented', '+', 'aug3', '+3'): ((4, 8), ),
    ('增七和弦', 'aug7', 'augmented7', '+7'): ((4, 8, 10), ),
    ('增大七和弦', 'augmaj7', 'augmented-major7', '+maj7', 'augM7'): ((4, 8, 11), ),
    ('意大利增六和弦', 'aug6', 'augmented6', '+6', 'italian-sixth'): ((4, 10), ),
    (
        '法国增六和弦',
        'frenchsixth',
    ): ((4, 6, 10), ),
    ('增九和弦', 'aug9', '+9'): ((4, 8, 10, 14), ),
    ('挂四和弦', 'sus', 'sus4'): ((5, 7), ),
    (
        '挂二和弦',
        'sus2',
    ): ((2, 7), ),
    ('属九和弦', '9', 'dominant9', 'dominant-ninth', 'ninth'): ((4, 7, 10, 14), ),
    ('大九和弦', 'maj9', 'major-ninth', 'major9th', 'M9'): ((4, 7, 11, 14), ),
    ('小九和弦', 'm9', 'minor9', 'minor9th', '-9'): ((3, 7, 10, 14), ),
    ('增大九和弦', 'augmaj9', '+maj9', '+M9', 'augM9'): ((4, 8, 11, 14), ),
    ('大六和弦', 'add6', '6', 'sixth'): ((4, 7, 9), ),
    ('小六和弦', 'm6', 'minorsixth'): ((3, 7, 9), ),
    ('加二和弦', 'add2', '+2'): ((2, 4, 7), ),
    (
        '加九和弦',
        'add9',
    ): ((4, 7, 14), ),
    ('加小二和弦', 'madd2', 'm+2'): ((2, 3, 7), ),
    (
        '加小九和弦',
        'madd9',
    ): ((3, 7, 14), ),
    ('属七挂四和弦', '7sus4', '7sus'): ((5, 7, 10), ),
    (
        '属七挂二和弦',
        '7sus2',
    ): ((2, 7, 10), ),
    ('大七挂四和弦', 'maj7sus4', 'maj7sus', 'M7sus4'): ((5, 7, 11), ),
    ('大七挂二和弦', 'maj7sus2', 'M7sus2'): ((2, 7, 11), ),
    ('属九挂四和弦', '9sus4', '9sus'): ((5, 7, 10, 14), ),
    (
        '属九挂二和弦',
        '9sus2',
    ): ((2, 7, 10, 14), ),
    ('大九挂四和弦', 'maj9sus4', 'maj9sus', 'M9sus', 'M9sus4'): ((5, 7, 11, 14), ),
    ('属十三挂四和弦', '13sus4', '13sus'): ((5, 7, 10, 14, 21), (7, 10, 14, 17, 21)),
    (
        '属十三挂二和弦',
        '13sus2',
    ): ((2, 7, 10, 17, 21), ),
    ('大十三挂四和弦', 'maj13sus4', 'maj13sus', 'M13sus', 'M13sus4'):
    ((5, 7, 11, 14, 21), (7, 11, 14, 17, 21)),
    ('大十三挂二和弦', 'maj13sus2', 'M13sus2'): ((2, 7, 11, 17, 21), ),
    ('加四和弦', 'add4', '+4'): ((4, 5, 7), ),
    ('加小四和弦', 'madd4', 'm+4'): ((3, 5, 7), ),
    ('大七降五和弦', 'maj7b5', 'M7b5'): ((4, 6, 11), ),
    ('大七升十一和弦', 'maj7#11', 'M7#11'): ((4, 7, 11, 18), ),
    ('大九升十一和弦', 'maj9#11', 'M9#11'): ((4, 7, 11, 14, 18), ),
    ('六九和弦', '69', '6/9', 'add69'): ((4, 7, 9, 14), ),
    ('小六九和弦', 'm69', 'madd69'): ((3, 7, 9, 14), ),
    ('大六挂四和弦', '6sus4', '6sus'): ((5, 7, 9), ),
    (
        '大六挂二和弦',
        '6sus2',
    ): ((2, 7, 9), ),
    ('强力和弦(五度和弦)', '5', 'power chord'): ((7, ), ),
    ('强力和弦(五度八度和弦)', '5(+octave)', 'power chord(with octave)'): ((7, 12), ),
    ('大十一和弦', 'maj11', 'M11', 'eleventh', 'major 11'): ((4, 7, 11, 14, 17), ),
    ('小十一和弦', 'm11', 'minor eleventh', 'minor 11'): ((3, 7, 10, 14, 17), ),
    ('属十一和弦', '11', 'dominant11', 'dominant 11'): ((4, 7, 10, 14, 17), ),
    ('属十三和弦', '13', 'dominant13', 'dominant 13'): ((4, 7, 10, 14, 17, 21), ),
    ('大十三和弦', 'maj13', 'major 13', 'M13'): ((4, 7, 11, 14, 17, 21), ),
    ('小十三和弦', 'm13', 'minor 13'): ((3, 7, 10, 14, 17, 21), ),
    ('大七升十一和弦', 'maj13#11', 'M13#11'): ((4, 7, 11, 14, 18, 21), ),
    (
        '属十三升十一和弦',
        '13#11',
    ): ((4, 7, 10, 14, 18, 21), ),
    (
        '五度加九和弦',
        'fifth 9th',
    ): ((7, 14), ),
    ('小大九和弦', 'minormajor9', 'minor major 9', 'mM9'): ((3, 7, 11, 14), ),
    ('减大七和弦', 'dim(Maj7)'): ((3, 6, 11), )
})

detectTypes = chordTypes.reverse()

# musicpy


def inversion_from(a, b, num=False, mode=0):
    N = len(b)
    for i in range(1, N):
        temp = b.inversion(i)
        if [x.name for x in temp.notes] == [y.name for y in a.notes]:
            return f'/{a[0].name}' if not num else f'第{i}转位'
    return f'could not get chord {a.notes} from a single inversion of chord {b.notes}, you could try sort_from' if mode == 0 else None


def sort_from(a, b, getorder=False):
    names = [i.name for i in b]
    try:
        order = [names.index(j.name) + 1 for j in a]
        return f'{b.notes} 排序 {order}' if not getorder else order
    except:
        return


def omit_from(a, b, showls=False, alter_notes_show_degree=False):
    a_notes = a.names()
    b_notes = b.names()
    omitnotes = list(set(b_notes) - set(a_notes))
    if alter_notes_show_degree:
        b_first_note = b[0].degree
        omitnotes_degree = []
        for j in omitnotes:
            current = database.reverse_degree_match[b[b_notes.index(j)].degree
                                                    - b_first_note]
            if current == 'not found':
                omitnotes_degree.append(j)
            else:
                omitnotes_degree.append(current)
        omitnotes = omitnotes_degree
    if showls:
        result = omitnotes
    else:
        result = f"省略 {', '.join(omitnotes)}"
        order_omit = chord([x for x in b_notes if x in a_notes])
        if order_omit.names() != a.names():
            result += ' ' + inversion_way(a, order_omit)
    return result


def change_from(a,
                b,
                octave_a=False,
                octave_b=False,
                same_degree=True,
                alter_notes_show_degree=False):
    '''
    how a is changed from b (flat or sharp some notes of b to get a)
    this is used only when two chords have the same number of notes
    in the detect chord function
    '''
    if octave_a:
        a = a.inoctave()
    if octave_b:
        b = b.inoctave()
    if same_degree:
        b = b.down(12 * (b[0].num - a[0].num))
    N = min(len(a), len(b))
    anotes = [x.degree for x in a.notes]
    bnotes = [x.degree for x in b.notes]
    anames = a.names()
    bnames = b.names()
    M = min(len(anotes), len(bnotes))
    changes = [(bnames[i], bnotes[i] - anotes[i]) for i in range(M)]
    changes = [x for x in changes if x[1] != 0]
    if any(abs(j[1]) != 1 for j in changes):
        changes = []
    else:
        if not alter_notes_show_degree:
            changes = [f'b{j[0]}' if j[1] > 0 else f'#{j[0]}' for j in changes]
        else:
            b_first_note = b[0].degree
            for i in range(len(changes)):
                note_name, note_change = changes[i]
                current_degree = database.reverse_degree_match[
                    bnotes[bnames.index(note_name)] - b_first_note]
                if current_degree == 'not found':
                    current_degree = note_name
                if note_change > 0:
                    changes[i] = f'b{current_degree}'
                else:
                    changes[i] = f'#{current_degree}'

    return ', '.join(changes)


def contains(a, b):
    '''
    if b contains a (notes), in other words,
    all of a's notes is inside b's notes
    '''
    return set(a.names()) < set(b.names()) and len(a) < len(b)


def inversion_way(a, b, inv_num=False, chordtype=None, only_msg=False):
    if samenotes(a, b):
        return f'{b[0].name}{chordtype}'
    if samenote_set(a, b):
        inversion_msg = inversion_from(
            a, b, mode=1) if not inv_num else inversion_from(
                a, b, num=True, mode=1)
        if inversion_msg is not None:
            if not only_msg:
                if chordtype is not None:
                    return f'{b[0].name}{chordtype}{inversion_msg}' if not inv_num else f'{b[0].name}{chordtype} {inversion_msg}'
                else:
                    return inversion_msg
            else:
                return inversion_msg
        else:
            sort_msg = sort_from(a, b, getorder=True)
            if sort_msg is not None:
                if not only_msg:
                    if chordtype is not None:
                        return f'{b[0].name}{chordtype} 排序 {sort_msg}'
                    else:
                        return f'排序 {sort_msg}'
                else:
                    return f'排序 {sort_msg}'
            else:
                return f'a voicing of {b[0].name}{chordtype}'
    else:
        return 'not good'


def samenotes(a, b):
    return a.names() == b.names()


def samenote_set(a, b):
    return set(a.names()) == set(b.names())


def find_similarity(a,
                    b=None,
                    only_ratio=False,
                    fromchord_name=True,
                    getgoodchord=False,
                    listall=False,
                    ratio_and_chord=False,
                    ratio_chordname=False,
                    provide_name=None,
                    result_ratio=False,
                    get_types=False,
                    change_from_first=False,
                    same_note_special=True,
                    alter_notes_show_degree=False):
    result = ''
    types = None
    if b is None:
        wholeTypes = chordTypes.keynames()
        selfname = a.names()
        rootnote = a[0]
        possible_chords = [(chd(rootnote, i), i) for i in wholeTypes]
        lengths = len(possible_chords)
        if same_note_special:
            ratios = [(1 if samenote_set(a, x[0]) else SequenceMatcher(
                None, selfname, x[0].names()).ratio(), x[1])
                      for x in possible_chords]
        else:
            ratios = [(SequenceMatcher(None, selfname,
                                       x[0].names()).ratio(), x[1])
                      for x in possible_chords]
        alen = len(a)
        ratios_temp = [
            ratios[k] for k in range(len(ratios))
            if len(possible_chords[k][0]) >= alen
        ]
        if len(ratios_temp) != 0:
            ratios = ratios_temp
        ratios.sort(key=lambda x: x[0], reverse=True)
        if listall:
            return ratios
        if only_ratio:
            return ratios[0]
        first = ratios[0]
        highest = first[0]
        chordfrom = possible_chords[wholeTypes.index(first[1])][0]
        if ratio_and_chord:
            if ratio_chordname:
                return first, chordfrom
            return highest, chordfrom
        if highest > 0.6:
            if change_from_first:
                result = find_similarity(
                    a,
                    chordfrom,
                    fromchord_name=False,
                    alter_notes_show_degree=alter_notes_show_degree)
                cff_ind = 0
                while result == 'not good':
                    cff_ind += 1
                    try:
                        first = ratios[cff_ind]
                    except:
                        first = ratios[0]
                        highest = first[0]
                        chordfrom = possible_chords[wholeTypes.index(
                            first[1])][0]
                        result = ''
                        break
                    highest = first[0]
                    chordfrom = possible_chords[wholeTypes.index(first[1])][0]
                    if highest > 0.6:
                        result = find_similarity(
                            a,
                            chordfrom,
                            fromchord_name=False,
                            alter_notes_show_degree=alter_notes_show_degree)
                    else:
                        first = ratios[0]
                        highest = first[0]
                        chordfrom = possible_chords[wholeTypes.index(
                            first[1])][0]
                        result = ''
                        break
            if highest == 1:
                chordfrom_type = first[1]
                if samenotes(a, chordfrom):
                    result = f'{rootnote.name}{chordfrom_type}'
                    types = 'original'
                else:
                    if samenote_set(a, chordfrom):
                        result = inversion_from(a, chordfrom, mode=1)
                        types = 'inversion'
                        if result is None:
                            sort_message = sort_from(a,
                                                     chordfrom,
                                                     getorder=True)
                            if sort_message is None:
                                result = f'a voicing of the chord {rootnote.name}{chordfrom_type}'
                            else:
                                result = f'{rootnote.name}{chordfrom_type} 排序 {sort_message}'
                        else:
                            result = f'{rootnote.name}{chordfrom_type} {result}'
                    else:
                        return 'not good'
                if get_types:
                    result = [result, types]
                if result_ratio:
                    return (highest, result) if not getgoodchord else (
                        (highest,
                         result), chordfrom, f'{chordfrom[0].name}{first[1]}')
                return result if not getgoodchord else (
                    result, chordfrom, f'{chordfrom[0].name}{first[1]}')
            else:
                if samenote_set(a, chordfrom):
                    result = inversion_from(a, chordfrom, mode=1)
                    types = 'inversion'
                    if result is None:
                        sort_message = sort_from(a, chordfrom, getorder=True)
                        types = 'inversion'
                        if sort_message is None:
                            return f'a voicing of the chord {rootnote.name}{chordfrom_type}'
                        else:
                            result = f'排序 {sort_message}'
                elif contains(a, chordfrom):
                    result = omit_from(
                        a,
                        chordfrom,
                        alter_notes_show_degree=alter_notes_show_degree)
                    types = 'omit'
                elif len(a) == len(chordfrom):
                    result = change_from(
                        a,
                        chordfrom,
                        alter_notes_show_degree=alter_notes_show_degree)
                    types = 'change'
                if result == '':
                    return 'not good'

                if fromchord_name:
                    from_chord_names = f'{rootnote.name}{first[1]}'
                    result = f'{from_chord_names} {result}'
                if get_types:
                    result = [result, types]
                if result_ratio:
                    return (highest,
                            result) if not getgoodchord else ((highest,
                                                               result),
                                                              chordfrom,
                                                              from_chord_names)
                return result if not getgoodchord else (result, chordfrom,
                                                        from_chord_names)

        else:
            return 'not good'
    else:
        if samenotes(a, b):
            if fromchord_name:
                if provide_name != None:
                    bname = b[0].name + provide_name
                else:
                    bname = detect(
                        b,
                        change_from_first=change_from_first,
                        same_note_special=same_note_special,
                        alter_notes_show_degree=alter_notes_show_degree)
                return bname if not getgoodchord else (bname, chordfrom, bname)
            else:
                return 'same'
        if only_ratio or listall:
            return SequenceMatcher(None, a.names(), b.names()).ratio()
        chordfrom = b
        if samenote_set(a, chordfrom):
            result = inversion_from(a, chordfrom, mode=1)
            if result is None:
                sort_message = sort_from(a, chordfrom, getorder=True)
                if sort_message is None:
                    return f'a voicing of the chord {rootnote.name}{chordfrom_type}'
                else:
                    result = f'排序 {sort_message}'
        elif contains(a, chordfrom):
            result = omit_from(a,
                               chordfrom,
                               alter_notes_show_degree=alter_notes_show_degree)
        elif len(a) == len(chordfrom):
            result = change_from(
                a, chordfrom, alter_notes_show_degree=alter_notes_show_degree)
        if result == '':
            return 'not good'
        bname = None
        if fromchord_name:
            if provide_name != None:
                bname = b[0].name + provide_name
            else:
                bname = detect(b,
                               change_from_first=change_from_first,
                               same_note_special=same_note_special,
                               alter_notes_show_degree=alter_notes_show_degree)
            if isinstance(bname, list):
                bname = bname[0]
        return result if not getgoodchord else (result, chordfrom, bname)


def detect_variation(current_chord,
                     inv_num=False,
                     change_from_first=False,
                     original_first=False,
                     same_note_special=True,
                     N=None,
                     alter_notes_show_degree=False):
    for each in range(1, N):
        each_current = current_chord.inversion(each)
        each_detect = detect(each_current,
                             inv_num,
                             change_from_first,
                             original_first,
                             same_note_special,
                             whole_detect=False,
                             return_fromchord=True,
                             alter_notes_show_degree=alter_notes_show_degree)
        if each_detect is not None:
            detect_msg, change_from_chord, chord_name_str = each_detect
            inv_msg = inversion_way(current_chord, each_current, inv_num)
            result = f'{detect_msg} {inv_msg}'
            if any(x in detect_msg
                   for x in ['排序', '/']) and any(y in inv_msg
                                                 for y in ['排序', '/']):
                inv_msg = inversion_way(current_chord, change_from_chord,
                                        inv_num)
                if inv_msg == 'not good':
                    inv_msg = find_similarity(
                        current_chord,
                        change_from_chord,
                        alter_notes_show_degree=alter_notes_show_degree)
                result = f'{chord_name_str} {inv_msg}'
            return result
    for each2 in range(1, N):
        each_current = current_chord.inversion_highest(each2)
        each_detect = detect(each_current,
                             inv_num,
                             change_from_first,
                             original_first,
                             same_note_special,
                             whole_detect=False,
                             return_fromchord=True,
                             alter_notes_show_degree=alter_notes_show_degree)
        if each_detect is not None:
            detect_msg, change_from_chord, chord_name_str = each_detect
            inv_msg = inversion_way(current_chord, each_current, inv_num)
            result = f'{detect_msg} {inv_msg}'
            if any(x in detect_msg
                   for x in ['排序', '/']) and any(y in inv_msg
                                                 for y in ['排序', '/']):
                inv_msg = inversion_way(current_chord, change_from_chord,
                                        inv_num)
                if inv_msg == 'not good':
                    inv_msg = find_similarity(
                        current_chord,
                        change_from_chord,
                        alter_notes_show_degree=alter_notes_show_degree)
                result = f'{chord_name_str} {inv_msg}'
            return result


def detect_split(current_chord, N=None, **detect_args):
    if N < 6:
        splitind = 1
        lower = current_chord.notes[0].name
        upper = detect(current_chord.notes[splitind:], **detect_args)
        if isinstance(upper, list):
            upper = upper[0]
        return f'[{upper}]/{lower}'
    else:
        splitind = N // 2
        lower = detect(current_chord.notes[:splitind], **detect_args)
        upper = detect(current_chord.notes[splitind:], **detect_args)
        if isinstance(lower, list):
            lower = lower[0]
        if isinstance(upper, list):
            upper = upper[0]
        return f'[{upper}]/[{lower}]'


def interval_check(current_chord):
    times, dist = divmod(
        (current_chord.notes[1].degree - current_chord.notes[0].degree), 12)
    if times > 0:
        dist = 12 + dist
    if dist in INTERVAL:
        interval_name = INTERVAL[dist]
    else:
        interval_name = INTERVAL[dist % 12]
    root_note_name = current_chord[0].name
    if interval_name == '纯五度':
        return f'{root_note_name} 和 纯五度 / {root_note_name}5 ({root_note_name} 强力和弦)'
    return f'{root_note_name} 和 {interval_name}'


def detect(current_chord,
           inv_num=False,
           change_from_first=True,
           original_first=True,
           same_note_special=False,
           whole_detect=True,
           return_fromchord=False,
           poly_chord_first=False,
           root_position_return_first=True,
           alter_notes_show_degree=False):
    if not isinstance(current_chord, chord):
        current_chord = chord(current_chord)
    N = len(current_chord)
    if N == 1:
        return f'单音 {current_chord.notes[0]}'
    if N == 2:
        return interval_check(current_chord)
    current_chord = current_chord.standardize()
    N = len(current_chord)
    if N == 1:
        return f'单音 {current_chord.notes[0]}'
    if N == 2:
        return interval_check(current_chord)
    root = current_chord[0].degree
    rootNote = current_chord[0].name
    distance = tuple(i.degree - root for i in current_chord[1:])
    findTypes = detectTypes[distance]
    if findTypes != 'not found':
        return [
            rootNote + i for i in findTypes
        ] if not root_position_return_first else rootNote + findTypes[0]
    original_detect = find_similarity(
        current_chord,
        result_ratio=True,
        change_from_first=change_from_first,
        same_note_special=same_note_special,
        getgoodchord=return_fromchord,
        get_types=True,
        alter_notes_show_degree=alter_notes_show_degree)
    if original_detect != 'not good':
        if return_fromchord:
            original_ratio, original_msg = original_detect[0]
        else:
            original_ratio, original_msg = original_detect
        types = original_msg[1]
        original_msg = original_msg[0]
        if original_first:
            if original_ratio > 0.86 and types != 'change':
                return original_msg if not return_fromchord else (
                    original_msg, original_detect[1], original_detect[2])
        if original_ratio == 1:
            return original_msg if not return_fromchord else (
                original_msg, original_detect[1], original_detect[2])
    for i in range(1, N):
        current = chord(current_chord.inversion(i).names())
        root = current[0].degree
        distance = tuple(i.degree - root for i in current[1:])
        result1 = detectTypes[distance]
        if result1 != 'not found':
            inversion_result = inversion_way(current_chord, current, inv_num,
                                             result1[0])
            if '排序' in inversion_result:
                continue
            else:
                return inversion_result if not return_fromchord else (
                    inversion_result, current,
                    f'{current[0].name}{result1[0]}')
        else:
            current = current.inoctave()
            root = current[0].degree
            distance = tuple(i.degree - root for i in current[1:])
            result1 = detectTypes[distance]
            if result1 != 'not found':
                inversion_result = inversion_way(current_chord, current,
                                                 inv_num, result1[0])
                if '排序' in inversion_result:
                    continue
                else:
                    return inversion_result if not return_fromchord else (
                        inversion_result, current,
                        f'{current[0].name}{result1[0]}')
    for i in range(1, N):
        current = chord(current_chord.inversion_highest(i).names())
        root = current[0].degree
        distance = tuple(i.degree - root for i in current[1:])
        result1 = detectTypes[distance]
        if result1 != 'not found':
            inversion_high_result = inversion_way(current_chord, current,
                                                  inv_num, result1[0])
            if '排序' in inversion_high_result:
                continue
            else:
                return inversion_high_result if not return_fromchord else (
                    inversion_high_result, current,
                    f'{current[0].name}{result1[0]}')
        else:
            current = current.inoctave()
            root = current[0].degree
            distance = tuple(i.degree - root for i in current[1:])
            result1 = detectTypes[distance]
            if result1 != 'not found':
                inversion_high_result = inversion_way(current_chord, current,
                                                      inv_num, result1[0])
                if '排序' in inversion_high_result:
                    continue
                else:
                    return inversion_high_result if not return_fromchord else (
                        inversion_high_result, current,
                        f'{current[0].name}{result1[0]}')
    if poly_chord_first and N > 3:
        return detect_split(
            current_chord,
            N,
            inv_num=inv_num,
            change_from_first=change_from_first,
            original_first=original_first,
            same_note_special=same_note_special,
            whole_detect=whole_detect,
            return_fromchord=return_fromchord,
            poly_chord_first=poly_chord_first,
            root_position_return_first=root_position_return_first,
            alter_notes_show_degree=alter_notes_show_degree)
    inversion_final = True
    possibles = [
        (find_similarity(current_chord.inversion(j),
                         result_ratio=True,
                         change_from_first=change_from_first,
                         same_note_special=same_note_special,
                         getgoodchord=True,
                         alter_notes_show_degree=alter_notes_show_degree), j)
        for j in range(1, N)
    ]
    possibles = [x for x in possibles if x[0] != 'not good']
    if len(possibles) == 0:
        possibles = [
            (find_similarity(current_chord.inversion_highest(j),
                             result_ratio=True,
                             change_from_first=change_from_first,
                             same_note_special=same_note_special,
                             getgoodchord=True,
                             alter_notes_show_degree=alter_notes_show_degree),
             j) for j in range(1, N)
        ]
        possibles = [x for x in possibles if x[0] != 'not good']
        inversion_final = False
    if len(possibles) == 0:
        if original_detect != 'not good':
            return original_msg if not return_fromchord else (
                original_msg, original_detect[1], original_detect[2])
        if not whole_detect:
            return
        else:
            detect_var = detect_variation(current_chord, inv_num,
                                          change_from_first, original_first,
                                          same_note_special, N,
                                          alter_notes_show_degree)
            if detect_var is None:
                result_change = detect(
                    current_chord,
                    inv_num,
                    not change_from_first,
                    original_first,
                    same_note_special,
                    False,
                    return_fromchord,
                    alter_notes_show_degree=alter_notes_show_degree)
                if result_change is None:
                    return detect_split(
                        current_chord,
                        N,
                        inv_num=inv_num,
                        change_from_first=change_from_first,
                        original_first=original_first,
                        same_note_special=same_note_special,
                        whole_detect=whole_detect,
                        return_fromchord=return_fromchord,
                        poly_chord_first=poly_chord_first,
                        root_position_return_first=root_position_return_first,
                        alter_notes_show_degree=alter_notes_show_degree)
                else:
                    return result_change
            else:
                return detect_var
    possibles.sort(key=lambda x: x[0][0][0], reverse=True)
    best = possibles[0][0]
    highest_ratio, highest_msg = best[0]
    if original_detect != 'not good':
        if original_ratio > 0.6 and (original_ratio >= highest_ratio
                                     or '排序' in highest_msg):
            return original_msg if not return_fromchord else (
                original_msg, original_detect[1], original_detect[2])
    if highest_ratio > 0.6:
        if inversion_final:
            current_invert = current_chord.inversion(possibles[0][1])
        else:
            current_invert = current_chord.inversion_highest(possibles[0][1])
        invfrom_current_invert = inversion_way(current_chord, current_invert,
                                               inv_num)
        highest_msg = best[0][1]
        if any(x in highest_msg
               for x in ['排序', '/']) and any(y in invfrom_current_invert
                                             for y in ['排序', '/']):
            retry_msg = find_similarity(
                current_chord,
                best[1],
                fromchord_name=return_fromchord,
                getgoodchord=return_fromchord,
                alter_notes_show_degree=alter_notes_show_degree)
            if not return_fromchord:
                invfrom_current_invert = retry_msg
            else:
                invfrom_current_invert, fromchord, chordnames = retry_msg
                current_invert = fromchord
                highest_msg = chordnames
            final_result = f'{best[2]} {invfrom_current_invert}'
        else:
            final_result = f'{highest_msg} {invfrom_current_invert}'
        return final_result if not return_fromchord else (final_result,
                                                          current_invert,
                                                          highest_msg)

    if not whole_detect:
        return
    else:
        detect_var = detect_variation(current_chord, inv_num,
                                      change_from_first, original_first,
                                      same_note_special, N,
                                      alter_notes_show_degree)
        if detect_var is None:
            result_change = detect(
                current_chord,
                inv_num,
                not change_from_first,
                original_first,
                same_note_special,
                False,
                return_fromchord,
                alter_notes_show_degree=alter_notes_show_degree)
            if result_change is None:
                return detect_split(
                    current_chord,
                    N,
                    inv_num=inv_num,
                    change_from_first=change_from_first,
                    original_first=original_first,
                    same_note_special=same_note_special,
                    whole_detect=whole_detect,
                    return_fromchord=return_fromchord,
                    poly_chord_first=poly_chord_first,
                    root_position_return_first=root_position_return_first,
                    alter_notes_show_degree=alter_notes_show_degree)
            else:
                return result_change
        else:
            return detect_var


def getchord(start,
             mode=None,
             duration=0.25,
             intervals=None,
             interval=None,
             cummulative=True,
             pitch=4,
             ind=0,
             start_time=0):
    if not isinstance(start, note):
        start = toNote(start, pitch=pitch)
    if interval is not None:
        return getchord_by_interval(start,
                                    interval,
                                    duration,
                                    intervals,
                                    cummulative,
                                    start_time=start_time)
    premode = mode
    mode = mode.lower().replace(' ', '')
    initial = start.degree
    chordlist = [start]
    interval_premode = chordTypes(premode, mode=1, index=ind)
    if interval_premode != 'not found':
        interval = interval_premode
    else:
        interval_mode = chordTypes(mode, mode=1, index=ind)
        if interval_mode != 'not found':
            interval = interval_mode
        else:
            raise ValueError('could not detect the chord types')
    for i in range(len(interval)):
        chordlist.append(degree_to_note(initial + interval[i]))
    return chord(chordlist, duration, intervals, start_time=start_time)


chd = getchord


def trans(obj, pitch=4, duration=0.25, interval=None):
    obj = obj.replace(' ', '')
    if obj.count('/') > 1:
        current_parts = obj.split('/')
        current_parts = [int(i) if i.isdigit() else i for i in current_parts]
        result = trans(current_parts[0], pitch, duration, interval)
        for each in current_parts[1:]:
            if each in database.standard:
                each = database.standard_dict.get(each, each)
            elif not isinstance(each, int):
                each = trans(each, pitch, duration, interval)
            result /= each
        return result
    if obj in database.standard:
        return chd(obj,
                   'M',
                   pitch=pitch,
                   duration=duration,
                   intervals=interval)
    if '/' not in obj:
        check_structure = obj.split(',')
        check_structure_len = len(check_structure)
        if check_structure_len > 1:
            return trans(check_structure[0], pitch)(','.join(
                check_structure[1:])) % (duration, interval)
        N = len(obj)
        if N == 2:
            first = obj[0]
            types = obj[1]
            if first in database.standard and types in chordTypes:
                return chd(first,
                           types,
                           pitch=pitch,
                           duration=duration,
                           intervals=interval)
        elif N > 2:
            first_two = obj[:2]
            type1 = obj[2:]
            if first_two in database.standard and type1 in chordTypes:
                return chd(first_two,
                           type1,
                           pitch=pitch,
                           duration=duration,
                           intervals=interval)
            first_one = obj[0]
            type2 = obj[1:]
            if first_one in database.standard and type2 in chordTypes:
                return chd(first_one,
                           type2,
                           pitch=pitch,
                           duration=duration,
                           intervals=interval)
    else:
        parts = obj.split('/')
        part1, part2 = parts[0], '/'.join(parts[1:])
        first_chord = trans(part1, pitch)
        if isinstance(first_chord, chord):
            if part2.isdigit() or (part2[0] == '-' and part2[1:].isdigit()):
                return (first_chord / int(part2)) % (duration, interval)
            elif part2[-1] == '!' and part2[:-1].isdigit():
                return (first_chord @ int(part2[:-1])) % (duration, interval)
            elif part2 in database.standard:
                if part2 not in database.standard2:
                    part2 = database.standard_dict[part2]
                first_chord_notenames = first_chord.names()
                if part2 in first_chord_notenames and part2 != first_chord_notenames[
                        0]:
                    return (first_chord.inversion(
                        first_chord_notenames.index(part2))) % (duration,
                                                                interval)
                return chord([part2] + first_chord_notenames,
                             rootpitch=pitch,
                             duration=duration,
                             interval=interval)
            else:
                second_chord = trans(part2, pitch)
                if isinstance(second_chord, chord):
                    return chord(second_chord.names() + first_chord.names(),
                                 rootpitch=pitch,
                                 duration=duration,
                                 interval=interval)
    raise ValueError(
        'not a valid chord representation or chord types not in database')


C = trans


def info(self, alter_notes_show_degree=True, get_dict=False, **detect_args):
    chord_type = detect(self,
                        alter_notes_show_degree=alter_notes_show_degree,
                        **detect_args)
    if chord_type is None:
        return
    standard_notes = self.standardize()
    if len(standard_notes) == 1:
        if get_dict:
            return {
                '类型': '音符',
                '音符名称': str(standard_notes[0]),
                '完整名称': chord_type
            }
        else:
            return f'音符名称: {standard_notes[0]}'
    elif len(standard_notes) == 2:
        if get_dict:
            return {
                '类型': '音程',
                '音程名称': chord_type.split('和 ')[1],
                '根音': str(standard_notes[0]),
                '完整名称': chord_type
            }
        else:
            return f'音程名称: {chord_type.split("和 ")[1]}\n根音: {standard_notes[0]}'
    original_chord_type = copy(chord_type)
    other_msg = {'省略音': None, '变化音': None, '和弦外音的最低音': None, '和弦声位': None}
    has_split = False
    if '/' in chord_type:
        has_split = True
        if ']/[' in chord_type:
            chord_speciality = '复合和弦'
        else:
            chord_speciality = '转位和弦'
    elif '排序' in chord_type:
        chord_speciality = '和弦声位'
    else:
        alter_notes = chord_type.split(' ')
        if len(alter_notes) > 1 and alter_notes[1][0] in ['#', 'b']:
            chord_speciality = '变化音和弦'
        else:
            chord_speciality = '原位和弦'
    if '省略' in chord_type:
        if chord_speciality != '复合和弦':
            other_msg['省略音'] = [
                int(i) if i.isdigit() else i
                for i in chord_type.split('/', 1)[0].split('排序', 1)[0].strip(
                    '[]').split('省略', 1)[1].replace(' ', '').split(',')
            ]
    if '排序' in chord_type:
        other_msg['和弦声位'] = [
            int(i) for i in chord_type.split('/', 1)[0].strip('[]').split(
                '排序', 1)[1].replace(' ', '').strip('[]').split(',')
        ]
    try:
        alter_notes = chord_type.split('/', 1)[0].split(
            '排序', 1)[0].strip('[]').split(' ', 1)[1].replace(' ',
                                                             '').split(',')
    except:
        alter_notes = None
    if alter_notes:
        other_msg['变化音'] = []
        for each in alter_notes:
            if each and each[0] in ['#', 'b']:
                other_msg['变化音'].append(each)
        if not other_msg['变化音']:
            other_msg['变化音'] = None
    if has_split:
        inversion_split = chord_type.split('/')
        first_part = inversion_split[0].replace(',', '')
        if first_part[0] == '[':
            current_type = first_part[1:-1].split(' ')
        else:
            current_type = first_part.split(' ')
        current_type = [i for i in current_type if i]
        if len(current_type) > 1 and current_type[1][0] in ['#', 'b']:
            chord_types_root = ','.join(current_type)
            if len(inversion_split) > 1:
                chord_type = '/'.join([chord_types_root, inversion_split[1]])
        else:
            chord_types_root = current_type[0]
    else:
        chord_types_root = chord_type.split(' ')[0]
    note_names = self.names()
    note_names.sort(key=lambda s: len(s), reverse=True)
    for each in note_names:
        each_standard = f"{each[0].upper()}{''.join(each[1:])}"
        if each_standard in chord_types_root:
            root_note = each
            break
        elif each_standard in database.standard_dict and database.standard_dict[
                each_standard] in chord_types_root:
            root_note = each
            break
    if has_split:
        try:
            inversion_msg = inversion_from(C(chord_type),
                                           C(chord_types_root),
                                           num=True)
            if 'could not get chord' in inversion_msg:
                if inversion_split[1][0] == '[':
                    chord_type = original_chord_type
                    chord_types_root = chord_type
                else:
                    first_part, second_part = chord_type.split('/', 1)
                    if first_part[0] == '[':
                        first_part = first_part[1:-1]
                    chord_speciality = self._get_chord_speciality_helper(
                        first_part)
                    other_msg['和弦外音的最低音'] = second_part
        except:
            import traceback
            if '省略' in first_part and first_part[0] != '[':
                temp_ind = first_part.index(' ')
                current_chord_types_root = first_part[:
                                                      temp_ind] + ',' + first_part[
                                                          temp_ind:]
            else:
                current_chord_types_root = chord_types_root
            try:
                inversion_msg = inversion_from(self,
                                               C(current_chord_types_root),
                                               num=True)
                if 'could not get chord' in inversion_msg:
                    if inversion_split[1][0] == '[':
                        chord_type = original_chord_type
                        chord_types_root = chord_type
                    else:
                        first_part, second_part = chord_type.split('/', 1)
                        if first_part[0] == '[':
                            first_part = first_part[1:-1]
                        chord_speciality = self._get_chord_speciality_helper(
                            first_part)
                        other_msg['和弦外音的最低音'] = second_part
            except:
                chord_type = original_chord_type
                chord_types_root = chord_type
                if chord_speciality == '转位和弦':
                    inversion_msg = None
    if other_msg['变化音']:
        chord_types_root = chord_types_root.split(',')[0]
        chord_type = original_chord_type
    root_note = database.standard_dict.get(root_note, root_note)
    if chord_speciality == '复合和弦' or (chord_speciality == '转位和弦'
                                      and inversion_msg is None):
        chord_type_name = chord_type
    else:
        chord_type_name = chord_types_root[len(root_note):]
    if get_dict:
        return {
            '类型': '和弦',
            '和弦名称': chord_type,
            '原位': chord_types_root,
            '根音': root_note,
            '和弦类型': chord_type_name,
            '和弦性质': chord_speciality,
            '转位': inversion_msg if chord_speciality == '转位和弦' else None,
            '其他': other_msg
        }
    else:
        other_msg_str = '\n'.join(
            [f'{i}: {j}' for i, j in other_msg.items() if j])
        return f"和弦名称: {chord_type}\n原位和弦: {chord_types_root}\n根音: {root_note}\n和弦类型: {chord_type_name}\n和弦性质: {chord_speciality}" + (
            f"\n转位: {inversion_msg}" if chord_speciality == '转位和弦' else
            '') + (f'\n{other_msg_str}' if other_msg_str else '')


# browse

browse_language_dict = {
    'choose': "选择你想要播放的MIDI文件",
    'MIDI files': "MIDI文件",
    'go back': "返回",
    'choose MIDI file': "选择你想要播放的MIDI文件",
    'out of index': '这个轨道不存在',
    'cancel': "取消",
    'trackind': 'MIDI轨道序号',
    'from': '从',
    'to': '到',
    'show melody': '只显示主旋律',
    'show chord': '只显示和弦',
    'merge': '合并所有音轨',
    'file name': '文件名'
}

# ideal piano

ideal_piano_language_dict = {
    'sort': '排序',
    'current_midi_device': '请先进入MIDI键盘模式，按ctrl可以关掉我哦~',
    'changes': '已改变为',
    'reload': '重新加载设置',
    'load': '正在加载音源，请稍候...',
    'finished': '音源加载完成',
    'no MIDI input': 'MIDI设备id不存在，\n请右键点击MIDI KEYBOARD按钮选择一个MIDI设备',
    'pause': '已暂停, 按{unpause_key}键继续',
    'repeat': '音乐播放完毕, 按{repeat_key}键重新听一遍',
    'sample': '正在使用音频采样渲染当前MIDI文件，请稍等',
    'soundfont': '正在使用SoundFont渲染当前MIDI文件，请稍等',
    'type': '类型',
    'chord name': '和弦名称',
    'root': '根音',
    'note name': '音符名称',
    'interval name': '音程名称',
    'whole name': '完整名称',
    'other': '其他',
    'chord': '和弦',
    'note': '音符',
    'interval': '音程',
    'with': '和'
}
