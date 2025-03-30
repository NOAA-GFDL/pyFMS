import yaml


def test_write_input_files():
    diag_table = yaml.load(
        """
title: test_diag_manager
base_date: 2 1 1 1 1 1

diag_files:
- file_name: test_send_data
  freq: 1 hours
  time_units: hours
  unlimdim: time
  varlist:
  - module: atm_mod
    var_name: var_3d
    reduction: average
    kind: r4
    output_name: var3_avg
  - module: atm_mod
    var_name: var_2d
    reduction: average
    kind: r4
    output_name: var2_avg
""",
        Loader=yaml.Loader,
    )

    diag_table_yaml_file = open("diag_table.yaml", "w")
    yaml.dump(diag_table, diag_table_yaml_file, sort_keys=False)
    diag_table_yaml_file.close()

    input_nml = """
&diag_manager_nml
    use_modern_diag = .true.
/"""
    input_nml_file = open("input.nml", "w")
    input_nml_file.write(input_nml)
    input_nml_file.close()
