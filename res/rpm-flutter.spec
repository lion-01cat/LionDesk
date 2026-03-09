Name:       liondesk
Version:    1.4.6
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://liondesk.com
Vendor:     liondesk <info@liondesk.com>
Requires:   gtk3 libxcb libXfixes alsa-lib libva pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/liondesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/liondesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/liondesk.service -t "%{buildroot}/usr/share/liondesk/files"
install -Dm 644 $HBB/res/liondesk.desktop -t "%{buildroot}/usr/share/liondesk/files"
install -Dm 644 $HBB/res/liondesk-link.desktop -t "%{buildroot}/usr/share/liondesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/liondesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/liondesk.svg"

%files
/usr/share/liondesk/*
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
ln -sf /usr/share/liondesk/liondesk /usr/bin/liondesk
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
    rm /usr/bin/liondesk || true
    rmdir /usr/lib/liondesk || true
    rmdir /usr/local/liondesk || true
    rmdir /usr/share/liondesk || true
    rm /usr/share/applications/liondesk.desktop || true
    rm /usr/share/applications/liondesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/liondesk || true
    rmdir /usr/local/liondesk || true
  ;;
esac
