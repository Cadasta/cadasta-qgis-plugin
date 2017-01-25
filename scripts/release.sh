#!/bin/bash
echo "Export the plugin to a zip with no .git folder"
echo "And build a windows installer"

# Make sure has the proper sub module state
git submodule init
git submodule update

VERSION=`cat ../metadata.txt | grep ^version | sed 's/version=//g'`
STATUS=`cat ../metadata.txt | grep ^status | sed 's/status=//g'`

if [ "${STATUS}" != "final" ]; then
    VERSION="${VERSION}.${STATUS}"
fi

echo ${VERSION}

#see http://stackoverflow.com/questions/1371261/get-current-working-directory-name-in-bash-script
DIR='cadasta-qgis-plugin'

OUT="/tmp/${DIR}.${VERSION}.zip"

WORKDIR=/tmp/${DIR}$$
TARGZFILE="/tmp/${DIR}.tar.gz"

echo ${WORKDIR}

mkdir -p ${WORKDIR}
# Archive source code of the current branch to tar gz file.
# Use git-archive-all since we use git submodule.
pip install git-archive-all
git-archive-all ${TARGZFILE}
# Extract the file
tar -xf ${TARGZFILE} -C ${WORKDIR}
# Remove tar gz file
rm ${TARGZFILE}

rm -rf ${WORKDIR}/${DIR}/data/*

find ${WORKDIR}/${DIR} -name test*.py -delete
find ${WORKDIR}/${DIR} -name *_test.py -delete
find ${WORKDIR}/${DIR} -name *.po -delete
find ${WORKDIR}/${DIR} -name *.ts -delete

pushd .
cd ${WORKDIR}
find . -name test -exec /bin/rm -rf {} \;
# Compress all images shipped
#for FILE in `find . -type f -name "*.png"`
#do
#    echo "Compressing $FILE"
#    convert -dither FloydSteinberg -colors 128 $FILE $FILE
#done

# The \* tells zip to ignore recursively
rm ${OUT}
zip -r ${OUT} ${DIR} --exclude \*.pyc \
              ${DIR}/.git\* \
              ${DIR}/*.bat \
              ${DIR}/.gitattributes \
              ${DIR}/.settings\* \
              ${DIR}/.pydev\* \
              ${DIR}/.coverage\* \
              ${DIR}/.project\* \
              ${DIR}/.achievements\* \
              ${DIR}/Makefile \
              ${DIR}/scripts\* \
              ${DIR}/impossible_state.* \
              ${DIR}/riab_demo_data\* \
              ${DIR}/\*.*~ \
              ${DIR}/\*test_*.py \
              ${DIR}/\*.*.orig \
              ${DIR}/\*.bat \
              ${DIR}/\*.xcf \
              ${DIR}/\.tx\* \
              ${DIR}/\*.sh \
              ${DIR}/\Vagrantfile \
              ${DIR}/~

popd

#rm -rf ${WORKDIR}

echo "Your plugin archive has been generated as"
ls -lah ${OUT}
echo "${OUT}"