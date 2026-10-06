"""Create private local configuration without printing the administrative secret."""
import os
import secrets
from pathlib import Path

root = Path(__file__).resolve().parent
config = root / '.env'
if not config.exists():
    config.write_text('ADMIN_TOKEN=' + secrets.token_urlsafe(40) + '\nCANDIDATE_IMAGE=northstar-submission:local\nLOCAL_UID=' + str(os.getuid() if hasattr(os, 'getuid') else 1000) + '\nLOCAL_GID=' + str(os.getgid() if hasattr(os, 'getgid') else 1000) + '\n', encoding='utf-8')
provider = root / '.candidate.env'
if not provider.exists():
    provider.write_text('# Add only candidate model/provider keys here. Never add ADMIN_TOKEN.\n', encoding='utf-8')
(root / 'reports').mkdir(exist_ok=True)
print('Private .env, model-key placeholder and reports directory are ready. Secrets were not printed.')
