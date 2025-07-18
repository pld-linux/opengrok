# TODO
# - fix man generation
#
# Conditional build:
%bcond_with	javadoc		# don't build javadoc

Summary:	Source browser and indexer
Name:		opengrok
Version:	0.11.1
Release:	0.6
License:	CDDL
Group:		Development/Tools
Source0:	https://java.net/projects/opengrok/downloads/download/archive/%{name}-%{version}-src.tar.gz
# Source0-md5:	beb185b056a678b4119eff0c89a62d6c
Source1:	%{name}.sh
Source2:	configuration.xml
Source3:	tomcat-context.xml
Patch0:		lucene35.patch
Patch1:		jflex.patch
Patch2:		path.patch
URL:		http://opengrok.github.io/OpenGrok/
BuildRequires:	ant
BuildRequires:	docbook-dtd42-sgml
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-utils
BuildRequires:	java-bcel >= 5.1
BuildRequires:	java-cup
BuildRequires:	java-lucene >= 3.5
BuildRequires:	java-lucene-contrib >= 3.5
BuildRequires:	java-oro
BuildRequires:	java-servletapi
BuildRequires:	jdk
BuildRequires:	jflex >= 1.4
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	ant
Requires:	ctags
Requires:	group(servlet)
Requires:	java-bcel
Requires:	java-lucene >= 3.5
Requires:	java-lucene-contrib >= 3.5
Requires:	java-oro
Requires:	java-servletapi
Requires:	java-swing-layout
Requires:	jpackage-utils
Requires:	tomcat
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenGrok is a fast and usable source code search and cross reference
engine. It helps you search, cross-reference and navigate your source
tree. It can understand various program file formats and version
control histories like Mercurial, Git, SCCS, RCS, CVS, Subversion,
Teamware, ClearCase, Perforce and Bazaar. In other words it lets you
grok (profoundly understand) the open source, hence the name OpenGrok.

%prep
%setup -q -n %{name}-%{version}-src
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

# nuke prebuilt stuff
mv lib nolibs
mkdir lib

# Default war configuration
sed 's,/var/opengrok/etc/configuration.xml,%{_sysconfdir}/%{name}/configuration.xml,' \
        -i web/WEB-INF/web.xml

%build
export JAVA_HOME="%{java_home}"

required_jars="jflex cup junit"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

%ant \
	-Djavac.source=1.5 \
	-Djavac.target=1.5 \
	\
	-Dfile.reference.ant.jar=$(build-classpath ant) \
	-Dfile.reference.bcel-5.2.jar=$(build-classpath bcel) \
	-Dfile.reference.jakarta-oro-2.0.8.jar=$(build-classpath oro) \
	-Dfile.reference.lucene-core-3.0.2.jar=$(build-classpath lucene) \
	-Dfile.reference.lucene-spellchecker-3.0.2.jar=$(build-classpath lucene-contrib/lucene-spellchecker) \
	-Dfile.reference.org.apache.commons.jrcs.diff.jar=jrcs/lib/org.apache.commons.jrcs.diff.jar \
	-Dfile.reference.org.apache.commons.jrcs.rcs.jar=jrcs/lib/org.apache.commons.jrcs.rcs.jar \
	-Dfile.reference.servlet-api.jar=$(build-classpath servlet-api) \
	-Dfile.reference.swing-layout-0.9.jar=$(build-classpath swing-layout)

# SolBook is more-or-less DocBook subset, so this can be done safely
# FIXME: db2x_docbook2man output is not as nice as it should be
%if 0
%{__sed} -e '
        s,^<!DOCTYPE.*,<!DOCTYPE refentry PUBLIC "-//OASIS//DTD DocBook XML V4.2//EN" "/usr/share/sgml/docbook/xml-dtd-4.2/docbookx.dtd">,
        /^<?Pub Inc>/d
		/<?xml version="1.0" encoding="UTF-8"?>/d
' dist/opengrok.1 > opengrok.1.in
#docbook2man opengrok.1.in
refentry2man < dist/opengrok.1.in > opengrok.1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_bindir},%{_mandir}/man1,%{_javadir}} \
	$RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/{src,data} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_tomcatconfdir},%{_datadir}/%{name}} \
	$RPM_BUILD_ROOT%{_javadocdir}/%{name}

#     [echo] To run this application from the command line without Ant, try:
#     [echo] java -cp "%{_javadir}/ant.jar:%{_javadir}/bcel.jar:%{_javadir}/oro.jar:%{_javadir}/lucene.jar:/home/users/glen/rpm/BUILD.noarch-linux/opengrok-0.7-src/lib/lucene-spellchecker-2.2.0.jar:/home/users/glen/rpm/BUILD.noarch-linux/opengrok-0.7-src/lib/org.apache.commons.jrcs.diff.jar:/home/users/glen/rpm/BUILD.noarch-linux/opengrok-0.7-src/lib/org.apache.commons.jrcs.rcs.jar:%{_javadir}/servlet-api.jar:/home/users/glen/rpm/BUILD.noarch-linux/opengrok-0.7-src/lib/swing-layout-0.9.jar:/home/users/glen/rpm/BUILD.noarch-linux/opengrok-0.7-src/lib/jmxremote_optional.jar:/home/users/glen/rpm/BUILD.noarch-linux/opengrok-0.7-src/dist/opengrok.jar" org.opensolaris.opengrok.index.Indexer

# jar
install -p dist/opengrok.jar $RPM_BUILD_ROOT%{_javadir}/opengrok-%{version}.jar
ln -sf opengrok-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/opengrok.jar

# jrcs
install -p lib/jrcs.jar $RPM_BUILD_ROOT%{_javadir}/opengrok-jrcs-%{version}.jar
ln -sf opengrok-jrcs-%{version}.jar \
        $RPM_BUILD_ROOT%{_javadir}/opengrok-jrcs.jar

# bin
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}
#cp -p opengrok.1 $RPM_BUILD_ROOT%{_mandir}/man1

# Make love, not war!
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/lib
unzip -q dist/source.war -d $RPM_BUILD_ROOT%{_datadir}/%{name}
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/lib/jrcs.jar
(IFS=:; for file in $(build-classpath \
        bcel jakarta-oro swing-layout \
        lucene lucene-contrib/lucene-spellchecker) \
        %{_javadir}/opengrok.jar \
        %{_javadir}/opengrok-jrcs.jar; do
	ln -sf $file $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/lib
done)
mv $RPM_BUILD_ROOT{%{_datadir}/%{name}/WEB-INF,%{_sysconfdir}/%{name}}/web.xml
ln -sf %{_sysconfdir}/%{name}/web.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/WEB-INF/web.xml
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tomcat-context.xml
ln -sf %{_sysconfdir}/%{name}/tomcat-context.xml $RPM_BUILD_ROOT%{_tomcatconfdir}/%{name}.xml

%if %{with javadoc}
cp -a dist/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%endif

# Configuration file configuration.xml
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.txt doc/EXAMPLE.txt
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/configuration.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/tomcat-context.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/web.xml
%{_tomcatconfdir}/%{name}.xml
%attr(755,root,root) %{_bindir}/opengrok
#%{_mandir}/man1/opengrok.1*
%{_javadir}/opengrok-%{version}.jar
%{_javadir}/opengrok.jar
%{_javadir}/opengrok-jrcs-%{version}.jar
%{_javadir}/opengrok-jrcs.jar
%{_datadir}/%{name}
%{_localstatedir}/lib/%{name}

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/*
%endif
