import os
import sys

doc_root = os.path.dirname(__file__)
os.chdir(doc_root)

sys.path.append(doc_root)
if os.path.exists('%s/venv' % doc_root):
    version = sys.version_info
    pkgs_path = '%s/venv/lib/python%d.%d/site-packages' % (doc_root, version.major, version.minor)
    if os.path.exists(pkgs_path):
        sys.path.append(pkgs_path)

application = getattr(__import__('app'), 'create_app')()
