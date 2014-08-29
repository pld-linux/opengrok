#!/bin/sh
# 
# OpenGrok script
# Lubomir Rintel <lkundrak@v3.sk>

# Source functions library
if [ -f /usr/share/java-utils/java-functions ] ; then 
  . /usr/share/java-utils/java-functions
else
  echo "Can't find functions library, aborting"
  exit 1
fi

# Load system-wide configuration
if [ -f /etc/opengrok.conf ]; then
  . /etc/opengrok.conf
fi

# Load user configuration
if [ -f "$HOME/.opengrokrc" ]; then
  . "$HOME/.opengrokrc"
fi

# Rest of the configuration
MAIN_CLASS=org.opensolaris.opengrok.index.Indexer

BASE_JARS="$BASE_JARS lucene.jar"
BASE_JARS="$BASE_JARS lucene-contrib/lucene-spellchecker.jar"
BASE_JARS="$BASE_JARS jakarta-oro.jar"
BASE_JARS="$BASE_JARS opengrok-jrcs"
BASE_JARS="$BASE_JARS bcel.jar"
BASE_JARS="$BASE_JARS servlet.jar"
BASE_JARS="$BASE_JARS ant.jar"
BASE_JARS="$BASE_JARS swing-layout.jar"
BASE_JARS="$BASE_JARS opengrok.jar"

# Set parameters
set_jvm
set_classpath $BASE_JARS
set_flags $BASE_FLAGS
set_options $BASE_OPTIONS $OPENGROK_OPTS

# Let's start
run "$@"
