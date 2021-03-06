from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

import os
import sys


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("My_WEB")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://ya.ru"))

        self.tabs = QTabWidget()

    self.tabs.setDocumentMode(True)
    self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
    self.tabs.currentChanged.connect(self.current_tab_changed)
    self.tabs.setTabsClosable(True)
    self.tabs.tabCloseRequested.connect(self.close_current_tab)

    self.browser.urlChanged.connect(self.update_urlbar)
    self.browser.loadFinished.connect(self.update_title)
    self.setCentralWidget(self.browser)

    self.status = QStatusBar()
    self.setStatusBar(self.status)

    navtb = QToolBar("Navigation")
    navtb.setIconSize(QSize(16, 16))
    self.addToolBar(navtb)

    back_btn = QAction(QIcon(os.path.join('images_PyQt', 'arrow-180.png')), "Back", self)
    back_btn.setStatusTip("Back to previous page")
    back_btn.triggered.connect(self.browser.back)
    navtb.addAction(back_btn)

    next_btn = QAction(QIcon(os.path.join('images_PyQt', 'arrow-000.png')), "Forward", self)
    next_btn.setStatusTip("Forward to next page")
    next_btn.triggered.connect(self.browser.forward)
    navtb.addAction(next_btn)

    reload_btn = QAction(QIcon(os.path.join('images_PyQt', 'arrow-circle-315.png')), "Reload", self)
    reload_btn.setStatusTip("Reload page")
    reload_btn.triggered.connect(self.browser.reload)
    navtb.addAction(reload_btn)

    home_btn = QAction(QIcon(os.path.join('images_PyQt', 'home.png')), "Home", self)
    home_btn.setStatusTip("Go home")
    home_btn.triggered.connect(self.navigate_home)
    navtb.addAction(home_btn)

    navtb.addSeparator()

    self.httpsicon = QLabel()  # Yes, really!
    self.httpsicon.setPixmap(QPixmap(os.path.join('images_PyQt', 'lock-nossl.png')))
    navtb.addWidget(self.httpsicon)

    self.urlbar = QLineEdit()
    self.urlbar.returnPressed.connect(self.navigate_to_url)
    navtb.addWidget(self.urlbar)

    new_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Tab", self)


new_tab_action.setStatusTip("Open a new tab")
new_tab_action.triggered.connect(lambda _: self.add_new_tab())

self.show()


def add_new_tab(self, qurl=None, label="Blank"):


if qurl is None:
    qurl = QUrl('')

browser = QWebEngineView()
browser.setUrl(qurl)
i = self.tabs.addTab(browser, label)

self.tabs.setCurrentIndex(i)

# More difficult! We only want to update the url when it's from the
# correct tab
browser.urlChanged.connect(lambda qurl, browser=browser:
                           self.update_urlbar(qurl, browser))

browser.loadFinished.connect(lambda _, i=i, browser=browser:
                             self.tabs.setTabText(i, browser.page().title()))


def tab_open_doubleclick(self, i):
    if i == -1:  # No tab under the click
        self.add_new_tab()


def current_tab_changed(self, i):
    qurl = self.tabs.currentWidget().url()
    self.update_urlbar(qurl, self.tabs.currentWidget())
    self.update_title(self.tabs.currentWidget())


def close_current_tab(self, i):
    if self.tabs.count() < 2:
        return

    self.tabs.removeTab(i)
    self.setWindowIcon(QIcon(os.path.join('images_PyQt', 'ma-icon-64.png')))


def update_title(self):
    title = self.browser.page().title()

    self.setWindowTitle("%s - My WEB" % title)


def navigate_mozarella(self):
    self.browser.setUrl(QUrl("https://ya.ru"))


def about(self):
    dlg = AboutDialog()
    dlg.exec_()


def open_file(self):
    filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                              "Hypertext Markup Language (*.htm *.html);;"
                                              "All files (*.*)")

    if filename:
        with open(filename, 'r') as f:
            html = f.read()

        self.browser.setHtml(html)
        self.urlbar.setText(filename)


def save_file(self):
    filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                              "Hypertext Markup Language (*.htm *html);;"
                                              "All files (*.*)")

    if filename:
        html = self.browser.page().toHtml()
        with open(filename, 'w') as f:
            f.write(html)


def print_page(self):
    dlg = QPrintPreviewDialog()
    dlg.paintRequested.connect(self.browser.print_)
    dlg.exec_()


def navigate_home(self):
    self.browser.setUrl(QUrl("http://ya.ru"))


def navigate_to_url(self):  # Does not receive the Url
    q = QUrl(self.urlbar.text())
    if q.scheme() == "":
        q.setScheme("http")

    self.browser.setUrl(q)


def update_urlbar(self, q):
    if q.scheme() == 'https':
        # Secure padlock icon
        self.httpsicon.setPixmap(QPixmap(os.path.join('images_PyQt', 'lock-ssl.png')))

    else:
        # Insecure padlock icon
        self.httpsicon.setPixmap(QPixmap(os.path.join('images_PyQt', 'lock-nossl.png')))

    self.urlbar.setText(q.toString())
    self.urlbar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("WEB GUI")

window = MainWindow()

app.exec_()
