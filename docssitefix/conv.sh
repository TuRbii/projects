#!/bin/bash

#Convert the markup files to html

doc=""
dest="/tmp/web.$$"
header="`dirname $0`/header.html"
footer="`dirname $0`/footer.html"
css="`dirname $0`/style.css"
lock="/tmp/`basename $0`.lock"


function help() {
	cat <<END
Usage: $0 [-h | --help] DIR

Options:
	--help          Display this help
	-h | --header   The header to use instead of the default
	-f | --footer   The footer to use instead of the default
	-c | --css      The CSS file to use instead of the ddefault
	-d | --dest     The location to make the HTML files
	-v | --verbose  Say what's happening

Pass this utility the dir that holds the documentation and it will
convert it to HTML. A header, footer, and CSS (defaults to
"header.html", "footer.html", "style.css") will be applied to each
file.
END
	exit 0
}


if [[ $# -eq 0 ]]; then
	help
fi

while [[ $# -gt 0 ]]; do
	case "$1" in
	--help)
		help
		;;
	-h|--header)
		shift
		header="$1"
		;;
	-f|--footer)
		shift
		footer="$1"
		;;
	-d|--dest)
		shift
		dest="$1"
		;;
	-c|--css)
		shift
		css="$1"
		;;
	-v|--verbose)
		verbose=1
		;;
	*)
		if [[ ! -d $1 ]]; then
			echo "'$1' is not a dir" 1>&2
			exit 1
		fi
		doc="$1"
		;;
	esac
	shift
done

#Check for the lock file
if [[ -e "$lock" ]]; then
	>&2 echo "Lock file '$lock' exists"
	exit 2
else
	touch "$lock"
fi

#Update the documentation repo
git -C "$doc" remote update
git -C "$doc" reset --hard origin/master --
git -C "$doc" clean -f

#Clean up the destination
mkdir -p "$dest"
rm -rf "$dest"/*
cp -r "$doc"/* "$dest"
cp "$css" "$dest"

#Convert each file from Markup to HTML
for f in `find "$dest" -name "*.md"`; do
	o=`echo "$f" | sed 's/\.md/\.html/'`
	[[ $verbose -eq 1 ]] && echo $f "->" $o
	cat "$header" >"$o"
	cat "$f" | /usr/local/bin/cmark | sed 's/\.md/.html/g' >>"$o"
	cat "$footer" >>"$o"
	rm "$f"
done

#Find each HTML file and make a site map.
walk () {
	echo '<ul>'
	for f in *; do
		b=`basename "$f"`
		if test -d "$f"; then
			echo '<li>'$b'</li>'
			(cd "$f"; walk "$1/$f")
		fi
		if echo "$f" | grep 'html$' > /dev/null; then
			echo '<li><a href="'$1/$f'">'$b'</a></li>'
		fi
	done
	echo '</ul>'
}
cat "$header" >"$dest"/index.html
echo '<h1>Site Map</h1>' >>"$dest"/index.html
(cd "$dest"; walk) >>"$dest"/index.html
cat "$footer" >>"$dest"/index.html


rm "$lock"
echo "$dest"

