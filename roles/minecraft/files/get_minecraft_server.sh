#!/usr/bin/env bash

VERSION="$1"
VERSION_ARG="${VERSION}"

VERSIONS_URL="https://launchermeta.mojang.com/mc/game/version_manifest.json"
versions="$(/usr/bin/wget -O - "${VERSIONS_URL}")"

# If specified version is latest versions
: ${VERSION:="latest-release"}
if [ "${VERSION}" = 'latest-snapshot' -o "${VERSION}" = 'latest-release' ]; then
	if [ "$VERSION" == "latest-snapshot" ];    then pattern=".latest.snapshot"
	elif [ "${VERSION}" == "latest-release" ]; then pattern=".latest.release"
	else
		exit 1 # must not come here.
	fi

	VERSION=$(echo "${versions}" | jq -r "${pattern}")

	if ( test -z "${VERSION}" ); then
		echo "Automatic VERSION generating is failed. Regex doesn't match version information. You can use this image by setting VERSION manually." >&2
		exit 1
	fi
fi

version_url="$(echo "${versions}" | jq -r ".versions[] | select(.id == \"${VERSION}\").url")"
uri_jar="$(curl "${version_url}" | jq -r ".downloads.server.url")"

: ${EXEC_JAR:="/opt/minecraft_server.${VERSION}.jar"}
: ${URI_JAR:="${uri_jar}"}

# if file not found, try to download jar
if ( ! test -f "${EXEC_JAR}" ); then
	echo "Downloading \"${EXEC_JAR}\" from \"${URI_JAR}\"..."
	/usr/bin/wget -O "${EXEC_JAR}" "${URI_JAR}"
	# if failed to download
	if ( test "$?" -ne 0); then
		echo "Couldn't download! Check the enviroment variables to container." >&2
		exit 1
	fi
        if [ "${VERSION_ARG}" = "latest-snapshot" -o "${VERSION_ARG}" = "latest-release" ]; then
            ln -s ${EXEC_JAR} "/opt/minecraft_server.${VERSION_ARG}.jar"
        fi
fi

# vim: set ts=4 sw=4 :
