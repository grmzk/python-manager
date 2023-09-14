Name:           python-manager
Version:        0.2
Release:        alt1

Summary:        Python installation and update manager
License:        GPLv3+

Group:          Other
BuildArch:      noarch

URL:            https://github.com/grmzk/python-manager

BuildRequires:  rpm-build-python3

Requires:       bash
Requires:       coreutils
Requires:       eepm
Requires:       hasher
Requires:       rpm-build
Requires:       python3
Requires:       python3-module-dotenv
Requires:       python3-module-requests
Requires:       sed
Requires:       wget

%description
Manager for installing or updating different versions 
of the python interpreters on the same computer


%define SrcDir  %{name}-%{version}

%prep
rm -rf %{SrcDir}
git clone %{url}.git %{SrcDir}
cd %{SrcDir}


%install
cd %{SrcDir}
mkdir -pv %buildroot/%python3_sitelibdir_noarch/%name/actions
mkdir -pv %buildroot/%python3_sitelibdir_noarch/%name/altlinux
mkdir -pv %buildroot/%python3_sitelibdir_noarch/%name/checkers
mkdir -pv %buildroot/%python3_sitelibdir_noarch/%name/versions
mkdir -pv %buildroot/%_bindir
install -Dm0755 main.py \
                %buildroot/%python3_sitelibdir_noarch/%name/
install -Dm0755 altlinux/python3-build.altlinux.sh \
                %buildroot/%python3_sitelibdir_noarch/%name/altlinux/
install -Dm0644 altlinux/python3.altlinux.spec.template \
                %buildroot/%python3_sitelibdir_noarch/%name/altlinux/
install -Dm0644 actions/*.py \
                %buildroot/%python3_sitelibdir_noarch/%name/actions/
install -Dm0644 checkers/*.py \
                %buildroot/%python3_sitelibdir_noarch/%name/checkers/
install -Dm0644 versions/*.py \
                %buildroot/%python3_sitelibdir_noarch/%name/versions/
ln -sv %python3_sitelibdir_noarch/%name/main.py \
       %buildroot/%_bindir/python-manager


%files
%python3_sitelibdir_noarch/%name/*.py
%python3_sitelibdir_noarch/%name/altlinux/*.sh
%python3_sitelibdir_noarch/%name/altlinux/*.spec.template
%python3_sitelibdir_noarch/%name/actions/*.py
%python3_sitelibdir_noarch/%name/checkers/*.py
%python3_sitelibdir_noarch/%name/versions/*.py
%_bindir/python-manager


%changelog
* Thu Sep 14 2023 Igor Muzyka <muzyka-iv@yandex.ru> 0.2-alt1
- added argument --last-versions

* Wed Sep 06 2023 Igor Muzyka <muzyka-iv@yandex.ru> 0.1-alt1
- Init

