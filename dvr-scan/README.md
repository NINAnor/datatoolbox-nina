# dvr-scan

Detect motion on videos and extract segments.

## Snippets

Here is an example on how to generate a playlist file with the resulting segments, sorted by the forth field in the filename, and converting the path for Windows PC.

```bash
find -type f -name '*.avi' -print | sort -t_ -k4 | xargs -L1 realpath | sed 's|^/data/P-Prosjekter2/|P:\\|; s|/|\\|g' > playlist.m3u
```

This is an example on how to rename files so that the timestamp is placed at the beginning of the filename:

```bash
rename -E 's/^(\d+_\d+_\w)_(\d+)/$2_$1/' *.avi
```
