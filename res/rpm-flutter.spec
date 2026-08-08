Name:       4desk
Version:    1.4.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://github.com/Tarek-Bohdima/4desk
Vendor:     4desk <info@github.com/Tarek-Bohdima/4desk>
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

mkdir -p "%{buildroot}/usr/share/4desk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/4desk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/4desk.service -t "%{buildroot}/usr/share/4desk/files"
install -Dm 644 $HBB/res/4desk.desktop -t "%{buildroot}/usr/share/4desk/files"
install -Dm 644 $HBB/res/4desk-link.desktop -t "%{buildroot}/usr/share/4desk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/4desk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/4desk.svg"

%files
/usr/share/4desk/*
/usr/share/4desk/files/4desk.service
/usr/share/icons/hicolor/256x256/apps/4desk.png
/usr/share/icons/hicolor/scalable/apps/4desk.svg
/usr/share/4desk/files/4desk.desktop
/usr/share/4desk/files/4desk-link.desktop

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
    systemctl stop 4desk || true
  ;;
esac

%post
cp /usr/share/4desk/files/4desk.service /etc/systemd/system/4desk.service
cp /usr/share/4desk/files/4desk.desktop /usr/share/applications/
cp /usr/share/4desk/files/4desk-link.desktop /usr/share/applications/
ln -sf /usr/share/4desk/4desk /usr/bin/4desk
systemctl daemon-reload
systemctl enable 4desk
systemctl start 4desk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop 4desk || true
    systemctl disable 4desk || true
    rm /etc/systemd/system/4desk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/bin/4desk || true
    rmdir /usr/lib/4desk || true
    rmdir /usr/local/4desk || true
    rmdir /usr/share/4desk || true
    rm /usr/share/applications/4desk.desktop || true
    rm /usr/share/applications/4desk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/4desk || true
    rmdir /usr/local/4desk || true
  ;;
esac
