from dataclasses import dataclass
from typing import Any, Dict, List

import dacite
import yaml


@dataclass
class FieldTable:
    field_type: str
    modlist: List[Dict]

    @classmethod
    def from_file(cls, file_path: str) -> "FieldTable":
        """
        FieldTable class method for creating an instance from a yaml file

        Returns: instance of FieldTable
        """
        with open(file_path, "r") as f:
            config = yaml.safe_load(f)
        return FieldTable.from_dict(config)

    @classmethod
    def from_dict(cls, config: Dict) -> "FieldTable":
        """
        FieldTable class method for creating an instance from a dictionary.

        Returns: instance of FieldTable
        """
        return dacite.from_dict(data_class=cls, data=config["field_table"][0])

    def add_to_varlist(self, module: str, var: Dict):
        """
        Adds a variable to the varlist of module of
        calling FieldTable instance.

        Returns: Nothing to return, modifies calling instance
        """
        varlist = [mod for mod in self.modlist if mod["model_type"] == module][0][
            "varlist"
        ]
        varlist.append(var)

    def get_var(self, module: str, varname: str) -> Dict:
        """
        When called will return dictionary related to variable matching `varname`
        within module 'module', containg all current key:value pairs of the variable

        Returns: Dictionary
        """
        out = None

        for item in [mod for mod in self.modlist if mod["model_type"] == module][0][
            "varlist"
        ]:
            if varname == item["variable"]:
                out = item

        return out

    def get_subparam(self, module: str, varname: str, subparam_name: str) -> List[Dict]:
        """
        When called will return subparameter matching `subparam_name` of variable
        matching `varname` in module matching 'module'.

        Returns: List containing subparameter dictionary
        """
        subparam = None

        var = self.get_var(module=module, varname=varname)
        if var is not None:
            subparam = var[subparam_name]

        return subparam

    def get_value(self, module: str, varname: str, key: str) -> Any:
        """
        When called will return value of key matching 'key' in variable matching
        `varname` in module 'module'

        Returns: Any data type as values can be string or numeric
        """

        var = self.get_var(module=module, varname=varname)
        return var[key]

    def get_subparam_value(
        self, module: str, varname: str, listname: str, paramname: str
    ) -> Any:
        """
        When called will return value of parameter matching `paramname` contained within
        subparameter list matching `listname`, for variable matching `varname` within
        module 'module'.

        Returns: Any data type as values can be string or numeric
        """

        var = self.get_var(module=module, varname=varname)
        subparamlist = var[listname]
        return subparamlist[0][paramname]

    def get_variable_list(self, module: str) -> List:
        """
        When called will return list of variables contained within calling FieldTable
        instance specified module

        Returns: List of variables
        """
        variables = []
        varlist = [mod for mod in self.modlist if mod["model_type"] == module][0][
            "varlist"
        ]
        for item in varlist:
            variables.append(item["variable"])
        return variables

    def get_num_variables(self, module: str) -> int:
        """
        When called will return total number of variables associated with calling
        FieldTable instance specified module

        Returns: integer number of variables
        """
        varlist = [mod for mod in self.modlist if mod["model_type"] == module][0][
            "varlist"
        ]
        num_var = len(varlist)
        return num_var

    def get_subparam_list(self, module: str, varname: str) -> List[Dict]:
        """
        When called will return List of dictionary subparameters associated with
        variable matching `varname` of FieldTable instance specified module.

        Returns: List of dictionary objects
        """
        subparamlist = []

        var = self.get_var(module=module, varname=varname)
        for key in var:
            if type(var[key]) == list:
                subparamlist.append(key)

        return subparamlist

    def get_num_subparam(self, module: str, varname: str) -> int:
        """
        When called will return number of subparameters associated with variable
        matching `varname` in calling FieldTable instance specified module.

        Returns: integer number of subparameters
        """
        subparamlist = []

        var = self.get_var(module=module, varname=varname)
        for key in var:
            if type(var[key]) == list:
                subparamlist.append(key)

        return len(subparamlist)

    def set_value(self, module: str, varname: str, key: str, value):
        """
        This method sets the value associated with the key matching 'key' of the
        variable matching `varname` withing the calling FieldTable instance specified
        module.

        Returns: Nothing to return, modifies calling instance
        """

        changed_var = self.get_var(module=module, varname=varname)
        changed_var[key] = value

    def set_subparam_value(
        self, module: str, varname: str, listname: str, subparamname: str, value
    ):
        """
        This method sets the value associated with the key matching 'subparamname`
        within the subparameter list of the variable matching `varname` withing the
        calling FieldTable instance specified module.

        Returns: Nothing to return, modifies calling instance
        """

        var = self.get_var(module=module, varname=varname)
        paramlist = var[listname]
        paramlist[0][subparamname] = value

    def set_var_name(self, module: str, old_name: str, new_name: str):
        """
        This method changes the name of a currently existing variable matching `old_name`
        in the calling instance of FieldTable to `new_name` within specified module.

        Returns: Nothing to return, modifies calling instance
        """
        changed_var = self.get_var(module=module, varname=old_name)
        changed_var["variable"] = new_name

    def set_var_attr_name(self, module: str, varname: str, oldname: str, newname: str):
        """
        This method changes the name of a currently existing variable attribute matching
        `oldname` to `newname` in the variable matching `varname` of the calling instance
        of FieldTable of the specified module.

        Returns: Nothing to return, modifies calling instance
        """
        var = self.get_var(module=module, varname=varname)

        var[newname] = var.pop(oldname)

    def set_subparam_name(
        self, module: str, varname: str, listname: str, oldname: str, newname: str
    ):
        """
        This method sets the subparameter name of subparameter in the variable matching
        `varname`, changing it `oldname` to `newname` in the calling instance of FieldTable's
        specified module.

        Returns: Nothing to return, modifies calling instance
        """

        var = self.get_var(module=module, varname=varname)
        paramlist = var[listname]
        paramlist[0][newname] = paramlist[0].pop(oldname)

    # Tracer method
    def check_if_prognostic(self, module: str, tracername: str) -> bool:
        """
        This method checks if the tracer matching `tracername` is prognostic or
        diagnostic of the specified. This is done by checking the value of the
        `tracer_type` key of the tracer.

        Returns: True if prognostic, False otherwise
        """
        tracer = self.get_var(module=module, varname=tracername)

        if "tracer_type" in tracer:
            tracer_type = tracer["tracer_type"]
            if tracer_type == "prognostic":
                return True
            if tracer_type == "diagnostic":
                return False
        else:
            return False

        return None

    # Tracer method
    def adjust_mass(self):
        model = self.model_type
        # TODO: Get list of models which need mass adjustment

    # Tracer method
    def adjust_positive_def(self):
        model = self.model_type
        # TODO: Get list of models which need to be adjusted to remain positive definite
