#!/bin/bash

PACKAGE_NAME=$1
VERSION=$2
PACKAGES_DIR=$3
INSTALL=$4

BUILD_DIR="/tmp/.private/$USER/python3-build"
HSH_DIR="$BUILD_DIR/hsh-workdir"
SPECFILE_TEMPLATE="$(dirname $0)/python3.altlinux.spec.template"
SPECFILE="$BUILD_DIR/SPECS/$PACKAGE_NAME.spec"
PACKAGE_FILE="${PACKAGE_NAME}-${VERSION}-alt1.$(arch).rpm"


mkdir -pv $BUILD_DIR/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS} || exit 1
cp -v $SPECFILE_TEMPLATE $SPECFILE || exit 2
sed -i "s/{Name}/Name: $PACKAGE_NAME/" $SPECFILE || exit 3
sed -i "s/{Version}/Version: $VERSION/" $SPECFILE || exit 4
wget --directory-prefix="$BUILD_DIR/SOURCES" \
    https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tar.xz || exit 5
rpmbuild --define "_topdir $BUILD_DIR" --nodeps -bs $SPECFILE || exit 6
mkdir -pv "$HSH_DIR" "$PACKAGES_DIR" || exit 7
hsh --no-sisyphus-check \
    --workdir=$HSH_DIR \
    $BUILD_DIR/SRPMS/${PACKAGE_NAME}-${VERSION}-alt1.src.rpm || exit 8
cp -v \
    $HSH_DIR/repo/$(arch)/RPMS.hasher/$PACKAGE_FILE \
    "$PACKAGES_DIR" || exit 9
[ $INSTALL = "True" ] && ( epm install "$PACKAGES_DIR/$PACKAGE_FILE" || exit 10 )

exit 0