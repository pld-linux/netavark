Summary:	Container network stack
Name:		netavark
Version:	1.6.0
Release:	1
License:	Apache v2.0
Group:		Applications/System
Source0:	https://github.com/containers/netavark/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d74d976ff73153cd398853a8b114ea9d
Source1:	https://github.com/containers/netavark/releases/download/v%{version}/%{name}-v%{version}-vendor.tar.gz
# Source1-md5:	7d50dcc38f030c28389a86eed4a753f3
URL:		https://github.com/containers/netavark
BuildRequires:	cargo
BuildRequires:	mandown
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
- Support for iptables and firewalld at present, with support for
  nftables planned in a future release
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
