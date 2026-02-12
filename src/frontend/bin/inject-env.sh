#!/bin/sh

source=$1
# Create temporary file to use for changes
dest=$source.TMP
cp "$source" "$dest"

# Loop over any Environment variables in given file and replace them
for key in $(grep process\.env "$dest" | sed -r 's/.*process\.env\.([A-Z_]+).*/\1/'); do
  value=$(eval echo \$\{$key\})
  sed -re "s|process\.env\.[A-Z_]+|$value|g" -i "$dest"
done

# Move results and start server
fname=$(basename "$source")
mv "$dest" "/usr/share/nginx/html/$fname" && nginx -g 'daemon off;'
