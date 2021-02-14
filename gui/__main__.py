import sys
from os.path import dirname, join, realpath
import jinja2
from PySide2.QtWidgets import ( # type: ignore
   QApplication, QPushButton, QLabel,
   QLineEdit, QVBoxLayout, QWidget
)
from PySide2.QtGui import QTextDocument, QPixmap, QPainter, QColor # type: ignore
from .. import lookup

if __name__ == "__main__":

   instance = QApplication.instance()
   if instance is None:
      app = QApplication(sys.argv)
   else:
      app = instance

   path = realpath(join(dirname(__file__), "../templates"))
   templateLoader = jinja2.FileSystemLoader(searchpath=path)
   templateEnv = jinja2.Environment(loader=templateLoader)
   template = templateEnv.get_template("results.html")

   def f():
      doc = QTextDocument()
      tables = lookup(line.text())
      doc.setHtml(template.render(
         request={"script_root":""},
         tables=tables,
         url_for=lambda *_, **__: None
      ))
      doc.setTextWidth(doc.size().width())
      pixmap = QPixmap(doc.size().width(), doc.size().height())
      pixmap.fill(QColor(0, 0, 0, 0))
      painter = QPainter(pixmap)
      doc.drawContents(painter)
      painter.end()
      lab.setPixmap(pixmap)
      lab.setFixedSize(pixmap.size())

   qwid = QWidget()

   line = QLineEdit()

   but = QPushButton()
   but.setText("Претрага")
   but.clicked.connect(f)
   lab = QLabel()

   layout = QVBoxLayout()
   layout.addWidget(line)
   layout.addWidget(but)
   layout.addWidget(lab)
   qwid.setLayout(layout)
   qwid.show()

   sys.exit(app.exec_())
