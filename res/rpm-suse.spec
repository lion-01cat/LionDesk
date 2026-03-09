Name:       liondesk
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1 xdotool

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/liondesk/
mkdir -p %{buildroot}/usr/share/liondesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/liondesk %{buildroot}/usr/bin/liondesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/liondesk/libsciter-gtk.so
install $HBB/res/liondesk.service %{buildroot}/usr/share/liondesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/liondesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/liondesk.svg
install $HBB/res/liondesk.desktop %{buildroot}/usr/share/liondesk/files/
install $HBB/res/liondesk-link.desktop %{buildroot}/usr/share/liondesk/files/

%files
/usr/bin/liondesk
/usr/share/liondesk/libsciter-gtk.so
/usr/share/liondesk/files/liondesk.service
/usr/share/icons/hicolor/256x256/apps/liondesk.png
/usr/share/icons/hicolor/scalable/apps/liondesk.svg
/usr/share/liondesk/files/liondesk.desktop
/usr/share/liondesk/files/liondesk-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop liondesk || true
  ;;
esac

%post
cp /usr/share/liondesk/files/liondesk.service /etc/systemd/system/liondesk.service
cp /usr/share/liondesk/files/liondesk.desktop /usr/share/applications/
cp /usr/share/liondesk/files/liondesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable liondesk
systemctl start liondesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop liondesk || true
    systemctl disable liondesk || true
    rm /etc/systemd/system/liondesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/liondesk.desktop || true
    rm /usr/share/applications/liondesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
