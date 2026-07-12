from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QSpinBox,
    QVBoxLayout,
)


class SimpleFormDialog(QDialog):
    def __init__(self, title: str, fields: list[dict[str, Any]], parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(460, 520)
        self._widgets: dict[str, Any] = {}

        layout = QVBoxLayout(self)
        header = QLabel(title)
        header.setObjectName("Title")
        layout.addWidget(header)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignTop)
        form.setSpacing(12)
        for field in fields:
            widget = self._build_widget(field)
            self._widgets[field["name"]] = widget
            form.addRow(field["label"], widget)
        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _build_widget(self, field: dict[str, Any]):
        field_type = field.get("type", "text")
        if field_type == "text":
            widget = QLineEdit(str(field.get("value", "")))
            widget.setPlaceholderText(field.get("placeholder", ""))
            if field.get("password"):
                widget.setEchoMode(QLineEdit.Password)
            return widget
        if field_type == "multiline":
            widget = QPlainTextEdit(str(field.get("value", "")))
            widget.setPlaceholderText(field.get("placeholder", ""))
            widget.setMaximumHeight(120)
            return widget
        if field_type == "select":
            widget = QComboBox()
            for value, label in field.get("options", []):
                widget.addItem(label, value)
            default = field.get("value")
            if default is not None:
                index = widget.findData(default)
                if index >= 0:
                    widget.setCurrentIndex(index)
            return widget
        if field_type == "int":
            widget = QSpinBox()
            widget.setRange(field.get("min", 0), field.get("max", 999999))
            widget.setValue(field.get("value", 0))
            return widget
        if field_type == "float":
            widget = QDoubleSpinBox()
            widget.setDecimals(field.get("decimals", 0))
            widget.setRange(field.get("min", 0.0), field.get("max", 999999999.0))
            widget.setValue(field.get("value", 0.0))
            widget.setSingleStep(field.get("step", 1000.0))
            return widget
        if field_type == "bool":
            widget = QCheckBox()
            widget.setChecked(bool(field.get("value", False)))
            return widget
        raise ValueError(f"Unsupported field type: {field_type}")

    def values(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for name, widget in self._widgets.items():
            if isinstance(widget, QLineEdit):
                data[name] = widget.text().strip()
            elif isinstance(widget, QPlainTextEdit):
                data[name] = widget.toPlainText().strip()
            elif isinstance(widget, QComboBox):
                data[name] = widget.currentData()
            elif isinstance(widget, QSpinBox):
                data[name] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                data[name] = widget.value()
            elif isinstance(widget, QCheckBox):
                data[name] = widget.isChecked()
        return data
