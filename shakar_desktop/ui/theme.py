APP_STYLE = """
QWidget {
    background: #0f172a;
    color: #e2e8f0;
    font-family: Segoe UI, Tahoma;
    font-size: 12px;
}
QMainWindow, QDialog {
    background: #0b1220;
}
QFrame#Card {
    background: #111c33;
    border: 1px solid #1f2d48;
    border-radius: 14px;
}
QFrame#Sidebar {
    background: #08101f;
    border-left: 1px solid #17253c;
}
QLabel#Title {
    font-size: 22px;
    font-weight: 700;
    color: #f8fafc;
}
QLabel#Subtitle {
    color: #94a3b8;
    font-size: 12px;
}
QPushButton {
    background: #1d4ed8;
    border: none;
    border-radius: 10px;
    padding: 10px 16px;
    color: white;
    font-weight: 600;
}
QPushButton:hover { background: #2563eb; }
QPushButton:pressed { background: #1e40af; }
QPushButton[variant="secondary"] { background: #17253c; color: #cbd5e1; }
QPushButton[variant="ghost"] { background: transparent; border: 1px solid #26364f; color: #cbd5e1; }
QPushButton[variant="danger"] { background: #b91c1c; }
QPushButton#SidebarButton {
    text-align: right;
    background: transparent;
    border: 1px solid transparent;
    color: #cbd5e1;
    padding: 12px 16px;
    border-radius: 12px;
}
QPushButton#SidebarButton:hover, QPushButton#SidebarButton:checked {
    background: #16233a;
    border-color: #24406a;
    color: #ffffff;
}
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
    background: #0f1b31;
    border: 1px solid #22324b;
    border-radius: 10px;
    padding: 8px;
    color: #e2e8f0;
}
QTableWidget {
    background: #0f1b31;
    gridline-color: #23324a;
    border: 1px solid #22324b;
    border-radius: 12px;
    alternate-background-color: #13213a;
}
QHeaderView::section {
    background: #17253c;
    color: #f8fafc;
    border: none;
    padding: 10px;
    font-weight: 700;
}
QScrollArea, QScrollArea > QWidget > QWidget { border: none; }
QMessageBox {
    background: #0b1220;
}
"""
