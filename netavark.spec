Summary:	Container network stack
Name:		netavark
Version:	1.12.0
Release:	2
License:	Apache v2.0
Group:		Applications/System
Source0:	https://github.com/containers/netavark/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9fb18ecf2b4a3dbe3703059abeb0eaec
Source1:	https://github.com/containers/netavark/releases/download/v%{version}/%{name}-v%{version}-vendor.tar.gz
# Source1-md5:	2ffb9b306e08a26cd3bb3040c64cf91c
URL:		https://github.com/containers/netavark
BuildRequires:	cargo
BuildRequires:	go-md2man
BuildRequires:	protobuf
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust
Suggests:	aardvark-dns
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Netavark is a tool for configuring networking for Linux containers.
Its features include:
- Configuration of container networks via JSON configuration file
- Creation and management of required network interfaces, including
  MACVLAN networks
- All required firewall configuration to perform NAT and port
  forwarding as required for containers
- Support for iptables, firewalld and nftables
- Support for rootless containers
- Support for IPv4 and IPv6
- Support for container DNS resolution via the aardvark-dns project

%prep
%setup -q -a1

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build

%{__make} -C docs

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

install -D %cargo_objdir/netavark $RPM_BUILD_ROOT%{_libexecdir}/podman/netavark

%{__make} -C docs install \
	DESTDIR=$RPM_BUILD_ROOT \
	MANDIR="%{_mandir}"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md RELEASE_NOTES.md SECURITY.md
%attr(755,root,root) %{_libexecdir}/podman/netavark
%{_mandir}/man1/netavark.1*
