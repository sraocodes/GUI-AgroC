import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTabWidget, QScrollArea, QFormLayout, QGroupBox,
                             QTextEdit, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from datetime import datetime

class PlantInGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SOILCO2 plants.in Generator")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Create tabs
        self.create_general_tab()
        self.create_plant_params_tab()
        self.create_tables_tab()

        # Create generate button
        generate_button = QPushButton("Generate plants.in")
        generate_button.clicked.connect(self.generate_file)
        main_layout.addWidget(generate_button)

    def create_general_tab(self):
        tab = QWidget()
        layout = QFormLayout(tab)

        # Add fields for general parameters
        layout.addRow("Version number:", QLineEdit())
        layout.addRow("Start date (YYYY MM DD):", QLineEdit())
        layout.addRow("Number of plant types:", QLineEdit())
        layout.addRow("Unit in SOILCO2:", QLineEdit())
        layout.addRow("Interception model:", QLineEdit())
        layout.addRow("Latitude:", QLineEdit())

        self.tab_widget.addTab(tab, "General")

    def create_plant_params_tab(self):
        tab = QScrollArea()
        content = QWidget()
        layout = QFormLayout(content)

        # Add fields for plant parameters
        params = [
            "Plant type name", "Kc calculation", "Senescence start", "Senescence end",
            "p0", "p1", "p2h", "p2l", "p3", "RNA_MAX", "ROOT_MAX", "ROOT_INIT",
            "EXU_FACT", "DEATHFACMAX", "NSL", "RGR", "TEMPBASE", "SLA", "RSLA",
            "AMX", "EFF", "RKDF", "SCP", "RMAINSO", "ASRQSO", "TEMPSTART",
            "DEBR_FAC", "LS", "RLAICR", "EAI", "RMATR", "SSL", "SRW", "SLAID_OFF"
        ]

        for param in params:
            layout.addRow(f"{param}:", QLineEdit())

        tab.setWidget(content)
        tab.setWidgetResizable(True)
        self.tab_widget.addTab(tab, "Plant Parameters")

    def create_tables_tab(self):
        tab = QScrollArea()
        content = QWidget()
        layout = QVBoxLayout(content)

        # Add input areas for each table
        for i in range(1, 18):
            group_box = QGroupBox(f"Table {i}")
            group_layout = QVBoxLayout()
            text_edit = QTextEdit()
            text_edit.setObjectName(f"table_{i}")
            group_layout.addWidget(text_edit)
            group_box.setLayout(group_layout)
            layout.addWidget(group_box)

        tab.setWidget(content)
        tab.setWidgetResizable(True)
        self.tab_widget.addTab(tab, "Tables")

    def validate_inputs(self):
        errors = []

        # Validate General tab
        version = self.findChild(QLineEdit, "Version number:").text()
        if not version.isdigit():
            errors.append("Version number must be an integer.")

        start_date = self.findChild(QLineEdit, "Start date (YYYY MM DD):").text()
        try:
            datetime.strptime(start_date, "%Y %m %d")
        except ValueError:
            errors.append("Start date must be in the format YYYY MM DD.")

        latitude = self.findChild(QLineEdit, "Latitude:").text()
        try:
            lat = float(latitude)
            if not -90 <= lat <= 90:
                raise ValueError
        except ValueError:
            errors.append("Latitude must be a number between -90 and 90.")

        # Validate Plant Parameters tab
        rna_max = self.findChild(QLineEdit, "RNA_MAX:").text()
        try:
            rna_max = float(rna_max)
            if rna_max > 0:
                errors.append("RNA_MAX should be a negative number.")
        except ValueError:
            errors.append("RNA_MAX must be a number.")

        return errors

    def generate_plants_in(self):
        content = []

        # General section
        content.append(f"{self.findChild(QLineEdit, 'Version number:').text()}  version number")
        content.append("CO2_fluxes   respiration   maint_growth (output files)   waterstress   rootExudation   rootDeath   harvestresidues   farquhar")
        content.append("     f           f              f                            t              f                f            t           f      ")
        content.append("T daily timestep (T = daily, F = hourly)")
        content.append(f"{self.findChild(QLineEdit, 'Start date (YYYY MM DD):').text()}  start date of the simulation ( yyyy mm dd )")
        content.append(f"{self.findChild(QLineEdit, 'Number of plant types:').text()}  no of plant types")
        content.append(f"{self.findChild(QLineEdit, 'Unit in SOILCO2:').text()}  unit in SOILCO2 1=mm 2=cm 3=dm 4=m 5=km")
        content.append(f"{self.findChild(QLineEdit, 'Interception model:').text()}  interception 1=Bormann, 2=Hoyningen-Huene")
        content.append(f"{self.findChild(QLineEdit, 'Latitude:').text()}  latitude of the site                                                 (LATITUDE)")

        # Plant parameters section
        content.append("# plant type 1 **************************************************")
        content.append(f"{self.findChild(QLineEdit, 'Plant type name:').text()}")
        
        # Add more parameters...
        params = [
            "Kc calculation", "Senescence start", "Senescence end",
            "p0", "p1", "p2h", "p2l", "p3", "RNA_MAX", "ROOT_MAX", "ROOT_INIT",
            "EXU_FACT", "DEATHFACMAX", "NSL", "RGR", "TEMPBASE", "SLA", "RSLA",
            "AMX", "EFF", "RKDF", "SCP", "RMAINSO", "ASRQSO", "TEMPSTART",
            "DEBR_FAC", "LS", "RLAICR", "EAI", "RMATR", "SSL", "SRW", "SLAID_OFF"
        ]
        
        for param in params:
            content.append(f"{self.findChild(QLineEdit, param + ':').text()}  {param}")

        # Tables section
        for i in range(1, 18):
            content.append(f"# (Tab.{i})")
            table_content = self.findChild(QTextEdit, f"table_{i}").toPlainText()
            content.extend(table_content.split('\n'))

        return '\n'.join(content)

    def generate_file(self):
        errors = self.validate_inputs()
        if errors:
            error_message = "\n".join(errors)
            QMessageBox.warning(self, "Input Validation Error", error_message)
            return

        content = self.generate_plants_in()
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save plants.in", "", "Input Files (*.in);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as f:
                f.write(content)
            QMessageBox.information(self, "File Saved", f"plants.in file has been saved to {file_name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlantInGenerator()
    window.show()
    sys.exit(app.exec_())