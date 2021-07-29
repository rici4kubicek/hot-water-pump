#!/bin/bash
set -e

BASE_DIR=$(dirname "$0")
SRC=$(realpath "$BASE_DIR")
DIST=$(realpath "$BASE_DIR/dist")
BUILD=$(realpath "$BASE_DIR/build")

rm -rf "$BUILD"
mkdir "$BUILD"

rm -rf "$DIST"
mkdir "$DIST"

cp -r "$SRC/eledio-app "$BUILD"
cp -r "$SRC/app "$BUILD"
chmod a+x "$BUILD/eledio-app"

VERSION=$("$BASE_DIR/tools/long-version")

"$BASE_DIR/tools/replace" "$BUILD/eledio-app" '{{$APPVERSION$}}' "$VERSION"

tar -cvf "$DIST/eledio-app.tar" --owner=0 --group=0 -C "$BUILD" .