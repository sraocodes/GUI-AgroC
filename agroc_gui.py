import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QLineEdit, QCheckBox, QDateEdit, QSpinBox, QComboBox,
                             QPushButton, QFileDialog, QMessageBox, QScrollArea, QLabel)
from PyQt5.QtCore import Qt, QDate

class AgroCInputEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AgroC Input Editor")
        self.setGeometry(100, 100, 800, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_form()
        self.create_buttons()

        self.default_file = "plants.in"
        self.modified_file = "plants_mod.in"
        self.load_default_values()

    def create_form(self):
        scroll = QScrollArea()
        form_widget = QWidget()
        self.form_layout = QFormLayout(form_widget)

        # General Settings
        self.version_input = QLineEdit()
        self.form_layout.addRow("Version number:", self.version_input)

        # Boolean settings
        self.bool_settings = {
            "CO2 fluxes": QCheckBox(),
            "Respiration": QCheckBox(),
            "Maint growth": QCheckBox(),
            "Waterstress": QCheckBox(),
            "Root exudation": QCheckBox(),
            "Root death": QCheckBox(),
            "Harvest residues": QCheckBox(),
            "Farquhar": QCheckBox()
        }
        for label, checkbox in self.bool_settings.items():
            self.form_layout.addRow(label, checkbox)

        self.daily_timestep = QCheckBox()
        self.form_layout.addRow("Daily timestep:", self.daily_timestep)

        self.start_date = QDateEdit()
        self.start_date.setDisplayFormat("yyyy MM dd")
        self.form_layout.addRow("Start date:", self.start_date)

        self.num_plant_types = QSpinBox()
        self.num_plant_types.setMinimum(1)
        self.form_layout.addRow("Number of plant types:", self.num_plant_types)

        self.unit_soilco2 = QComboBox()
        self.unit_soilco2.addItems(["mm", "cm", "dm", "m", "km"])
        self.form_layout.addRow("Unit in SOILCO2:", self.unit_soilco2)

        self.interception_model = QComboBox()
        self.interception_model.addItems(["Bormann", "Hoyningen-Huene"])
        self.form_layout.addRow("Interception model:", self.interception_model)

        self.latitude = QLineEdit()
        self.form_layout.addRow("Latitude:", self.latitude)

        # Plant Type 1 Settings
        self.form_layout.addRow(QLabel("Plant Type 1 Settings"))

        self.plant_type_name = QLineEdit()
        self.form_layout.addRow("Plant type name:", self.plant_type_name)

        self.table_rows = QLineEdit()
        self.form_layout.addRow("Table rows:", self.table_rows)

        self.planting_dates = QLineEdit()
        self.form_layout.addRow("No. of planting/emergence and harvests:", self.planting_dates)

        self.num_parameters = QLineEdit()
        self.form_layout.addRow("Number of parameters:", self.num_parameters)

        self.kc_calculation = QLineEdit()
        self.form_layout.addRow("Kc calculation:", self.kc_calculation)

        self.senescence = QLineEdit()
        self.form_layout.addRow("Senescence start and end:", self.senescence)

        self.p_values = QLineEdit()
        self.form_layout.addRow("p0, p1, p2h, p2l, p3 (mm):", self.p_values)

        self.ceres_temperatures = QLineEdit()
        self.form_layout.addRow("CERES temperatures:", self.ceres_temperatures)

        self.ceres_photoperiod = QLineEdit()
        self.form_layout.addRow("CERES photoperiod:", self.ceres_photoperiod)

        self.ceres_max_dev_rate = QLineEdit()
        self.form_layout.addRow("CERES maximum development rate:", self.ceres_max_dev_rate)

        # Additional fields
        self.rna_max = QLineEdit()
        self.form_layout.addRow("RNA_MAX:", self.rna_max)

        self.root_max = QLineEdit()
        self.form_layout.addRow("ROOT_MAX:", self.root_max)

        self.root_init = QLineEdit()
        self.form_layout.addRow("ROOT_INIT:", self.root_init)

        self.exu_fact = QLineEdit()
        self.form_layout.addRow("EXU_FACT:", self.exu_fact)

        self.deathfacmax = QLineEdit()
        self.form_layout.addRow("DEATHFACMAX:", self.deathfacmax)

        self.nsl = QLineEdit()
        self.form_layout.addRow("NSL:", self.nsl)

        self.rgr = QLineEdit()
        self.form_layout.addRow("RGR:", self.rgr)

        self.tempbase = QLineEdit()
        self.form_layout.addRow("TEMPBASE:", self.tempbase)

        self.sla = QLineEdit()
        self.form_layout.addRow("SLA:", self.sla)

        self.rsla = QLineEdit()
        self.form_layout.addRow("RSLA:", self.rsla)

        self.amx = QLineEdit()
        self.form_layout.addRow("AMX:", self.amx)

        self.eff = QLineEdit()
        self.form_layout.addRow("EFF:", self.eff)

        self.rkdf = QLineEdit()
        self.form_layout.addRow("RKDF:", self.rkdf)

        self.scp = QLineEdit()
        self.form_layout.addRow("SCP:", self.scp)

        self.rmainso = QLineEdit()
        self.form_layout.addRow("RMAINSO:", self.rmainso)

        self.asrqso = QLineEdit()
        self.form_layout.addRow("ASRQSO:", self.asrqso)

        self.tempstart = QLineEdit()
        self.form_layout.addRow("TEMPSTART:", self.tempstart)

        self.debr_fac = QLineEdit()
        self.form_layout.addRow("DEBR_FAC:", self.debr_fac)

        self.ls = QLineEdit()
        self.form_layout.addRow("LS:", self.ls)

        self.rlaicr = QLineEdit()
        self.form_layout.addRow("RLAICR:", self.rlaicr)

        self.eai = QLineEdit()
        self.form_layout.addRow("EAI:", self.eai)

        self.rmatr = QLineEdit()
        self.form_layout.addRow("RMATR:", self.rmatr)

        self.ssl = QLineEdit()
        self.form_layout.addRow("SSL:", self.ssl)

        self.srw = QLineEdit()
        self.form_layout.addRow("SRW:", self.srw)

        self.slaid_off = QLineEdit()
        self.form_layout.addRow("SLAID_OFF:", self.slaid_off)

        self.emergence_harvest_dates = QLineEdit()
        self.form_layout.addRow("Emergence and harvest dates:", self.emergence_harvest_dates)

        scroll.setWidget(form_widget)
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll)

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
        if os.path.exists(self.default_file):
            self.load_file(self.default_file)
        else:
            QMessageBox.warning(self, "File Not Found", f"Default file '{self.default_file}' not found. Starting with empty values.")

    def load_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

            self.version_input.setText(lines[1].split()[0])

            bool_settings = lines[2].split()
            for i, (label, checkbox) in enumerate(self.bool_settings.items()):
                checkbox.setChecked(bool_settings[i].lower() == 't')

            self.daily_timestep.setChecked(lines[4].strip().lower().startswith('t'))

            start_date = lines[5].split()[:3]
            self.start_date.setDate(QDate(int(start_date[0]), int(start_date[1]), int(start_date[2])))

            self.num_plant_types.setValue(int(lines[6].split()[0]))
            self.unit_soilco2.setCurrentIndex(int(lines[7].split()[0]) - 1)
            self.interception_model.setCurrentIndex(int(lines[8].split()[0]) - 1)
            self.latitude.setText(lines[9].split()[0])

            # Plant Type 1 Settings
            self.plant_type_name.setText(lines[11].strip())
            self.table_rows.setText(' '.join(lines[12].split()[:17]))
            self.planting_dates.setText(lines[13].split()[0])
            self.num_parameters.setText(lines[14].split()[0])
            self.kc_calculation.setText(lines[15].split()[0])
            self.senescence.setText(' '.join(lines[16].split()[:2]))
            self.p_values.setText(' '.join(lines[17].split()[:5]))
            self.ceres_temperatures.setText(' '.join(lines[18].split()[:13]))
            self.ceres_photoperiod.setText(' '.join(lines[19].split()[:3]))
            self.ceres_max_dev_rate.setText(' '.join(lines[20].split()[:3]))

            # Additional fields
            self.rna_max.setText(lines[21].split()[0])
            self.root_max.setText(lines[22].split()[0])
            self.root_init.setText(lines[23].split()[0])
            self.exu_fact.setText(lines[24].split()[0])
            self.deathfacmax.setText(lines[25].split()[0])
            self.nsl.setText(lines[26].split()[0])
            self.rgr.setText(lines[27].split()[0])
            self.tempbase.setText(lines[28].split()[0])
            self.sla.setText(lines[29].split()[0])
            self.rsla.setText(lines[30].split()[0])
            self.amx.setText(lines[31].split()[0])
            self.eff.setText(lines[32].split()[0])
            self.rkdf.setText(lines[33].split()[0])
            self.scp.setText(lines[34].split()[0])
            self.rmainso.setText(lines[35].split()[0])
            self.asrqso.setText(lines[36].split()[0])
            self.tempstart.setText(lines[37].split()[0])
            self.debr_fac.setText(lines[38].split()[0])
            self.ls.setText(lines[39].split()[0])
            self.rlaicr.setText(lines[40].split()[0])
            self.eai.setText(lines[41].split()[0])
            self.rmatr.setText(lines[42].split()[0])
            self.ssl.setText(lines[43].split()[0])
            self.srw.setText(lines[44].split()[0])
            self.slaid_off.setText(lines[45].split()[0])

            self.emergence_harvest_dates.setText(lines[47].strip())

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

            # Note: The tables are not included in this version of the GUI.
            # If you want to include the tables, you'll need to add UI elements for them
            # and include the logic here to write them to the file.

        print(f"File saved successfully: {filename}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AgroCInputEditor()
    window.show()
    sys.exit(app.exec_())