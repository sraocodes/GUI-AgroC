#############################################################################################################

"""
Author: Sathyanarayan Rao

Description:
This Python script uses PyQt5 to create a GUI for editing the 'plants.in' configuration file
used in the AgroC simulation software. The GUI supports editing general settings, plant parameters,
and tabular data specific to agricultural modeling and simulation processes.

The application allows users to:
- Load and modify existing configuration data.
- Save changes to a new configuration file.
- Dynamically add and remove rows in data tables.
- Reset to default settings.
"""
############# IMPORT all necessary Libraries ################################################################

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QLineEdit, QCheckBox, QDateEdit, QSpinBox, QComboBox,
                             QPushButton, QFileDialog, QMessageBox, QScrollArea, QLabel,
                             QTableWidget, QTableWidgetItem, QTabWidget, QListWidget)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


###############################################################################################################


class AgroCInputEditor(QMainWindow):
# Main class for the AgroC Plants.in Input Editor
# Initialize the application, set main window properties, and load default values

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AgroC Plants.in Input Editor")
        self.setGeometry(100, 100, 800, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_form()
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.central_widget, "General Settings")
        self.tab_widget.addTab(self.create_tabular_data(), "Tabular Data")
        self.setCentralWidget(self.tab_widget)
        self.create_buttons()

        self.default_file = "plants.in"
        self.modified_file = "plants_mod.in"
        
        # Load default values after creating all UI elements
        self.load_default_values()


    ##########################################
    # Create the form layout for user input

    def create_form(self):
        # Scroll area to accommodate all input fields dynamically
        scroll = QScrollArea()
        form_widget = QWidget()
        self.form_layout = QFormLayout(form_widget)

        # General Settings
        self.version_input = QLineEdit()
        self.form_layout.addRow("Software Version:", self.version_input)

        # Boolean settings
        self.bool_settings = {
            "CO2 Fluxes Enabled": QCheckBox(),
            "Respiration Enabled": QCheckBox(),
            "Maintenance Growth Enabled": QCheckBox(),
            "Water Stress Enabled": QCheckBox(),
            "Root Exudation Enabled": QCheckBox(),
            "Root Death Enabled": QCheckBox(),
            "Harvest Residues Included": QCheckBox(),
            "Use Farquhar Model": QCheckBox()
        }
        for label, checkbox in self.bool_settings.items():
            self.form_layout.addRow(label, checkbox)

        self.daily_timestep = QCheckBox()
        self.form_layout.addRow("Daily Timestep Enabled:", self.daily_timestep)

        self.start_date = QDateEdit()
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.form_layout.addRow("Simulation Start Date:", self.start_date)

        self.num_plant_types = QSpinBox()
        self.num_plant_types.setMinimum(1)
        self.form_layout.addRow("Number of Plant Types:", self.num_plant_types)

        self.unit_soilco2 = QComboBox()
        self.unit_soilco2.addItems(["mm", "cm", "dm", "m", "km"])
        self.form_layout.addRow("Soil CO2 Measurement Unit:", self.unit_soilco2)

        self.interception_model = QComboBox()
        self.interception_model.addItems(["Bormann", "Hoyningen-Huene"])
        self.form_layout.addRow("Rainfall Interception Model:", self.interception_model)

        self.latitude = QLineEdit()
        self.form_layout.addRow("Site Latitude (degrees):", self.latitude)

        # Plant Type 1 Settings
        self.form_layout.addRow(QLabel("Plant Type 1 Settings"))

        self.plant_type_name = QLineEdit()
        self.form_layout.addRow("Plant Type Name:", self.plant_type_name)

        self.table_rows = QLineEdit()
        self.form_layout.addRow("number of rows in the 17 tables:", self.table_rows)

        self.planting_dates = QLineEdit()
        self.form_layout.addRow("Planting/Emergence and Harvest Dates:", self.planting_dates)

        self.num_parameters = QLineEdit()
        self.form_layout.addRow("Number of Parameters:", self.num_parameters)

        self.kc_calculation = QLineEdit()
        self.form_layout.addRow("Kc Calculation Method:", self.kc_calculation)

        self.senescence = QLineEdit()
        self.form_layout.addRow("Senescence Start and End (DOY):", self.senescence)

        self.p_values = QLineEdit()
        self.form_layout.addRow("P Values (mm):", self.p_values)

        self.ceres_temperatures = QLineEdit()
        self.form_layout.addRow("CERES Temperatures (C):", self.ceres_temperatures)

        self.ceres_photoperiod = QLineEdit()
        self.form_layout.addRow("CERES Photoperiod:", self.ceres_photoperiod)

        self.ceres_max_dev_rate = QLineEdit()
        self.form_layout.addRow("CERES Max Development Rate:", self.ceres_max_dev_rate)

        # Additional fields
        self.rna_max = QLineEdit()
        self.form_layout.addRow("RNA_MAX - Max Root Depth Without Water Uptake (mm):", self.rna_max)
        self.rna_max.setToolTip("Maximum depth above which no root water uptake is considered in the model.")

        self.root_max = QLineEdit()
        self.form_layout.addRow("ROOT_MAX - Maximum Rooting Depth (mm):", self.root_max)
        self.root_max.setToolTip("The deepest extent of the root zone from which the plant can uptake water.")

        self.root_init = QLineEdit()
        self.form_layout.addRow("ROOT_INIT - Initial Rooting Depth (mm):", self.root_init)
        self.root_init.setToolTip("Initial depth of the plant's roots at the beginning of the simulation.")

        self.exu_fact = QLineEdit()
        self.form_layout.addRow("EXU_FACT - Root Exudation Factor:", self.exu_fact)
        self.exu_fact.setToolTip("Factor controlling the rate of root exudation, affecting soil chemistry and microbe interactions.")

        self.deathfacmax = QLineEdit()
        self.form_layout.addRow("DEATHFACMAX - Maximum Death Factor:", self.deathfacmax)
        self.deathfacmax.setToolTip("Controls the maximum rate of plant death due to various stress factors.")

        self.nsl = QLineEdit()
        self.form_layout.addRow("NSL - Number of Seedlings per m²:", self.nsl)
        self.nsl.setToolTip("Specifies the density of seedlings planted per square meter.")

        self.rgr = QLineEdit()
        self.form_layout.addRow("RGR - Relative Growth Rate (ha/ha/C/day):", self.rgr)
        self.rgr.setToolTip("The rate at which the plant's growth area increases relative to the temperature.")

        self.tempbase = QLineEdit()
        self.form_layout.addRow("TEMPBASE - Base Temperature for Growth (°C):", self.tempbase)
        self.tempbase.setToolTip("The lowest temperature at which the plant begins to grow.")

        self.sla = QLineEdit()
        self.form_layout.addRow("SLA - Specific Leaf Area (ha leaf/kg DM):", self.sla)
        self.sla.setToolTip("Area of leaves produced per kilogram of dry matter.")

        self.rsla = QLineEdit()
        self.form_layout.addRow("RSLA - Rate of Change in Specific Leaf Area (ha leaf/kg DM/°C/day):", self.rsla)
        self.rsla.setToolTip("Change in specific leaf area per unit of thermal time.")

        self.amx = QLineEdit()
        self.form_layout.addRow("AMX - Max Assimilation Rate (kg CO2/ha leaf/h):", self.amx)
        self.amx.setToolTip("Maximum rate at which the plant can assimilate carbon dioxide under ideal conditions.")

        self.eff = QLineEdit()
        self.form_layout.addRow("EFF - Initial Light Use Efficiency (kg CO2/ha leaf/h)/(J/m²/s):", self.eff)
        self.eff.setToolTip("Efficiency with which the plant converts absorbed light into stored energy via photosynthesis.")

        self.rkdf = QLineEdit()
        self.form_layout.addRow("RKDF - Diffuse Light Extinction Coefficient:", self.rkdf)
        self.rkdf.setToolTip("Coefficient that determines how much light is lost due to diffusion within the canopy.")

        self.scp = QLineEdit()
        self.form_layout.addRow("SCP - Scattering Coefficient for PAR (Photosynthetically Active Radiation):", self.scp)
        self.scp.setToolTip("Determines the fraction of PAR that is scattered by leaves in the canopy.")

        self.rmainso = QLineEdit()
        self.form_layout.addRow("RMAINSO - Maintenance Respiration Rate of Storage Organs (kg CH₂O/kg DM/day):", self.rmainso)
        self.rmainso.setToolTip("Rate at which storage organs respire, consuming sugars to maintain living tissues.")

        self.asrqso = QLineEdit()
        self.form_layout.addRow("ASRQSO - Assimilation Requirement for Storage Organs (kg CH₂O/kg DM):", self.asrqso)
        self.asrqso.setToolTip("Amount of carbohydrates required to produce a kilogram of dry matter in storage organs.")

        self.tempstart = QLineEdit()
        self.form_layout.addRow("TEMPSTART - Start Temperature for Plant Growth (°C*day):", self.tempstart)
        self.tempstart.setToolTip("Cumulative temperature from emergence until growth begins in spring.")

        self.debr_fac = QLineEdit()
        self.form_layout.addRow("DEBR_FAC - Dead Leaf Debris Factor:", self.debr_fac)
        self.debr_fac.setToolTip("Factor that determines the rate at which dead leaves are added to soil organic matter.")

        self.ls = QLineEdit()
        self.form_layout.addRow("LS - Leaf Area Index Switch from Temperature to Radiation Limitation (ha/ha):", self.ls)
        self.ls.setToolTip("Leaf area index at which growth switches from being temperature-limited to radiation-limited.")

        self.rlaicr = QLineEdit()
        self.form_layout.addRow("RLAICR - Critical Leaf Area Index for Self-Shading (ha/ha):", self.rlaicr)
        self.rlaicr.setToolTip("Leaf area index beyond which leaves begin to shade each other, affecting photosynthesis.")

        self.eai = QLineEdit()
        self.form_layout.addRow("EAI - Ear Area Index (2-sided) at Emergence:", self.eai)
        self.eai.setToolTip("Index measuring the area of ears (grain-bearing part of the plant) relative to ground area at emergence.")

        self.rmatr = QLineEdit()
        self.form_layout.addRow("RMATR - Maturity Class at Emergence:", self.rmatr)
        self.rmatr.setToolTip("Maturity classification of the crop at emergence, affecting growth and development stages.")

        self.ssl = QLineEdit()
        self.form_layout.addRow("SSL - Specific Seedling Leaf Area (m² leaf/seedling):", self.ssl)
        self.ssl.setToolTip("Leaf area of a single seedling, important for early growth stage modeling.")

        self.srw = QLineEdit()
        self.form_layout.addRow("SRW - Specific Root Weight (m/g):", self.srw)
        self.srw.setToolTip("Mass of roots per meter, used to calculate the total biomass of roots.")

        self.slaid_off = QLineEdit()
        self.form_layout.addRow("SLAID_OFF - Seasonal Leaf Area Index Decline (ha/ha):", self.slaid_off)
        self.slaid_off.setToolTip("Reduction in leaf area index after the growing season ends, reflecting leaf drop and senescence.")

        self.emergence_harvest_dates = QLineEdit()
        self.form_layout.addRow("Emergence and Harvest Dates:", self.emergence_harvest_dates)
        self.emergence_harvest_dates.setToolTip("Specific dates for plant emergence and harvest, critical for seasonal management.")


        scroll.setWidget(form_widget)
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll)

    ##########################################
    # The create_buttons method adds buttons for resetting to defaults and saving changes. 

    def create_buttons(self):
        # Add layout and buttons for save and reset actions
        button_layout = QHBoxLayout()
        reset_button = QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_to_default)
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(save_button)
        self.layout.addLayout(button_layout)

    ##########################################

    def load_default_values(self):
        # Attempt to load settings from the bundled default plants.in file.
        try:
            self.load_file(self.default_file)
        except Exception as e:
            QMessageBox.critical(self, "Error Loading Defaults", f"An error occurred while loading the default settings: {str(e)}\nPlease check that the default file is correctly placed and not corrupted.")

    ##########################################

    def load_file(self, filename):
    # Reads the file and sets the GUI fields to the file's values
    # Error handling included to capture and debug issues during file read
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

            # Load tabular data
            current_table = -1
            table_rows = list(map(int, self.table_rows.text().split()))
            for line in lines[49:]:  # Start from line 49 (0-indexed) which is the start of tabular data
                if line.strip().startswith('#'):
                    current_table += 1
                    continue
                
                if current_table >= len(self.tables):
                    break

                values = line.strip().split()
                if values:
                    row = self.tables[current_table].rowCount() - 1  # -1 because we start with one empty row
                    if row < table_rows[current_table]:
                        for col, value in enumerate(values):
                            if col < self.tables[current_table].columnCount():
                                self.tables[current_table].setItem(row, col, QTableWidgetItem(value))
                        if row < table_rows[current_table] - 1:  # Don't add extra row for the last entry
                            self.tables[current_table].insertRow(row + 1)

            # Remove extra rows
            for i, table in enumerate(self.tables):
                while table.rowCount() > table_rows[i]:
                    table.removeRow(table.rowCount() - 1)

            # Update the table list selection
            self.table_list.setCurrentRow(0)
            self.show_selected_table(self.table_list.item(0))

        except Exception as e:
            print(f"An error occurred while loading the file: {str(e)}")
            import traceback
            traceback.print_exc()

    ##########################################
    # Setup tabular data UI, including list and display of data tables

    def create_tabular_data(self):
        # Main widget and layout for tabular data section
        tabular_data_widget = QWidget()
        tabular_layout = QHBoxLayout(tabular_data_widget)

        # Create left panel for table names
        self.table_list = QListWidget()
        self.table_list.setMaximumWidth(300)
        self.table_list.itemClicked.connect(self.show_selected_table)
        tabular_layout.addWidget(self.table_list)

        # Create right panel for table display
        self.table_display = QWidget()
        self.table_display_layout = QVBoxLayout(self.table_display)
        tabular_layout.addWidget(self.table_display)

        # Populate table list
        table_headers = [
            "Temperature sum against reduction factor of the maximal light assimilation rate",
            "Effective temperature against reduction factor of the maximal light assimilation rate",
            "Effective temperature against reduction factor of the development rate, if DVS < 1",
            "Effective temperature against reduction factor of the development rate, if DVS > 1",
            "DVS against fraction of dry matter allocated to the shoot",
            "Temperature sum against fraction of dry matter allocated to the leaves",
            "Temperature sum against fraction of dry matter allocated to the stem",
            "Temperature sum against fraction of dry matter allocated to the cob/root",
            "DVS against death rate of leaves reduction function",
            "Effective temperature against death rate of the leaves",
            "DVS or time against akc",
            "Relative root depth against root density",
            "DVS against N content leaves",
            "DVS against N content stems",
            "DVS against N content roots",
            "DVS against N content storage organs",
            "DVS against N content crowns"
        ]

        for i, header in enumerate(table_headers):
            self.table_list.addItem(f"Table {i+1}: {header}")

        # Create tables (but don't add them to layout yet)
        self.tables = []
        table_rows = list(map(int, self.table_rows.text().split()))
        for i, _ in enumerate(table_headers):
            num_rows = table_rows[i] if i < len(table_rows) else 1
            table = QTableWidget(num_rows, 2)
            table.setHorizontalHeaderLabels(["Column 1", "Column 2"])
            table.horizontalHeader().setStretchLastSection(True)
            table.verticalHeader().setVisible(False)
            table.setEditTriggers(QTableWidget.AllEditTriggers)
            self.tables.append(table)

        # Add buttons to the tabular data tab
        button_layout = QHBoxLayout()
        reset_button = QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_to_default)
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(save_button)
        self.table_display_layout.addLayout(button_layout)

        # Show the first table by default
        self.show_selected_table(self.table_list.item(0))

        return tabular_data_widget

    # Show the selected data table from the list when clicked
    def show_selected_table(self, item):
        # Clear the display and setup the selected table along with + and - buttons
        for i in reversed(range(self.table_display_layout.count())):
            widget = self.table_display_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Get the index of the selected table
        table_index = self.table_list.row(item)

        # Ensure the buttons exist; if not, create them
        if not hasattr(self, 'add_button'):
            self.add_button = QPushButton("+")
            self.remove_button = QPushButton("-")
        
        # Disconnect existing connections if any (important to avoid multiple connections leading to multiple actions)
        try:
            self.add_button.clicked.disconnect()
        except TypeError:
            pass  # no connections
        try:
            self.remove_button.clicked.disconnect()
        except TypeError:
            pass  # no connections
        
        # Connect the buttons with the new table index
        self.add_button.clicked.connect(lambda: self.add_row_to_table(table_index))
        self.remove_button.clicked.connect(lambda: self.remove_row_from_table(table_index))

        # Add buttons to layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        self.table_display_layout.addLayout(button_layout)

        # Add the selected table to the display
        self.table_display_layout.addWidget(self.tables[table_index])


    # Add a new row to the currently displayed table
    def add_row_to_table(self, table_index):
        table = self.tables[table_index]
        row_count = table.rowCount()
        table.insertRow(row_count)
        table.setItem(row_count, 0, QTableWidgetItem("0"))  # Initialize new row with default values
        table.setItem(row_count, 1, QTableWidgetItem("0"))

    # Remove the last row from the currently displayed table
    def remove_row_from_table(self, table_index):
        table = self.tables[table_index]
        if table.rowCount() > 0:
            table.removeRow(table.rowCount() - 1)  # Remove the last row



    def update_table_rows(self):
        try:
            new_rows = list(map(int, self.table_rows.text().split()))
            if len(new_rows) == 17:
                for i, table in enumerate(self.tables):
                    current_rows = table.rowCount()
                    new_row_count = new_rows[i]
                    if new_row_count > current_rows:
                        for _ in range(new_row_count - current_rows):
                            row = table.rowCount()
                            table.insertRow(row)
                            table.setItem(row, 0, QTableWidgetItem("0"))
                            table.setItem(row, 1, QTableWidgetItem("0"))
                    elif new_row_count < current_rows:
                        for _ in range(current_rows - new_row_count):
                            table.removeRow(table.rowCount() - 1)
                
                # Update the currently displayed table
                current_item = self.table_list.currentItem()
                if current_item:
                    self.show_selected_table(current_item)
        except ValueError:
            pass  # Ignore invalid input


    ##########################################

    def reset_to_default(self):
        self.load_default_values()
        QMessageBox.information(self, "Reset Complete", "All values have been reset to default.")

    ##########################################

    def save_changes(self):
    # Calls generate_plants_in to write changes to plants_mod.in and informs the user
        self.generate_plants_in(self.modified_file)
        QMessageBox.information(self, "Save Complete", f"Changes have been saved to {self.modified_file}")

    ##########################################

    def generate_plants_in(self, filename):
    # Writes the current settings from the GUI back to a new plants.in file
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
            # Dynamically write the number of rows for each table
            table_rows = [str(table.rowCount()) for table in self.tables]
            file.write(f"{' '.join(table_rows)}   number of rows in the 17 tables\n")
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
            file.write("# emergence and harvest date(s)\n")
            file.write(f"{self.emergence_harvest_dates.text()}\n")
            # Write tabular data
            # Dynamically fetch and write the number of rows for each table
            table_rows = [str(table.rowCount()) for table in self.tables]
            file.write(f"{' '.join(table_rows)}   number of rows in the 17 tables\n")
            # Write tabular data for each table
            for i, table in enumerate(self.tables):
                file.write(f"# (Tab.{i+1}) [for crop 1 2 3 5] #    {self.table_list.item(i).text().split(': ', 1)[1]}\n")
                for row in range(table.rowCount()):
                    row_data = []
                    for col in range(table.columnCount()):
                        item = table.item(row, col)
                        row_data.append(item.text() if item and item.text() else "0")
                    file.write("    " + "        ".join(row_data) + "\n")
        print(f"File saved successfully: {filename}")

if __name__ == "__main__":
    # Create the application instance, set up the main window, and start the event loop
    app = QApplication(sys.argv)
    window = AgroCInputEditor()
    window.show()
    sys.exit(app.exec_())
