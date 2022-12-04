#!/bin/sh

echo "#!/bin/sh" > dist/hbd.sh
base64 hbd.py >> dist/hbd.sh
