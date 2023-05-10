
import sys
import unicodedata
import warnings


# https://github.com/ksze/sanitize

class ReplacementLengthWarning(UserWarning):
    pass


warnings.filterwarnings("always", category=ReplacementLengthWarning)


def _are_unicode(unicode_args=[]):
    if sys.version_info[0] == 2:
        return all((type(arg) == str) for arg in unicode_args)

    # Assume Python 3
    return all((type(arg) == str) for arg in unicode_args)


def sanitize_path_fragment(
        original_fragment,
        filename_extension = '', # when you do want a filename extension, there is no need to include the leading dot.
        target_file_systems = {
                'btrfs', 'ext', 'ext2', 'ext3', 'ext3cow', 'ext4', 'exfat', 'fat32',
                'hfs+', 'ntfs_win32', 'reiser4', 'reiserfs', 'xfs', 'zfs',
            },
        sanitization_method = 'underscore',
        truncate = True,
        replacement = '_',
        additional_illegal_characters=[],
    ):
    # Enforce that these args are unicode strings
    unicode_args = [original_fragment, filename_extension, replacement] + additional_illegal_characters
    if not _are_unicode(unicode_args):
        raise ValueError(
                '`original_fragment`, `filename_extension`, `replacement`, and `additional_illegal_characters` '
                'must be of the unicode type under Python 2 or str type under Python 3.'
            )

    if len(replacement) > 1:
        warnings.warn(
                "The replacement is longer than one character. "
                "The length of the resulting string cannot be guaranteed to fit the target file systems' length limit.",
                ReplacementLengthWarning
            )

    sanitized_fragment = unicodedata.normalize('NFC', original_fragment)
    if len(filename_extension) > 0:
        filename_extension = unicodedata.normalize('NFC', '.' + filename_extension)

    if sanitization_method == 'underscore':
        illegal_characters = {
            'btrfs': {'\0', '/'},
            'ext': {'\0', '/'},
            'ext2': {'\0', '/'},
            'ext3': {'\0', '/'},
            'ext3cow': {'\0', '/', '@'},
            'ext4': {'\0', '/'},
            'exfat': {
                '\00', '\01', '\02', '\03', '\04', '\05', '\06', '\07', '\10', '\11', '\12', '\13', '\14', '\15', '\16', '\17',
                '\20', '\21', '\22', '\23', '\24', '\25', '\26', '\27', '\30', '\31', '\32', '\33', '\34', '\35', '\36', '\37',
                '/', '\\', ':', '*', '?', '"', '<', '>', '|',
            },
            'fat32': { # TODO: Confirm this list; current list is just a wild guess, assuming UTF-16 encoding.
                '\00', '\01', '\02', '\03', '\04', '\05', '\06', '\07', '\10', '\11', '\12', '\13', '\14', '\15', '\16', '\17',
                '\20', '\21', '\22', '\23', '\24', '\25', '\26', '\27', '\30', '\31', '\32', '\33', '\34', '\35', '\36', '\37',
                '/', '\\', ':', '*', '?', '"', '<', '>', '|',
            },
            # In theory, all Unicode characters, including NUL, are usable in HFS+; so this is just
            # a sane set for legacy compatibility - e.g. OS APIs that don't support '/' and ':'.
            'hfs+': {'\0', '/', ':'},
            'ntfs_win32': {'\0', '/', '\\', ':', '*', '?', '"', '<', '>', '|'}, # NTFS Win32 namespace (stricter)
            'ntfs_posix': {'\0', '/'},                                          # NTFS POSIX namespace (looser)
            'reiser4': {'\0', '/'},
            'reiserfs': {'\0', '/'},
            'xfs': {'\0', '/'},
            'zfs': {'\0', '/'},
            'additional_illegal_characters': set(additional_illegal_characters),
        }

        # Replace illegal characters with an underscore
        # `target_file_systems` is used further down, so we don't want to pollute it here.
        _temp_target_file_systems = set.union(target_file_systems, {'additional_illegal_characters'})

        illegal_character_set = set.union(*(illegal_characters[file_system] for file_system in _temp_target_file_systems))

        # It would be stupid if the replacement contains an illegal character.
        if any(character in replacement for character in illegal_character_set):
            raise ValueError('The replacement contains a character that would be illegal in the target file system(s).')

        for character in illegal_character_set:
            sanitized_fragment = sanitized_fragment.replace(character, replacement)
            filename_extension = filename_extension.replace(character, replacement)

        # "Quote" illegal filenames
        if target_file_systems.intersection({'fat32', 'ntfs_win32'}):
            windows_reserved_names = (
                    "CON", "PRN", "AUX", "NUL",
                    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
                    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
                )

            if sanitized_fragment in windows_reserved_names:
                sanitized_fragment = replacement + sanitized_fragment + replacement

            if filename_extension in windows_reserved_names:
                filename_extension = replacement + filename_extension + replacement


        # Truncate if the resulting string is too long
        if truncate:
            max_lengths = {
                # For the entries of file systems commonly found with Linux, the length, 'utf-8',
                # and 'NFC' are only assumptions that apply to mostly vanilla kernels with default
                # build parameters.

                # Seriously, this is 2013. The fact that the Linux community does not move to a file
                # system with an enforced Unicode filename encoding is as bad as Windows 95's
                # codepage madness, some 18 years ago.

                # If you add more file systems, see if it is affected by Unicode Normal Forms, like
                # HFS+; You may have to take extra care in editing the actual sanitization routine
                # below.
                'btrfs': (255, 'bytes', 'utf-8', 'NFC'),
                'ext': (255, 'bytes', 'utf-8', 'NFC'),
                'ext2': (255, 'bytes', 'utf-8', 'NFC'),
                'ext3': (255, 'bytes', 'utf-8', 'NFC'),
                'ext3cow': (255, 'bytes', 'utf-8', 'NFC'),
                'ext4': (255, 'bytes', 'utf-8', 'NFC'),
                'exfat': (255, 'characters', 'utf-16', 'NFC'),

                # 'utf-16' is not entirely true. FAT32 used to be used with codepages; but since
                # Windows XP, the default seems to be UTF-16.
                'fat32': (255, 'characters', 'utf-16', 'NFC'),

                # FIXME: improve HFS+ handling, because it does not use the standard NFD. It's
                # close, but it's not exactly the same thing.
                'hfs+': (255, 'characters', 'utf-16', 'NFD'),

                'ntfs_win32': (255, 'characters', 'utf-16', 'NFC'),
                'ntfs_posix': (255, 'characters', 'utf-16', 'NFC'),

                # ReiserFS 3 and 4 support filenames > 255 bytes. I don't care if the vanilla Linux
                # kernel can't support that. That's Linux's problem, not mine.
                'reiser4': (3976, 'bytes', 'utf-8', 'NFC'),
                'reiserfs': (4032, 'bytes', 'utf-8', 'NFC'),

                'xfs': (255, 'bytes', 'utf-8', 'NFC'),
                'zfs': (255, 'bytes', 'utf-8', 'NFC'),
            }

            for file_system in target_file_systems:
                if max_lengths[file_system][1] == 'bytes':
                    extension_bytes = unicodedata.normalize(max_lengths[file_system][3], filename_extension).encode(max_lengths[file_system][2])

                    temp_fragment = bytearray()

                    for character in sanitized_fragment:
                        encoded_bytes = unicodedata.normalize(max_lengths[file_system][3], character).encode(max_lengths[file_system][2])

                        if len(temp_fragment) + len(encoded_bytes) + len(extension_bytes)<= max_lengths[file_system][0]:
                            temp_fragment = temp_fragment + encoded_bytes
                        else:
                            break

                    sanitized_fragment = unicodedata.normalize('NFC', temp_fragment.decode(max_lengths[file_system][2]))

                else: # Assume 'characters'
                    temp_fragment = ''

                    if file_system == 'hfs+':
                        normalize = unicodedata.ucd_3_2_0.normalize
                    else:
                        normalize = unicodedata.normalize

                    normalized_extension = normalize(max_lengths[file_system][3], filename_extension)

                    for character in sanitized_fragment:
                        normalized_character = normalize(max_lengths[file_system][3], character)
                        if len(temp_fragment) + len(normalized_character) + len(normalized_extension) <= max_lengths[file_system][0]:
                            temp_fragment += normalized_character
                        else:
                            break

                    sanitized_fragment = unicodedata.normalize('NFC', temp_fragment)

        sanitized_fragment = sanitized_fragment + filename_extension

        # Disallow a final dot or space for FAT32 and NTFS in Win32 namespace.
        # This can only be done after truncations because otherwise we may fix the fragment, but
        # still end up with a bad ending character once it's truncated
        if (
                target_file_systems.intersection({'fat32', 'ntfs_win32'}) and
                (sanitized_fragment.endswith('.') or sanitized_fragment.endswith(' '))
            ):

            if replacement.endswith('.') or replacement.endswith(' '):
                raise ValueError(
                        'The sanitized string ends with a dot or space, and the replacement also ends with a dot or space. '
                        'Therefore the string cannot be sanitized for fat32 or ntfs_win32.'
                    )

            while (sanitized_fragment.endswith('.') or sanitized_fragment.endswith(' ')):
                sanitized_fragment = sanitized_fragment[:-1] + replacement

    else:
        raise ValueError("sanitization_method must be a valid sanitization method.")

    return sanitized_fragment
