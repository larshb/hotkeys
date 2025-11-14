import subprocess
import pathlib
import yaml


HERE = pathlib.Path(__file__).parent.resolve()
CACHE = HERE / ".cache"


class Config:
    def __init__(self):
        self.data = {"variables": {"HERE": HERE}, "actions": {}}
        self.load_yaml()

    def load_yaml(self):
        config_dirs = [HERE / "config"]
        for config_dir in config_dirs:
            config_files = config_dir.rglob("*.yaml")
            for config_file in sorted(config_files):
                print("Load", str(config_file))
                patch = yaml.safe_load(open(config_file))
                for section in ["variables", "actions"]:
                    self.data[section].update(patch.get(section, {}))

    def get(self, key):
        return self.data[key]


class Actions:
    def __init__(self, gui_reference):
        self.gui = gui_reference
        self.actions = {}
        self.add_action("q", "Quit", "quit", "")

        self.config = Config()
        for key, action in self.config.get("actions").items():
            self.add_action(key, **action)

    def add_action(self, key, description, type, command):
        self.actions[key] = (description, type, command)

    def get_description(self, key):
        return self.actions.get(key, ("", None))[0]

    def get_callback(self, key):
        action = self.actions.get(key, None)
        if action:
            _, type, command = action
            if type == "quit":
                return self.quit
            elif type == "shell":
                command = command.format(**self.config.get("variables"))
                return lambda: subprocess.Popen(
                    command,
                    shell=True,
                    start_new_session=True,
                    # stdout=subprocess.DEVNULL,
                    # stderr=subprocess.DEVNULL,
                )
            else:
                raise KeyError("Unknown action type: %s", type)

    def quit(self):
        if not self.gui.close_on_keypress:
            self.gui.close_app()


def debug():
    class DummyGUI:
        def quit(self):
            pass

    _ = Actions(DummyGUI())


if __name__ == "__main__":
    debug()
