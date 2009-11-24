# TODO
# - i've installed .so to %{_libdir} because straced mysqld searched
#   same path as dlopen() would do (/lib:/lib/tls:/usr/lib). perhaps
#   %{_libdir}/mysql would be more appropriate (but then need to
#   insert .so with full path? patch mysqld?)
Summary:	MySQL UDF interface to PCRE
Name:		mysql-udf-preg
Version:	1.0
Release:	0.2
License:	GPL v3
Group:		Applications/Databases
Source0:	http://www.mysqludf.org/lib_mysqludf_preg/lib_mysqludf_preg-%{version}.tar.gz
# Source0-md5:	c1837e6996417669d7d10bc1ae1d00e6
URL:		http://www.mysqludf.org/lib_mysqludf_preg/index.php
BuildRequires:	mysql-devel
BuildRequires:	pcre-devel
Requires:	mysql
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MySQL UDF interface to the PCRE (Perl Compatible Regular Expressions)
library for pattern matching.

The PCRE library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics as
Perl 5. This syntax can often handle more complex expressions and
capturing than standard regular expression implementations.

lib_mysqludf_preg is a useful performance optimization for those
applications that are already performing these regular expression
matches in a high level language (i. e. PHP) on the client side. It is
also helpful when there is a need to capture a parenthesized
subexpression from a regular expression, or simply as a slight
performance boost over the builtin RLIKE/REGEXP functions.

%prep
%setup -q -n lib_mysqludf_preg-%{version}

%build
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/lib_mysqludf_preg.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	%banner -e %{name} <<-'EOF'
	To actually use the functions execute on your MySQL instances:

	zcat %{_docdir}/%{name}-%{version}/installdb.sql.gz | mysql

	To remove the functions:
	zcat %{_docdir}/%{name}-%{version}/uninstalldb.sql.gz | mysql

	EOF
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL README
%doc installdb.sql uninstalldb.sql
%attr(755,root,root) %{_libdir}/lib_mysqludf_preg.so
