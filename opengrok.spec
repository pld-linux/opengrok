#
# Conditional build:
%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif

%include	/usr/lib/rpm/macros.java
Summary:	A wicked fast source browser
Name:		opengrok
Version:	0.7
Release:	0.1
License:	CDDL
Group:		Development/Languages/Java
Source0:	http://opensolaris.org/os/project/opengrok/files/%{name}-%{version}-src.tar.gz
# Source0-md5:	131c14590db48da55fc5a1ff2509e878
URL:		http://opensolaris.org/os/project/opengrok/
BuildRequires:	ant
BuildRequires:	ant-nodeps
BuildRequires:	jakarta-bcel >= 5.1
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
BuildRequires:	java-lucene
BuildRequires:	java-oro
BuildRequires:	java-servletapi5
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jflex
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	ctags
Requires:	group(servlet)
Requires:	java-servletapi5
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenGrok is a fast and usable source code search and cross reference
engine. It helps you search, cross-reference and navigate your source
tree. It can understand various program file formats and version
control histories like Mercurial, Git, SCCS, RCS, CVS, Subversion,
Teamware, ClearCase, Perforce and Bazaar. In other words it lets you
grok (profoundly understand) the open source, hence the name OpenGrok.
It is written in Java.

%prep
%setup -q -n %{name}-%{version}-src

mv lib nolibs
mkdir lib

%{__sed} -i -e 's,\r$,,' conf/web.xml

%build
export JAVA_HOME="%{java_home}"

# TODO: patch build.xml to use jflex from CLASSPATH
jflex_jar=$(find-jar jflex)
ln -sf $jflex_jar lib/JFlex.jar

required_jars="jaxp_parser_impl jflex ant"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

%ant \
	-Djavac.source=1.5 \
	-Djavac.target=1.5 \
	-Dfile.reference.ant.jar=$(find-jar ant) \
	-Dfile.reference.bcel-5.1.jar=$(find-jar bcel) \
	-Dfile.reference.jakarta-oro-2.0.8.jar=$(find-jar oro) \
	-Dfile.reference.lucene-core-2.2.0.jar=$(find-jar lucene) \
	-Dfile.reference.servlet-api.jar=$(find-jar servlet-api) \

#	-Dfile.reference.lucene-spellchecker-2.2.0.jar}:\
#	-Dfile.reference.org.apache.commons.jrcs.diff.jar}:\
#	-Dfile.reference.org.apache.commons.jrcs.rcs.jar}:\
#	-Dfile.reference.swing-layout-0.9.jar}:\
#	-Dfile.reference.jmxremote_optional.jar}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_javadir}}

cp -a dist/opengrok.jar $RPM_BUILD_ROOT%{_javadir}
#     [echo] To run this application from the command line without Ant, try:
#     [echo] java -cp "/usr/share/java/ant.jar:/usr/share/java/bcel.jar:/usr/share/java/oro.jar:/usr/share/java/lucene.jar:/home/users/glen/rpm/BUILD.noarch-linux/opengrok-0.7-src/lib/lucene-spellchecker-2.2.0.jar:/home/users/glen/rpm/BUILD.noarch-linux/opengrok-0.7-src/lib/org.apache.commons.jrcs.diff.jar:/home/users/glen/rpm/BUILD.noarch-linux/opengrok-0.7-src/lib/org.apache.commons.jrcs.rcs.jar:/usr/share/java/servlet-api.jar:/home/users/glen/rpm/BUILD.noarch-linux/opengrok-0.7-src/lib/swing-layout-0.9.jar:/home/users/glen/rpm/BUILD.noarch-linux/opengrok-0.7-src/lib/jmxremote_optional.jar:/home/users/glen/rpm/BUILD.noarch-linux/opengrok-0.7-src/dist/opengrok.jar" org.opensolaris.opengrok.index.Indexer
cp -a dist/source.war $RPM_BUILD_ROOT%{_javadir}
cp -a conf/web.xml

#     [echo] Generating man page..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt CHANGES.txt
