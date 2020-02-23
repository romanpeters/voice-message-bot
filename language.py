class Language(object):
    LANGUAGE = "en_EN"
    DOWNLOADING = "Downloading..."
    TRANSCODING = "Transcoding..."
    TRANSCRIBING = "Transcribing..."
    UNKNOWN_VALUE = "???"
    REQUEST_ERROR = "Something went wrong"


class English(Language):
    pass


class Dutch(Language):
    LANGUAGE = "nl_NL"
    DOWNLOADING = "Aan het downloaden..."
    TRANSCODING = "Aan het transcoden..."
    TRANSCRIBING = "Aan het transcriberen..."
    UNKNOWN_VALUE = "???"
    REQUEST_ERROR = "Er ging iets verkeerd"
