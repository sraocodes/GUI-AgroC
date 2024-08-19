import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, 
                             QCheckBox, QDateEdit, QSpinBox, QComboBox, 
                             QPushButton, QTableWidget, QFileDialog, QMessageBox,
                             QTableWidgetItem, QScrollArea, QLabel)
from PyQt5.QtCore import Qt, QDate

class AgroCInputEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AgroC Input Editor")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_menu_bar()
        self.create_tabs()
        self.create_bottom_buttons()

        self.default_file = "plants.in"
        self.modified_file = "plants_mod.in"
        self.load_default_values()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("Reset to Default", self.reset_to_default)
        file_menu.addAction("Save Changes", self.save_changes)
        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction("About", self.show_about)

    def create_tabs(self):
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.create_general_settings_tab()
        self.create_plant_type_tab()
        self.create_tables_tab()

    def create_general_settings_tab(self):
        scroll = QScrollArea()
        tab = QWidget()
        layout = QFormLayout(tab)

        self.version_input = QLineEdit()
        layout.addRow("Version number:", self.version_input)

        self.co2_fluxes = QCheckBox("CO2 fluxes")
        self.respiration = QCheckBox("Respiration")
        self.maint_growth = QCheckBox("Maint growth")
        self.waterstress = QCheckBox("Waterstress")
        self.root_exudation = QCheckBox("Root exudation")
        self.root_death = QCheckBox("Root death")
        self.harvest_residues = QCheckBox("Harvest residues")
        self.farquhar = QCheckBox("Farquhar")
        
        layout.addRow(self.co2_fluxes)
        layout.addRow(self.respiration)
        layout.addRow(self.maint_growth)
        layout.addRow(self.waterstress)
        layout.addRow(self.root_exudation)
        layout.addRow(self.root_death)
        layout.addRow(self.harvest_residues)
        layout.addRow(self.farquhar)

        self.daily_timestep = QCheckBox("Daily timestep")
        layout.addRow(self.daily_timestep)

        self.start_date = QDateEdit()
        self.start_date.setDisplayFormat("yyyy MM dd")
        layout.addRow("Start date:", self.start_date)

        self.num_plant_types = QSpinBox()
        self.num_plant_types.setMinimum(1)
        self.num_plant_types.valueChanged.connect(self.update_plant_type_tabs)
        layout.addRow("Number of plant types:", self.num_plant_types)

        self.unit_soilco2 = QComboBox()
        self.unit_soilco2.addItems(["mm", "cm", "dm", "m", "km"])
        layout.addRow("Unit in SOILCO2:", self.unit_soilco2)

        self.interception_model = QComboBox()
        self.interception_model.addItems(["Bormann", "Hoyningen-Huene"])
        layout.addRow("Interception model:", self.interception_model)

        self.latitude = QLineEdit()
        layout.addRow("Latitude:", self.latitude)

        scroll.setWidget(tab)
        scroll.setWidgetResizable(True)
        self.tab_widget.addTab(scroll, "General Settings")

    def create_plant_type_tab(self):
        self.plant_type_tabs = QTabWidget()
        self.tab_widget.addTab(self.plant_type_tabs, "Plant Types")

    def update_plant_type_tabs(self, num_types):
        while self.plant_type_tabs.count() > num_types:
            self.plant_type_tabs.removeTab(self.plant_type_tabs.count() - 1)
        while self.plant_type_tabs.count() < num_types:
            self.add_plant_type_tab(self.plant_type_tabs.count() + 1)

    def add_plant_type_tab(self, plant_num):
        scroll = QScrollArea()
        tab = QWidget()
        layout = QFormLayout(tab)

        params = [
            "Plant type name", "Table rows", "Planting/emergence and harvests",
            "Number of parameters", "Kc calculation", "Senescence start", "Senescence end",
            "p0", "p1", "p2h", "p2l", "p3", "CERES temperatures", "CERES photoperiod",
            "CERES maximum development rate", "RNA_MAX", "ROOT_MAX", "ROOT_INIT",
            "EXU_FACT", "DEATHFACMAX", "NSL", "RGR", "TEMPBASE", "SLA", "RSLA",
            "AMX", "EFF", "RKDF", "SCP", "RMAINSO", "ASRQSO", "TEMPSTART",
            "DEBR_FAC", "LS", "RLAICR", "EAI", "RMATR", "SSL", "SRW", "SLAID_OFF"
        ]

        self.plant_params = {}
        for param in params:
            self.plant_params[param] = QLineEdit()
            layout.addRow(f"{param}:", self.plant_params[param])

        # Add emergence and harvest dates
        self.emergence_harvest_dates = QLineEdit()
        layout.addRow("Emergence and harvest dates:", self.emergence_harvest_dates)

        scroll.setWidget(tab)
        scroll.setWidgetResizable(True)
        self.plant_type_tabs.addTab(scroll, f"Plant Type {plant_num}")

    def create_tables_tab(self):
        scroll = QScrollArea()
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.tables = []
        for i in range(1, 18):
            table = QTableWidget(5, 2)  # Start with 5 rows, 2 columns
            table.setHorizontalHeaderLabels(["Column 1", "Column 2"])
            layout.addWidget(QLabel(f"Table {i}"))
            layout.addWidget(table)
            self.tables.append(table)

        scroll.setWidget(tab)
        scroll.setWidgetResizable(True)
        self.tab_widget.addTab(scroll, "Tables")

    def create_bottom_buttons(self):
        button_layout = QHBoxLayout()
        reset_button = QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_to_default)
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(save_button)
        self.layout.addLayout(button_layout)

    def load_default_values(self):
        if os.path.exists(self.default_file):
            self.load_file(self.default_file)
        else:
            QMessageBox.warning(self, "File Not Found", f"Default file '{self.default_file}' not found. Starting with empty values.")

    def load_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

            # Parse general settings
            self.version_input.setText(lines[1].split()[0])
            
            # Parse boolean settings
            bool_settings = lines[2].split()
            self.co2_fluxes.setChecked(bool_settings[0].lower() == 't')
            self.respiration.setChecked(bool_settings[1].lower() == 't')
            self.maint_growth.setChecked(bool_settings[2].lower() == 't')
            self.waterstress.setChecked(bool_settings[3].lower() == 't')
            self.root_exudation.setChecked(bool_settings[4].lower() == 't')
            self.root_death.setChecked(bool_settings[5].lower() == 't')
            self.harvest_residues.setChecked(bool_settings[6].lower() == 't')
            self.farquhar.setChecked(bool_settings[7].lower() == 't')

            self.daily_timestep.setChecked(lines[4].strip().lower().startswith('t'))

            # Parse start date
            start_date = lines[5].split()[:3]
            self.start_date.setDate(QDate(int(start_date[0]), int(start_date[1]), int(start_date[2])))

            self.num_plant_types.setValue(int(lines[6].split()[0]))
            self.unit_soilco2.setCurrentIndex(int(lines[7].split()[0]) - 1)
            self.interception_model.setCurrentIndex(int(lines[8].split()[0]) - 1)
            self.latitude.setText(lines[9].split()[0])

            # Parse plant types
            plant_start = lines.index("# plant type 1 **************************************************\n")
            for i in range(self.num_plant_types.value()):
                plant_data = lines[plant_start + 1:]
                self.load_plant_type(i, plant_data)
                plant_start = plant_start + plant_data.index("# (Tab.1)\n")

            # Parse tables
            table_start = lines.index("# (Tab.1)\n")
            for i, table in enumerate(self.tables):
                if i < 16:
                    table_end = lines.index(f"# (Tab.{i+2})\n")
                else:
                    try:
                        table_end = lines.index("# plant type")
                    except ValueError:
                        table_end = len(lines)
                table_data = lines[table_start + 1:table_end]
                self.load_table(i, table_data)
                table_start = table_end

        except Exception as e:
            print(f"An error occurred while loading the file: {str(e)}")
            import traceback
            traceback.print_exc()

    def load_plant_type(self, index, data):
        if index >= self.plant_type_tabs.count():
            self.add_plant_type_tab(index + 1)
        
        tab = self.plant_type_tabs.widget(index)
        content_widget = tab.findChild(QScrollArea).widget()
        layout = content_widget.layout()

        if layout is None:
            print(f"Error: Could not find layout for plant type {index + 1}")
            return

        # Load plant type name and table rows
        layout.itemAt(1).widget().setText(data[0].strip())
        layout.itemAt(3).widget().setText(" ".join(data[1].split()[:-7]))

        # Load other parameters
        for i, line in enumerate(data[2:]):
            if i + 2 < layout.rowCount() - 1:  # -1 for emergence/harvest dates
                widget = layout.itemAt((i + 2) * 2 + 1).widget()
                if isinstance(widget, QLineEdit):
                    widget.setText(line.split('#')[0].strip())
            else:
                print(f"Warning: More data than fields for plant type {index + 1}")
                break

        # Load emergence and harvest dates
        emergence_harvest_index = data.index("# emergence und harvest date(s)\n")
        self.emergence_harvest_dates.setText(data[emergence_harvest_index + 1].strip())

    def load_table(self, index, data):
        table = self.tables[index]
        table.setRowCount(len(data))
        for row, line in enumerate(data):
            values = line.strip().split()
            for col, value in enumerate(values):
                table.setItem(row, col, QTableWidgetItem(value))

    def reset_to_default(self):
        self.load_default_values()
        QMessageBox.information(self, "Reset Complete", "All values have been reset to default.")

    def save_changes(self):
        self.generate_plants_in(self.modified_file)
        QMessageBox.information(self, "Save Complete", f"Changes have been saved to {self.modified_file}")

    def generate_plants_in(self, filename):
        with open(filename, 'w') as file:
            # Write general settings
            file.write("soilco2 plant input\n")
            file.write(f"{self.version_input.text()} version number\n")
            
            # Write boolean settings
            bool_settings = [
                'T' if self.co2_fluxes.isChecked() else 'F',
                'T' if self.respiration.isChecked() else 'F',
                'T' if self.maint_growth.isChecked() else 'F',
                'T' if self.waterstress.isChecked() else 'F',
                'T' if self.root_exudation.isChecked() else 'F',
                'T' if self.root_death.isChecked() else 'F',
                'T' if self.harvest_residues.isChecked() else 'F',
                'T' if self.farquhar.isChecked() else 'F'
            ]
            file.write("CO2_fluxes   respiration   maint_growth   waterstress   rootExudation   rootDeath   harvestresidues   farquhar\n")
            file.write("     " + "     ".join(bool_settings) + "\n")
            
            file.write("T " if self.daily_timestep.isChecked() else "F ")
            file.write("daily timestep (T = daily, F = hourly)\n")
            
            file.write(f"{self.start_date.date().toString('yyyy MM dd')}  start date of the simulation ( yyyy mm dd )\n")
            file.write(f"{self.num_plant_types.value()}  no of plant types\n")
            file.write(f"{self.unit_soilco2.currentIndex() + 1}  unit in SOILCO2 1=mm 2=cm 3=dm 4=m 5=km\n")
            file.write(f"{self.interception_model.currentIndex() + 1}  interception 1=Bormann, 2=Hoyningen-Huene\n")
            file.write(f"{self.latitude.text()}  latitude of the site                                                 (LATITUDE)\n")

            # Write plant type data
            for i in range(self.num_plant_types.value()):
                file.write(f"# plant type {i+1} **************************************************\n")
                tab = self.plant_type_tabs.widget(i)
                content_widget = tab.findChild(QScrollArea).widget()
                layout = content_widget.layout()

                # Write plant type name and table rows
                file.write(f"{layout.itemAt(1).widget().text()}\n")
                file.write(f"{layout.itemAt(3).widget().text()} {self.count_table_rows()}   number of rows in the 17 tables\n")

                # Write other parameters
                for j in range(2, layout.rowCount() - 1):  # -1 for emergence/harvest dates
                    label = layout.itemAt(j * 2).widget().text().strip(':')
                    value = layout.itemAt(j * 2 + 1).widget().text()
                    file.write(f"{value}  {label}\n")

                # Write emergence and harvest dates
                file.write("# emergence und harvest date(s)\n")
                file.write(f"{self.emergence_harvest_dates.text()}\n")

            # Write tables
            for i, table in enumerate(self.tables):
                file.write(f"# (Tab.{i+1})\n")
                for row in range(table.rowCount()):
                    row_data = []
                    for col in range(table.columnCount()):
                        item = table.item(row, col)
                        row_data.append(item.text() if item else "")
                    file.write("  ".join(row_data) + "\n")

    def count_table_rows(self):
        """Count the number of rows in each table and return as a space-separated string."""
        return " ".join(str(table.rowCount()) for table in self.tables)

    def show_about(self):
        QMessageBox.about(self, "About AgroC Input Editor",
                          "AgroC Input Editor\n\n"
                          "This application allows you to edit AgroC input files (plants.in) "
                          "with a user-friendly interface. It loads default values from 'plants.in' "
                          "and saves modifications to 'plants_mod.in'.\n\n"
                          "Developed for AgroC project.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AgroCInputEditor()
    window.show()
    sys.exit(app.exec_())