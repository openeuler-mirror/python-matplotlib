%global debug_package %{nil}
Name:           python-matplotlib
Version:        2.2.4
Release:        3
Summary:        A comprehensive library for creating static, animated, and interactive visualizations
License:        Python and MIT and OFL-1.1 and BSD-3-Clause
URL:            https://github.com/matplotlib/matplotlib
Source0:        https://github.com/matplotlib/matplotlib/archive/v%{version}/matplotlib-%{version}.tar.gz
# The config file for python-matplotlib
Source1:        setup.cfg
Source1000:     https://github.com/QuLogic/mpl-images/archive/v2.2.3-with-freetype-2.8/matplotlib-2.2.3-with-freetype-2.9.1.tar.gz
Patch0001:      0001-Use-packaged-jquery-and-jquery-ui.patch
BuildRequires:  freetype-devel libpng-devel qhull-devel texlive-cm xorg-x11-server-Xvfb zlib-devel


%description
The package produces publication-quality figures in a variety of hardcopy formats and interactive environments
across platforms.

%package -n     python-matplotlib-data
Summary:        Data used by python-matplotlib
BuildArch:      noarch
Requires:       python-matplotlib-data-fonts = %{version}-%{release}
%python_provide python-matplotlib-data

%description -n python-matplotlib-data
Data used by python-matplotlib.

%package -n     python-matplotlib-data-fonts
Summary:        Fonts used by python-matplotlib
BuildArch:      noarch
Requires:       python-matplotlib-data = %{version}-%{release}
%python_provide python-matplotlib-data-fonts

%description -n python-matplotlib-data-fonts
Fonts used by python-matplotlib.

%package -n     python3-matplotlib
Summary:        Plotting with Python
BuildRequires:  python3-cairo python3-cycler >= 0.10.0 python3-dateutil python3-devel
BuildRequires:  python3-setuptools python3-gobject python3-kiwisolver python3-numpy
BuildRequires:  python3-pillow python3-pyparsing python3-pytz python3-six python3-sphinx
Requires:       dejavu-sans-fonts dvipng python-matplotlib-data = %{version}-%{release}
Requires:       python3-cairo python3-cycler >= 0.10.0 python3-dateutil python3-kiwisolver
Requires:       python3-matplotlib-tk = %{version}-%{release} python3-numpy
Requires:       python3-pyparsing python3-pytz python3-six
Provides:       bundled(stix-math-fonts)
Recommends:     python3-pillow
%python_provide python3-matplotlib

%description -n python3-matplotlib
The package produces publication-quality figures in a variety of hardcopy formats and interactive environments
across platforms.

%package -n     python3-matplotlib-qt4
Summary:        Qt4 backend for python3-matplotlib
BuildRequires:  python3-PyQt4-devel
Requires:       python3-matplotlib = %{version}-%{release} python3-matplotlib-qt5 python3-PyQt4
%python_provide python3-matplotlib-qt4

%description -n python3-matplotlib-qt4
The qt4 backend for python3-matplotlib.

%package -n     python3-matplotlib-qt5
Summary:        Qt5 backend for python3-matplotlib
BuildRequires:  python3-qt5
Requires:       python3-matplotlib = %{version}-%{release} python3-qt5
%python_provide python3-matplotlib-qt5

%description -n python3-matplotlib-qt5
The qt5 backend for python3-matplotlib.

%package -n     python3-matplotlib-gtk3
Summary:        GTK3 backend for python3-matplotlib
BuildRequires:  gtk3 python3-gobject
Requires:       gtk3 python3-gobject python3-matplotlib = %{version}-%{release}
%python_provide python3-matplotlib-gtk3

%description -n python3-matplotlib-gtk3
The gtk3 backend for python3-matplotlib.

%package -n     python3-matplotlib-tk
Summary:        Tk backend for python3-matplotlib
BuildRequires:  python3-tkinter
Requires:       python3-matplotlib = %{version}-%{release} python3-tkinter
%python_provide python3-matplotlib-tk

%description -n python3-matplotlib-tk
The tk backend for python3-matplotlib.

%package -n     python3-matplotlib-test-data
Summary:        Test data for python3-matplotlib
Requires:       python3-matplotlib = %{version}-%{release}
%python_provide python3-matplotlib-test-data

%description -n python3-matplotlib-test-data
Test data for python3-matplotlib.

%prep
%autosetup -n matplotlib-%{version} -p1 -N
%patch0001 -p1
gzip -dc %SOURCE1000 | tar xvf - --transform='s~^mpl-images-2.2.3-with-freetype-2.9.1/\([^/]\+\)/~lib/\1/tests/baseline_images/~'
rm -r extern/libqhull
sed 's/\(backend = \).*/\1TkAgg/' >setup.cfg <%{SOURCE1}

%build
export http_proxy=http://127.0.0.1/
find examples -name '*.py' -exec chmod a-x '{}' \;
MPLCONFIGDIR=$PWD MATPLOTLIBDATA=$PWD/lib/matplotlib/mpl-data xvfb-run %{__python3} setup.py build

%install
export http_proxy=http://127.0.0.1/
mkdir -p %{buildroot}%{_sysconfdir} %{buildroot}%{_datadir}/matplotlib
MPLCONFIGDIR=$PWD MATPLOTLIBDATA=$PWD/lib/matplotlib/mpl-data/ %{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
mv %{buildroot}%{python3_sitearch}/matplotlib/mpl-data/matplotlibrc %{buildroot}%{_sysconfdir}
mv %{buildroot}%{python3_sitearch}/matplotlib/mpl-data %{buildroot}%{_datadir}/matplotlib
chmod +x %{buildroot}%{python3_sitearch}/matplotlib/dates.py

%files -n python-matplotlib-data
%{_sysconfdir}/matplotlibrc
%{_datadir}/matplotlib/mpl-data/
%exclude %{_datadir}/matplotlib/mpl-data/fonts/

%files -n python-matplotlib-data-fonts
%{_datadir}/matplotlib/mpl-data/fonts/


%files -n python3-matplotlib
%doc README.rst LICENSE/
%{python3_sitearch}/{*egg-info,matplotlib-*-nspkg.pth,matplotlib/}
%{python3_sitearch}/mpl_toolkits/
%{python3_sitearch}/{pylab.py*,__pycache__/*}
%exclude %{python3_sitearch}/matplotlib/tests/baseline_images/*
%exclude %{python3_sitearch}/mpl_toolkits/tests/baseline_images/*
%exclude %{python3_sitearch}/matplotlib/backends/{backend_qt4*,__pycache__/backend_qt4*}
%exclude %{python3_sitearch}/matplotlib/backends/{backend_qt5*,__pycache__/backend_qt5*}
%exclude %{python3_sitearch}/matplotlib/backends/{backend_gtk*,__pycache__/backend_gtk*}
%exclude %{python3_sitearch}/matplotlib/backends/{backend_tkagg.*,__pycache__/backend_tkagg.*}
%exclude %{python3_sitearch}/matplotlib/backends/{tkagg.*,__pycache__/tkagg.*,_tkagg.*}
%exclude %{_pkgdocdir}/*/

%files -n python3-matplotlib-test-data
%{python3_sitearch}/matplotlib/tests/baseline_images/
%{python3_sitearch}/mpl_toolkits/tests/baseline_images/

%files -n python3-matplotlib-qt4
%{python3_sitearch}/matplotlib/backends/{backend_qt4.*,__pycache__/backend_qt4.*}
%{python3_sitearch}/matplotlib/backends/{backend_qt4agg.*,__pycache__/backend_qt4agg.*}

%files -n python3-matplotlib-qt5
%{python3_sitearch}/matplotlib/backends/{backend_qt5.*,__pycache__/backend_qt5.*}
%{python3_sitearch}/matplotlib/backends/{backend_qt5agg.*,__pycache__/backend_qt5agg.*}

%files -n python3-matplotlib-gtk3
%{python3_sitearch}/matplotlib/backends/{backend_gtk*,__pycache__/backend_gtk*}

%files -n python3-matplotlib-tk
%{python3_sitearch}/matplotlib/backends/{backend_tkagg.py*,__pycache__/backend_tkagg.*}
%{python3_sitearch}/matplotlib/backends/{tkagg.*,__pycache__/tkagg.*,_tkagg.*}

%changelog
* Fri Feb 19 2021 liyanan <liyanan32@huawei.com> - 2.2.4-3
- remove python2 dependency

* Fri Mar 6 2020 chenli <chenli147@huawei.com> - 2.2.4-2
- Init Package
