# TODO: libnifalcon, intersense, nidaqmx, viewpoint, phasespace, libfreespace
# proprietary: openhaptics, ghost,
# NATIONAL_INSTRUMENTS, NIDAQ, USDIGITAL, MICROSCRIBE, MONITONNODE, TRIVISIOCOLIBRI ???
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	gpm		# GPM Linux mouse interface support (GPL v2+)
%bcond_without	modbus		# Modbus support
%bcond_with	mpi		# MPI support
%bcond_without	wiiuse		# Wii support via wiiuse library (GPL v3+)
%bcond_without	java		# Java binding
#
%define	with_gpl	0%{?with_gpm:1}%{?with_wiiuse:1}
Summary:	Virtual Reality Peripheral Network
Summary(pl.UTF-8):	Sieć peryferiów do rzeczywistości wirtualnej (VR)
Name:		vrpn
Version:	07.32
%define	fver	%(echo %{version} | tr . _)
Release:	1
License:	Boost v1.0 (VRPN)%{?with_gpl:, depends on GPL libraries}
Group:		Libraries
Source0:	http://www.cs.unc.edu/Research/vrpn/downloads/%{name}_%{fver}.zip
# Source0-md5:	6cb32e51e6420385f2006f1aae58b457
Patch0:		%{name}-install.patch
Patch1:		%{name}-jsoncpp.patch
Patch2:		%{name}-modbus.patch
Patch3:		%{name}-wiiuse.patch
URL:		http://www.cs.unc.edu/Research/vrpn/
BuildRequires:	cmake >= 2.8.3
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_gpm:BuildRequires:	gpm-devel}
BuildRequires:	hidapi-devel >= 0.7.0
BuildRequires:	jdk
BuildRequires:	jsoncpp-devel >= 0.7.0
%{?with_modbus:BuildRequires:	libmodbus-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libusb-devel >= 1.0
%{?with_mpi:BuildRequires:	mpi-devel}
BuildRequires:	perl-Parse-RecDescent
BuildRequires:	perl-base
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	swig-python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Virtual-Reality Peripheral Network (VRPN) is a set of classes
within a library and a set of servers that are designed to implement a
network-transparent interface between application programs and the set
of physical devices (tracker, etc.) used in a virtual-reality (VR)
system. The idea is to have a PC or other host at each VR station that
controls the peripherals (tracker, button device, haptic device,
analog inputs, sound, etc). VRPN provides connections between the
application and all of the devices using the appropriate
class-of-service for each type of device sharing this link. The
application remains unaware of the network topology. Note that it is
possible to use VRPN with devices that are directly connected to the
machine that the application is running on, either using separate
control programs or running all as a single program.

%description -l pl.UTF-8
VRPN (Virtual-Reality Peripheral Network) to biblioteka klas i zestaw
serwerów zaprojektowanych jako implementacja przezroczystego sieciowo
interfejsu między aplikacjami a zbiorem urządzeń fizycznych (takich
jak tracker), używanych w systemie wirtualnej rzeczywistości (VR).
Idea polega na umieszczeniu komputera PC lub innego na każdej stacji
kontrolującej urządzenia peryferyjne (tracker, przyciski, urządzenie
haptyczne, wejścia analogowe, dźwiękowe itp.). VRPN zapewnia
połączenia między aplikacją a wszystkimi urządzeniami używającymi
odpowiedniej klasy usług dla każdego typu urządzeń współdzielących to
połączenie. Dla aplikacji topologia sieci nie ma znaczenia. Należy
zauważyć, że można używać oprogramowania VRPN z urządzeniami
podłączonymi bezpośrednio do maszyny, na której działa aplikacja -
albo przy użyciu osobnych programów sterujących, albo w ramach
jednego programu.

%package devel
Summary:	Header files for VRPN library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki VRPN
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for VRPN library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki VRPN.

%package apidocs
Summary:	VRPN API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki VRPN
Group:		Documentation

%description apidocs
API documentation for VRPN library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki VRPN.

%package -n java-vrpn
Summary:	Java binding to VRPN
Summary(pl.UTF-8):	Wiązanie Javy do bibliotek VRPN
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description -n java-vrpn
Java binding to VRPN.

%description -n java-vrpn -l pl.UTF-8
Wiązanie Javy do bibliotek VRPN.

%package -n python-vrpn
Summary:	Python binding to VRPN
Summary(pl.UTF-8):	Wiązania Pythona do bibliotek VRPN
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description -n python-vrpn
Python binding to VRPN.

%description -n python-vrpn -l pl.UTF-8
Wiązania Pythona do bibliotek VRPN.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
install -d build
cd build
%cmake .. \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir}/vrpn \
	-DVRPN_BUILD_PYTHON=ON \
	%{?with_gpl:-DVRPN_GPL_SERVER=ON} \
	-DVRPN_USE_GPM_MOUSE=%{?with_gpm:ON}%{!?with_gpm:OFF} \
	-DVRPN_USE_LOCAL_HIDAPI=OFF \
	-DVRPN_USE_LOCAL_JSONCPP=OFF \
	%{?with_modbus:-DVRPN_USE_MODBUS=ON} \
	-DVRPN_USE_MPI=%{?with_mpi:ON}%{!?with_mpi:OFF} \
	%{!?with_wiiuse:-DVRPN_USE_WIIUSE=OFF}

%{__make}

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/{c_interface_example,checklogfile,client_and_server,clock_drift_estimator,forcedevice_test_client,forward,forwarderClient,last_of_sequence,logfilesenders,logfiletypes,printcereal,printvals,run_auxiliary_logger,sample_analog,sample_server,test*,text,textServer,tracker_to_poser}

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/source-docs

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog Format README README.Legal
%attr(755,root,root) %{_bindir}/add_vrpn_cookie
%attr(755,root,root) %{_bindir}/bdbox_client
%attr(755,root,root) %{_bindir}/ff_client
%attr(755,root,root) %{_bindir}/phan_client
%attr(755,root,root) %{_bindir}/sound_client
%attr(755,root,root) %{_bindir}/sphere_client
%attr(755,root,root) %{_bindir}/vrpn_HID_device_watcher
%attr(755,root,root) %{_bindir}/vrpn_LamportClock
%attr(755,root,root) %{_bindir}/vrpn_ping
%attr(755,root,root) %{_bindir}/vrpn_print_devices
%attr(755,root,root) %{_bindir}/vrpn_print_messages
%attr(755,root,root) %{_bindir}/vrpn_print_performance
%attr(755,root,root) %{_bindir}/vrpn_server
%attr(755,root,root) %{_bindir}/vrpn_streamPrint
%dir %{_sysconfdir}/vrpn
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vrpn/vrpn.cfg
%attr(755,root,root) %{_libdir}/libgpsnmea.so
%attr(755,root,root) %{_libdir}/libquat.so
%attr(755,root,root) %{_libdir}/libvrpn.so
%attr(755,root,root) %{_libdir}/libvrpn_atmel.so
%attr(755,root,root) %{_libdir}/libvrpn_timecode_generator.so
%attr(755,root,root) %{_libdir}/libvrpnserver.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/latLonCoord.h
%{_includedir}/nmeaParser.h
%{_includedir}/quat.h
%{_includedir}/utmCoord.h
%{_includedir}/vrpn_*.h

%if %{with java}
%files -n java-vrpn
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjava_vrpn.so
%{_javadir}/vrpn-%{version}.jar
%endif

%files -n python-vrpn
%defattr(644,root,root,755)
# swig bindings
%attr(755,root,root) %{py_sitedir}/_vrpn_*.so
%attr(755,root,root) %{py_sitedir}/vrpn_*.py[co]
# "handwritten" binding
%attr(755,root,root) %{py_sitedir}/vrpn.so

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doxygen/docs-generated/html/*
%endif
