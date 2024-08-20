import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QLineEdit, QCheckBox, QDateEdit, QSpinBox, QComboBox,
                             QPushButton, QFileDialog, QMessageBox, QScrollArea, QLabel, QTabWidget,
                             QTextEdit, QGroupBox)
from PyQt5.QtCore import Qt, QDate

class AgroCInputEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AgroC Plants.in Input Editor")
        self.setGeometry(100, 100, 800, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.create_general_tab()
        self.create_plant_params_tab()
        self.create_additional_params_tab()
        self.create_buttons()

        self.default_file = "plants.in"
        self.modified_file = "plants_mod.in"
        self.load_default_values()

    def create_general_tab(self):
        tab = QScrollArea()
        content = QWidget()
        form_layout = QFormLayout(content)

        # Add existing fields for general parameters
        self.version_input = QLineEdit()
        form_layout.addRow("Software Version:", self.version_input)

        # Add other existing fields...

        tab.setWidget(content)
        tab.setWidgetResizable(True)
        self.tab_widget.addTab(tab, "General")

    def create_plant_params_tab(self):
        tab = QScrollArea()
        content = QWidget()
        form_layout = QFormLayout(content)

        # Add existing fields for plant parameters
        self.plant_type_name = QLineEdit()
        form_layout.addRow("Plant Type Name:", self.plant_type_name)

        # Add other existing fields...

        tab.setWidget(content)
        tab.setWidgetResizable(True)
        self.tab_widget.addTab(tab, "Plant Parameters")

    def create_additional_params_tab(self):
        tab = QScrollArea()
        content = QWidget()
        layout = QVBoxLayout(content)

        # Create input areas for each table
        self.table_inputs = {}
        for i in range(1, 18):
            group_box = QGroupBox(f"Table {i}")
            group_layout = QVBoxLayout()
            text_edit = QTextEdit()
            self.table_inputs[i] = text_edit
            group_layout.addWidget(text_edit)
            group_box.setLayout(group_layout)
            layout.addWidget(group_box)

        tab.setWidget(content)
        tab.setWidgetResizable(True)
        self.tab_widget.addTab(tab, "Additional Parameters")

    def create_buttons(self):
        button_layout = QHBoxLayout()
        reset_button = QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_to_default)
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(save_button)
        self.layout.addLayout(button_layout)

    def load_default_values(self):
        try:
            self.load_file(self.default_file)
        except Exception as e:
            QMessageBox.critical(self, "Error Loading Defaults", f"An error occurred while loading the default settings: {str(e)}")

    def load_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

            # Load existing parameters
            self.version_input.setText(lines[1].split()[0])
            # Load other existing parameters...

            # Load additional parameters (tables)
            current_table = 0
            table_content = []
            for line in lines[48:]:  # Start from line 49
                if line.startswith("# (Tab."):
                    if current_table > 0:
                        self.table_inputs[current_table].setPlainText('\n'.join(table_content))
                        table_content = []
                    current_table = int(line.split('.')[1].split(')')[0])
                elif current_table > 0:
                    table_content.append(line.strip())

            # Set the content of the last table
            if current_table > 0:
                self.table_inputs[current_table].setPlainText('\n'.join(table_content))

        except Exception as e:
            print(f"An error occurred while loading the file: {str(e)}")
            import traceback
            traceback.print_exc()

    def reset_to_default(self):
        self.load_default_values()
        QMessageBox.information(self, "Reset Complete", "All values have been reset to default.")

    def save_changes(self):
        self.generate_plants_in(self.modified_file)
        QMessageBox.information(self, "Save Complete", f"Changes have been saved to {self.modified_file}")

    def generate_plants_in(self, filename):
        with open(filename, 'w') as file:
            # Write existing parameters
            file.write("soilco2 plant input\n")
            file.write(f"{self.version_input.text()}  version number\n")

            bool_settings = ['T' if checkbox.isChecked() else 'F' for checkbox in self.bool_settings.values()]
            file.write("CO2_fluxes   respiration   maint_growth   waterstress   rootExudation   rootDeath   harvestresidues   farquhar\n")
            file.write("     " + "     ".join(bool_settings) + "\n")

            file.write("T " if self.daily_timestep.isChecked() else "F ")
            file.write("daily timestep (T = daily, F = hourly)\n")

            file.write(f"{self.start_date.date().toString('yyyy MM dd')}  start date of the simulation ( yyyy mm dd )\n")
            file.write(f"{self.num_plant_types.value()}  no of plant types\n")
            file.write(f"{self.unit_soilco2.currentIndex() + 1}  unit in SOILCO2 1=mm 2=cm 3=dm 4=m 5=km\n")
            file.write(f"{self.interception_model.currentIndex() + 1}  interception 1=Bormann, 2=Hoyningen-Huene\n")
            file.write(f"{self.latitude.text()}  latitude of the site                                                 (LATITUDE)\n")

            file.write("# plant type 1 **************************************************\n")
            file.write(f"{self.plant_type_name.text()}\n")
            file.write(f"{self.table_rows.text()}   number of rows in the 17 tables\n")
            file.write(f"{self.planting_dates.text()}  no of dates for planting/emergence and harvests\n")
            file.write(f"{self.num_parameters.text()} no of parameters\n")
            file.write(f"{self.kc_calculation.text()}  Kc calculation 1=dvs  2=time 3=computed from LAI                             (AKCTYPE)\n")
            file.write(f"{self.senescence.text()}   tstart, tend for senescence (day of year, i.e. Julian Date)\n")
            file.write(f"{self.p_values.text()}  p0, p1, p2h, p2l, p3 (mm)\n")
            file.write(f"{self.ceres_temperatures.text()}  CERES: temperatures (C) (first number: flag for 1=new or 0=old Model)\n")
            file.write(f"{self.ceres_photoperiod.text()}  CERES: photoperiod: Popt, Pcrit (h), omega (h(-1))\n")
            file.write(f"{self.ceres_max_dev_rate.text()}  CERES: maximum development rate (h(-1))                          (RMAX)\n")

            file.write(f"{self.rna_max.text()}     + max depth above there is no root water uptake (mm)                  (RNA_MAX)\n")
            file.write(f"{self.root_max.text()}      + max rooting depth (mm)                                    (ROOT_MAX)\n")
            file.write(f"{self.root_init.text()}     + initial rooting depth (mm)                                          (ROOT_INIT)\n")
            file.write(f"{self.exu_fact.text()}      + exudation factor                                                    (EXU_FACT)\n")
            file.write(f"{self.deathfacmax.text()}    + max factor used for deathfac                                        (DEATHFACMAX)\n")
            file.write(f"{self.nsl.text()}       + number of seedlings per m2                                          (NSL)\n")
            file.write(f"{self.rgr.text()}     + relative growth rate during exponential leaf area growth (ha/ha/C/d) (RGR)\n")
            file.write(f"{self.tempbase.text()}       + base temperature for juvenile leaf area growth (C)                  (TEMPBASE)\n")
            file.write(f"{self.sla.text()}    + specific leaf area of new leaves (ha leaf/kg DM)                    (SLA)\n")
            file.write(f"{self.rsla.text()} + change of specific leaf area per unit thermal time (ha leaf/kg DM/C/d) (RSLA)\n")
            file.write(f"{self.amx.text()} 	  + potential CO2-assimilation rate of a unit leaf area for light saturation (kg CO2/ha leaf/h) (AMX)\n")
            file.write(f"{self.eff.text()}      + initial light use efficiency ((kg CO2/ha leaf/h)/(J/m2/s))          (EFF) (is changed from ha to L2 in plants.f90)\n")
            file.write(f"{self.rkdf.text()}      + extinction coefficient for diffuse PAR flux                         (RKDF)\n")
            file.write(f"{self.scp.text()}       + scattering coefficient of leaves for PAR                            (SCP)\n")
            file.write(f"{self.rmainso.text()}      + maintenance demand rate for storage organs per unit dry matter (kg CH2O/kg DM/d) (RMAINSO)\n")
            file.write(f"{self.asrqso.text()}      + conversion efficiency coefficient (assimilation requirement of DM for storage organs) (kg CH2O/kg DM) (ASRQSO)\n")
            file.write(f"{self.tempstart.text()}       + start temperature for plant growth (C*day) (crop 1: temp_sum from emergence till 31.Dec + tempstart for spring growth) (TEMPSTART)\n")
            file.write(f"{self.debr_fac.text()}      + dead LAI debris factor                                              (DEBR_FAC)\n")
            file.write(f"{self.ls.text()}      + LAI as switch from temperature to radiation-limited LAI expansion (ha/ha) (LS)\n")
            file.write(f"{self.rlaicr.text()}       + critical LAI for leaf death due to self shading (ha/ha)             (RLAICR)\n")
            file.write(f"{self.eai.text()}         + initial value of the ear area index (2sided) (crop 1-3,5)           (EAI)\n")
            file.write(f"{self.rmatr.text()}       + initial value of the maturity class (crop 4)                        (RMATR)\n")
            file.write(f"{self.ssl.text()}    + leaf area of one seedling (m2 leaf/seedling)                        (SSL)\n")
            file.write(f"{self.srw.text()}    + specific root weight (m/g)                                          (SRW)\n")
            file.write(f"{self.slaid_off.text()}       + dead leaf area for outside the season (ha/ha)                       (SLAID_OFF)\n")

            file.write("# emergence und harvest date(s)\n")
            file.write(f"{self.emergence_harvest_dates.text()}\n")

            # Write additional parameters (tables)
            for i in range(1, 18):
                file.write(f"# (Tab.{i})\n")
                file.write(self.table_inputs[i].toPlainText() + '\n')

        print(f"File saved successfully: {filename}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AgroCInputEditor()
    window.show()
    sys.exit(app.exec_())
