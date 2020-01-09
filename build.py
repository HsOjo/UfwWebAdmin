import sys

from app import Log
from app.res.language import load_language, LANGUAGES
from app.res.language.translate_language import TranslateLanguage
from tools.translate import *

# build translate language data.
Log.append('Build', 'Info', 'Building translate data now...')

load_language()
for lang_type in LANGUAGES.values():
    if issubclass(lang_type, TranslateLanguage):
        lang = lang_type()
        if not lang._translated:
            if lang._translate_to == 'cn_t':
                translator = zhconv()
            elif '--translate-baidu' in sys.argv:
                translator = baidu_translate()
            else:
                translator = google_translate()
            Log.append('Build', 'Translate', 'Using %s' % translator.__class__.__name__)

            lang.translate(translator)
            lang.save_current_translate()

Log.append('Build', 'Info', 'Build finish.')
